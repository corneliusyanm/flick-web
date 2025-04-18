from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from .models import Station, Transaction, Member
from django import forms

# Create your views here.


def home(request):
    return render(request, "core/home.html")


@login_required
def active_stations(request):
    """
    Display all active stations in a card grid
    """
    stations = Station.objects.filter(is_active=True).select_related("station_type")

    # Get active transactions for each station
    for station in stations:
        station.active_transaction = station.transactions.filter(is_active=True).first()

    context = {"stations": stations, "current_time": timezone.now()}

    return render(request, "core/active_stations.html", context)


class NewSessionForm(forms.Form):
    member = forms.ModelChoiceField(
        queryset=Member.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Member",
    )
    station = forms.ModelChoiceField(
        queryset=Station.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Station",
    )
    duration = forms.IntegerField(
        min_value=15,
        max_value=240,
        initial=60,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Duration (minutes)",
    )
    is_loss = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Loss Transaction",
    )
    amount = forms.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Amount ($)",
    )


@login_required
def new_session(request):
    """
    Create a new active session
    """
    available_stations = Station.objects.filter(is_active=True)

    # Filter out stations that already have active transactions
    for station in available_stations:
        if station.transactions.filter(is_active=True).exists():
            available_stations = available_stations.exclude(id=station.id)

    form = NewSessionForm()
    form.fields["station"].queryset = available_stations

    if request.method == "POST":
        form = NewSessionForm(request.POST)
        form.fields["station"].queryset = available_stations

        if form.is_valid():
            station = form.cleaned_data["station"]
            member = form.cleaned_data["member"]
            duration = form.cleaned_data["duration"]
            is_loss = form.cleaned_data["is_loss"]
            amount = form.cleaned_data["amount"]

            # Check if station is already in use
            if station.transactions.filter(is_active=True).exists():
                messages.error(
                    request,
                    f"Station {station.name} is already in use. Please select another station.",
                )
                return render(request, "core/new_session.html", {"form": form})

            # Create new transaction
            transaction = Transaction.objects.create(
                member=member,
                station=station,
                clock_in=timezone.now(),
                duration=duration,
                is_loss=is_loss,
                status="active",
                is_active=True,
                amount=amount,
                created_by=request.user,
            )

            messages.success(
                request, f"New session created for {member.name} on {station.name}"
            )
            return redirect("core:active_stations")

    return render(request, "core/new_session.html", {"form": form})


class PaymentForm(forms.Form):
    amount_paid = forms.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Amount Paid ($)",
    )
    payment_method = forms.ChoiceField(
        choices=[
            ("cash", "Cash"),
            ("card", "Credit/Debit Card"),
            ("transfer", "Bank Transfer"),
            ("e-wallet", "E-Wallet"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Payment Method",
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        label="Notes",
    )


@login_required
def payment_form(request, transaction_id):
    """
    Process payment for a loss transaction
    """
    transaction = get_object_or_404(Transaction, pk=transaction_id)

    if not transaction.is_loss:
        messages.warning(request, "This transaction is not marked as a loss.")
        return redirect("core:complete_transaction", transaction_id=transaction.id)

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount_paid = form.cleaned_data["amount_paid"]
            payment_method = form.cleaned_data["payment_method"]
            notes = form.cleaned_data["notes"]

            # Record payment details in transaction
            transaction.amount = amount_paid  # Update with actual amount paid
            transaction.details = f"Payment Method: {payment_method}\nNotes: {notes}\n{transaction.details}"
            transaction.status = "paid"
            transaction.is_active = False
            transaction.save()

            messages.success(
                request,
                f"Payment of ${amount_paid} processed successfully for loss transaction.",
            )
            return redirect("core:active_stations")
    else:
        form = PaymentForm(initial={"amount_paid": transaction.amount})

    return render(
        request, "core/payment_form.html", {"transaction": transaction, "form": form}
    )


@login_required
def complete_transaction(request, transaction_id):
    """
    Complete a transaction: mark as paid or go to payment if it's a loss
    """
    transaction = get_object_or_404(Transaction, pk=transaction_id)

    if request.method == "POST":
        if transaction.is_loss:
            # Redirect to payment form
            return redirect("core:payment_form", transaction_id=transaction.id)
        else:
            # Mark as completed and paid
            transaction.status = "paid"
            transaction.is_active = False
            transaction.save()
            messages.success(
                request,
                f"Transaction for {transaction.member.name} completed successfully.",
            )
            return redirect("core:active_stations")

    # If not POST, show confirmation page
    return render(
        request, "core/complete_transaction.html", {"transaction": transaction}
    )


@login_required
def move_transaction(request, transaction_id):
    """
    Move a transaction to another station of the same type
    """
    transaction = get_object_or_404(Transaction, pk=transaction_id)

    if request.method == "POST":
        new_station_id = request.POST.get("new_station")
        if new_station_id:
            new_station = get_object_or_404(Station, pk=new_station_id)

            # Check if station type matches
            if new_station.station_type != transaction.station.station_type:
                return render(
                    request,
                    "core/move_transaction.html",
                    {
                        "transaction": transaction,
                        "error": "Cannot move to a different station type",
                        "available_stations": Station.objects.filter(
                            station_type=transaction.station.station_type,
                            is_active=True,
                        ).exclude(pk=transaction.station.pk),
                    },
                )

            # Check if new station is available
            if new_station.is_in_use:
                return render(
                    request,
                    "core/move_transaction.html",
                    {
                        "transaction": transaction,
                        "error": "Selected station is already in use",
                        "available_stations": Station.objects.filter(
                            station_type=transaction.station.station_type,
                            is_active=True,
                        ).exclude(pk=transaction.station.pk),
                    },
                )

            # Move the transaction
            transaction.station = new_station
            transaction.save()

            messages.success(
                request, f"Transaction moved to {new_station.name} successfully."
            )
            return redirect("core:active_stations")

    # If not POST, or if validation failed, show move form
    available_stations = Station.objects.filter(
        station_type=transaction.station.station_type, is_active=True
    ).exclude(pk=transaction.station.pk)

    return render(
        request,
        "core/move_transaction.html",
        {"transaction": transaction, "available_stations": available_stations},
    )

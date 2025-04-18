from django.db import models
from django.conf import settings

# Create your models here.


class StationType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=100)
    station_type = models.ForeignKey(StationType, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.station_type.name})"

    @property
    def is_in_use(self):
        return self.transactions.filter(is_active=True).exists()

    @property
    def current_transaction(self):
        try:
            return self.transactions.filter(is_active=True).latest("clock_in")
        except Transaction.DoesNotExist:
            return None


class Transaction(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("paid", "Paid"),
        ("loss", "Loss"),
        ("cancelled", "Cancelled"),
    ]

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="transactions"
    )
    station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="transactions"
    )
    clock_in = models.DateTimeField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    is_loss = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    is_active = models.BooleanField(default=True)
    details = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_transactions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member.name} - {self.station.name} - {self.clock_in.strftime('%Y-%m-%d %H:%M')}"

    @property
    def estimated_end_time(self):
        import datetime

        return self.clock_in + datetime.timedelta(minutes=self.duration)

    @property
    def time_remaining(self):
        import datetime

        now = datetime.datetime.now(self.clock_in.tzinfo)
        if now > self.estimated_end_time:
            return datetime.timedelta(0)
        return self.estimated_end_time - now

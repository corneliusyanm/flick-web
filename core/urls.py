from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("stations/active/", views.active_stations, name="active_stations"),
    path("stations/new-session/", views.new_session, name="new_session"),
    path(
        "transaction/<int:transaction_id>/complete/",
        views.complete_transaction,
        name="complete_transaction",
    ),
    path(
        "transaction/<int:transaction_id>/payment/",
        views.payment_form,
        name="payment_form",
    ),
    path(
        "transaction/<int:transaction_id>/move/",
        views.move_transaction,
        name="move_transaction",
    ),
]

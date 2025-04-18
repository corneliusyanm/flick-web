from django.contrib import admin
from .models import StationType, Branch, Member, Station, Transaction


@admin.register(StationType)
class StationTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone", "created_at", "updated_at")
    search_fields = ("name", "address", "phone")
    list_filter = ("created_at", "updated_at")


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "created_at", "updated_at")
    search_fields = ("name", "phone")
    list_filter = ("created_at", "updated_at")


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "station_type",
        "branch",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("name",)
    list_filter = ("station_type", "branch", "is_active", "created_at", "updated_at")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "station",
        "clock_in",
        "duration",
        "status",
        "is_loss",
        "amount",
        "created_at",
    )
    search_fields = ("member__name", "station__name")
    list_filter = ("status", "is_loss", "station__station_type", "created_at")

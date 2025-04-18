from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from core.models import StationType, Branch, Member, Station, Transaction
import datetime
import random


class Command(BaseCommand):
    help = "Populates the database with sample data for testing"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating sample data...")

        # Create superuser if not exists
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin")
            self.stdout.write(self.style.SUCCESS("Superuser created"))

        # Create station types
        station_types = [
            {"name": "PS5", "description": "PlayStation 5 console"},
            {"name": "PS4", "description": "PlayStation 4 console"},
            {"name": "PS4 Pro", "description": "PlayStation 4 Pro console"},
            {"name": "PS3", "description": "PlayStation 3 console"},
            {"name": "Netflix", "description": "Netflix streaming service"},
        ]

        for st_data in station_types:
            StationType.objects.get_or_create(name=st_data["name"], defaults=st_data)

        self.stdout.write(
            self.style.SUCCESS(f"Created {len(station_types)} station types")
        )

        # Create branch
        branch, created = Branch.objects.get_or_create(
            name="Main Branch",
            defaults={"address": "123 Main Street, City", "phone": "555-123-4567"},
        )

        self.stdout.write(self.style.SUCCESS("Branch created"))

        # Create members
        member_names = [
            "John Doe",
            "Jane Smith",
            "Mike Johnson",
            "Lisa Brown",
            "David Miller",
        ]
        members = []

        for name in member_names:
            phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            member, created = Member.objects.get_or_create(
                name=name, defaults={"phone": phone}
            )
            members.append(member)

        self.stdout.write(self.style.SUCCESS(f"Created {len(members)} members"))

        # Create stations
        stations_data = []

        # PS5 stations
        ps5 = StationType.objects.get(name="PS5")
        for i in range(1, 4):
            stations_data.append(
                {"name": f"PS5-{i}", "station_type": ps5, "branch": branch}
            )

        # PS4 stations
        ps4 = StationType.objects.get(name="PS4")
        for i in range(1, 5):
            stations_data.append(
                {"name": f"PS4-{i}", "station_type": ps4, "branch": branch}
            )

        # PS4 Pro stations
        ps4pro = StationType.objects.get(name="PS4 Pro")
        for i in range(1, 3):
            stations_data.append(
                {"name": f"PS4Pro-{i}", "station_type": ps4pro, "branch": branch}
            )

        # PS3 stations
        ps3 = StationType.objects.get(name="PS3")
        for i in range(1, 3):
            stations_data.append(
                {"name": f"PS3-{i}", "station_type": ps3, "branch": branch}
            )

        # Netflix stations
        netflix = StationType.objects.get(name="Netflix")
        for i in range(1, 3):
            stations_data.append(
                {"name": f"Netflix-{i}", "station_type": netflix, "branch": branch}
            )

        stations = []
        for station_data in stations_data:
            station, created = Station.objects.get_or_create(
                name=station_data["name"],
                defaults={
                    "station_type": station_data["station_type"],
                    "branch": station_data["branch"],
                    "is_active": True,
                },
            )
            stations.append(station)

        self.stdout.write(self.style.SUCCESS(f"Created {len(stations)} stations"))

        # Create some active transactions
        admin_user = User.objects.get(username="admin")
        now = timezone.now()

        # Clear existing transactions
        Transaction.objects.all().delete()

        # Create 5 active transactions
        for i in range(5):
            station = random.choice(stations)
            member = random.choice(members)
            duration = random.choice([30, 60, 90, 120])
            clock_in = now - datetime.timedelta(minutes=random.randint(0, 30))
            is_loss = random.random() < 0.2  # 20% chance of being a loss

            Transaction.objects.create(
                member=member,
                station=station,
                clock_in=clock_in,
                duration=duration,
                is_loss=is_loss,
                status="active",
                is_active=True,
                amount=duration * 0.5,  # $0.50 per minute
                created_by=admin_user,
            )

        self.stdout.write(self.style.SUCCESS("Created 5 active transactions"))
        self.stdout.write(self.style.SUCCESS("Sample data created successfully!"))

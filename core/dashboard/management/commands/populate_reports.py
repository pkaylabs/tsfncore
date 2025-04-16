import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apis.models import Report, School
from accounts.models import User
from core.utils.contants import MealType, ReportStatus


class Command(BaseCommand):
    help = 'Populate the database with random reports for each month'

    def handle(self, *args, **kwargs):
        schools = list(School.objects.all())
        users = list(User.objects.all())
        now = timezone.now()

        if not schools or not users:
            self.stdout.write(self.style.WARNING('No Schools Found... Creating some schools...'))
            # Create some schools if none exist
            names = ['School A', 'School B', 'School C', 'School D', 'School E']
            regions = ['Region 1', 'Region 2', 'Region 3', 'Region 4', 'Region 5']
            for i in range(len(names)):
                name = names[i]
                region = regions[i % len(regions)]
                sch = School.objects.create(
                    name=name,
                    region=region,
                    district='District ' + region,
                    town='Town ' + region,
                    phone=f'0{i}345678{i}{i+1}',
                    email=name.replace(" ", "").lower() + '@example.com',
                )
                schools.append(sch)
            self.stdout.write(self.style.SUCCESS(f'Successfully added {len(schools)} schools.'))

            for i in range(5):  # Create 5 users
                user = User.objects.create_user(
                    name=f'User {i+1}',
                    region=random.choice(regions),
                    district=f'District {random.choice(regions)}',
                    address=f'Address {i+1}',
                    phone=f'0{i}123456{i}{i+1}',
                    email=f'user{i+1}@examples.com',
                    password='password',  # Set a default password
                    is_staff=True,  # Set as staff for testing
                )
                users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Successfully added {len(users)} users.'))

        report_count = 0
        for month in range(1, 13):  # January to December
            for _ in range(random.randint(5, 15)):  # Random number of reports per month
                random_school = random.choice(schools)
                random_user = random.choice(users)

                # Random date in the target month
                random_day = random.randint(1, 28)  # To avoid date errors
                created_date = datetime(year=now.year, month=month, day=random_day, hour=random.randint(0, 23), minute=random.randint(0, 59))

                report = Report.objects.create(
                    school=random_school,
                    students_enrolled=random.randint(50, 500),
                    students_fed=random.randint(30, 500),
                    meal_type=random.choice([MealType.BREAKFAST.value, MealType.LUNCH.value]),
                    comments=random.choice(['', 'All went well', 'Minor delays', 'Food shortage reported']),
                    status=random.choice([ReportStatus.PENDING_REVIEW.value, ReportStatus.APPROVED.value]),
                    reported_by=random_user,
                    date_of_report=created_date.date(),
                    created_at=created_date,
                    updated_at=created_date,
                )
                report.created_at = created_date
                report.save()
                report_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully added {report_count} random reports across all months.'))

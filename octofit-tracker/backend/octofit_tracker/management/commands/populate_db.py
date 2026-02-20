
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'


    def handle(self, *args, **options):
        # Drop collections directly with pymongo for a clean slate
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        for col in ['activity', 'leaderboard', 'user', 'workout', 'team']:
            db[col].drop()

        # Create teams
        marvel = Team.objects.create(name='marvel', description='Marvel Team')
        dc = Team.objects.create(name='dc', description='DC Team')

        # Create users (pass Team instance)
        tony = User.objects.create(email='tony@stark.com', name='Tony Stark', team=marvel)
        steve = User.objects.create(email='steve@rogers.com', name='Steve Rogers', team=marvel)
        bruce = User.objects.create(email='bruce@wayne.com', name='Bruce Wayne', team=dc)
        clark = User.objects.create(email='clark@kent.com', name='Clark Kent', team=dc)

        # Create activities
        Activity.objects.create(user=tony, type='run', duration=30, date=timezone.now())
        Activity.objects.create(user=steve, type='cycle', duration=45, date=timezone.now())
        Activity.objects.create(user=bruce, type='swim', duration=60, date=timezone.now())
        Activity.objects.create(user=clark, type='run', duration=50, date=timezone.now())

        # Create workouts
        Workout.objects.create(name='Pushups', description='Do 20 pushups', suggested_for='marvel')
        Workout.objects.create(name='Situps', description='Do 30 situps', suggested_for='dc')

        # Create leaderboard
        Leaderboard.objects.create(team=marvel, points=150)
        Leaderboard.objects.create(team=dc, points=120)

        self.stdout.write(self.style.SUCCESS('Test data populated successfully!'))

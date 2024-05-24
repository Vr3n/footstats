from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = "Load the country and state fixture."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "directory", type=str,
            help="Directory consisting the fixture."
        )

    def handle(self, *args, **options):
        fixture_directory = options['directory']
        fixture_files = []

        for root, dirs, files in os.walk(fixture_directory):
            for file in files:
                if file.endswith('.json'):
                    fixture_files.append(os.path.join(root, file))

        if not fixture_files:
            self.stdout.write("No fixture files found.")
            return

        # Load fixtures one by one.
        for fixture_file in fixture_files:
            call_command('loaddata', fixture_file)
            self.stdout.write(self.style.SUCCESS(
                f'Loaded fixture file: {fixture_file}'))
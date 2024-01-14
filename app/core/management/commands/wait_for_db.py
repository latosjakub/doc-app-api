"""
Django Command to wait for database.
"""
import time
from psycopg2 import OperationalError as psyopg2OpError
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Db commands"""

    def handle(self, *args, **options):
        """Wait for db command."""
        self.stdout.write('Waiting for database...')
        db_up = False

        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except(psyopg2OpError, OperationalError):
                self.stdout.write('Database unavalible waiting 1 sec...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database avalible!'))

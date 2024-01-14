"""
Test for commands.
"""

from psycopg2 import OperationalError as psycopg2OpError
from django.db.utils import OperationalError
from unittest.mock import patch
from django.test import SimpleTestCase
from django.core.management import call_command


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTest(SimpleTestCase):
    """Test for custom commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Testing databse if reday."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_time, patched_check):
        """Testing database if ready."""
        patched_check.side_effect = [psycopg2OpError] * 2 + \
                                    [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])

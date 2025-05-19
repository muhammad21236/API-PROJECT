from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2OpError
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase
from django.db import connections


@patch.object(connections['default'], 'ensure_connection')
class CommandTests(TestCase):
    """Test cases for wait_for_db command."""

    databases = ['default']  # <-- Add this line to allow DB access

    def test_wait_for_db_ready(self, patched_ensure):
        """Test database available on first attempt."""
        patched_ensure.return_value = None
        call_command('wait_for_db')
        patched_ensure.assert_called_once()

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_ensure):
        """Test database connection retries."""
        # Raise errors on first 5 attempts, then succeed
        patched_ensure.side_effect = (
            [Psycopg2OpError] * 2 + [OperationalError] * 3 + [None]
        )
        call_command('wait_for_db')
        self.assertEqual(patched_ensure.call_count, 6)
        patched_ensure.assert_called_with()

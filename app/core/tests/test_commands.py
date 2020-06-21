# mocking django get db func
from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTest(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # gi = getitem
            # When we create management command
            # The way we check if our db is up, we test the connection
            # via the ConnectionHandler
            # The function that is actually called when
            # we get the db is __getitem__
            # This is how we mock the func
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)
    # Decorator

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        # Management command will be a while loop
        #   checking to see if OperationalError
        # If true it will wait a second and then try again
        # We will override this with the patch generator
        # So no delay, but will return a value of True to speed up tests
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # set side effect to func we are mocking
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)

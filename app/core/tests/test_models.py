"""
Test models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelsTests(TestCase):
    """Test Models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'tesuser@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@Example.com', 'test1@example.com'],
            ['TEST2@EXAMPLE.COM', 'TEST2@example.com'],
            ['test3@example.com', 'test3@example.com'],
        ]

        for sample, expection in sample_emails:
            user = get_user_model().objects.create_user(
                email=sample,
                password='testpass123',
            )
            self.assertEqual(user.email, expection)

    def test_raise_error_creating_user_without_email(self):
        """Test that creating user without email raises error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass123')

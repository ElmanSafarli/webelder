# from django.test import TestCase
# from django.contrib.auth.models import User
# from django.utils import timezone
# from .models import Organization

# class OrganizationModelTest(TestCase):

#     def setUp(self):
#         # Set up initial data for tests
#         self.organization = Organization.objects.create(
#             name="Test Organization",
#             domains="example.com test.com",
#             optional_info="Optional info for testing"
#         )
#         self.user = User.objects.create_user(username="testuser", email="user@example.com")

#     def test_organization_creation(self):
#         # Test if organization is created properly
#         self.assertEqual(self.organization.name, "Test Organization")
#         self.assertEqual(self.organization.domains, "example.com test.com")
#         self.assertEqual(self.organization.optional_info, "Optional info for testing")
#         self.assertTrue(isinstance(self.organization.created_date, timezone.datetime))

#     def test_add_user_by_email_success(self):
#         # Test if a user with a matching domain is added to the organization
#         email = "newuser@example.com"
#         user, created = self.organization.add_user_by_email(email)
#         self.assertIsNotNone(user)
#         self.assertTrue(created)
#         self.assertIn(user, self.organization.users.all())

#     def test_add_user_by_email_failure(self):
#         # Test if a user with a non-matching domain is not added to the organization
#         email = "newuser@nomatch.com"
#         user, created = self.organization.add_user_by_email(email)
#         self.assertIsNone(user)
#         self.assertFalse(created)

#     def test_str_method(self):
#         # Test the __str__ method
#         self.assertEqual(str(self.organization), "Test Organization")

#     def test_organization_verbose_names(self):
#         # Test the verbose names in the Meta class
#         self.assertEqual(self.organization._meta.verbose_name, 'Organization')
#         self.assertEqual(self.organization._meta.verbose_name_plural, 'Organizations')

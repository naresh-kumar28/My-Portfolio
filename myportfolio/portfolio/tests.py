from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Contact, Project, Skill, Certificate

class PageViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_public_pages_return_200(self):
        urls = ['home', 'about', 'contact', 'project', 'achievements']
        for url_name in urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200, f"URL '{url_name}' failed with status {response.status_code}")


class ContactFormTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')

    def test_valid_contact_submission(self):
        response = self.client.post(self.url, {
            'name': 'John Doe',
            'email': 'john@example.com',
            'contact': '9876543210',
            'message': 'Hello, I would like to hire you.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.count(), 1)
        c = Contact.objects.first()
        self.assertEqual(c.name, 'John Doe')
        self.assertEqual(c.email, 'john@example.com')

    def test_invalid_email_submission(self):
        response = self.client.post(self.url, {
            'name': 'Jane Doe',
            'email': 'not-an-email',
            'contact': '1234567890',
            'message': 'Testing bad email'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 0)

    def test_honeypot_spam_dropped(self):
        response = self.client.post(self.url, {
            'name': 'Spam Bot',
            'email': 'bot@spam.com',
            'contact': '0000000000',
            'message': 'Buy cheap items!',
            'website': 'http://spambot.xyz'  # honeypot filled
        })
        self.assertEqual(Contact.objects.count(), 0)


class AdminAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='adminuser',
            password='Password123!',
            is_staff=True
        )

    def test_anonymous_user_redirected_from_dashboard(self):
        response = self.client.get(reverse('admin'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_staff_user_can_access_dashboard(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('admin'))
        self.assertEqual(response.status_code, 200)

from django.test import TestCase, Client
from django.urls import reverse
from services.models import ServiceBooking, ServiceCategory, ServiceItem


class TechStyleSolutionsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category_web = ServiceCategory.objects.create(
            name="Web Solutions & Software", slug="web-solutions", description="Custom Web Apps"
        )
        self.category_cctv = ServiceCategory.objects.create(
            name="CCTV & Security Systems", slug="cctv-security", description="HD CCTV Kits"
        )
        self.service_web = ServiceItem.objects.create(
            category=self.category_web, title="Custom Web Application", slug="custom-web-application",
            description="Django & React App", starting_price=1500.00
        )

    def test_home_page_status(self):
        response = self.client.get(reverse('services:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TECHSTYLE")

    def test_services_page_status(self):
        response = self.client.get(reverse('services:services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Services Catalog")

    def test_cctv_page_status(self):
        response = self.client.get(reverse('services:cctv'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CCTV")

    def test_networking_page_status(self):
        response = self.client.get(reverse('services:networking'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Networking")

    def test_repairs_page_status(self):
        response = self.client.get(reverse('services:repairs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Repair")

    def test_portfolio_page_status(self):
        response = self.client.get(reverse('services:portfolio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Portfolio")

    def test_contact_page_status(self):
        response = self.client.get(reverse('services:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact")

    def test_create_booking_api(self):
        payload = {
            'customer_name': 'Test Client',
            'customer_phone': '0240001122',
            'customer_email': 'test@example.com',
            'service_type': 'Web Application Development',
            'details': 'Need Django portal built'
        }
        response = self.client.post(
            reverse('services:api_create_booking'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertTrue('TS-' in data['booking_ref'])

    def test_track_repair_api(self):
        booking = ServiceBooking.objects.create(
            customer_name="Alice",
            customer_phone="0241112233",
            service_type="CCTV Installation",
            details="8-Cam IP System",
            status="in_progress"
        )
        response = self.client.get(reverse('services:api_track_repair'), {'ref': booking.booking_ref})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['found'])
        self.assertEqual(data['booking_ref'], booking.booking_ref)

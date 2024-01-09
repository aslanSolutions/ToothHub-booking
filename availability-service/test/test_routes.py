from flask_testing import TestCase
from api import create_app
import json

class TestRoutes(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_pyfile('config.py')
        return app

    def test_set_availability_route(self):
        data = {
            "dentist_email": "dentist@test.com",
            "date": "2023-12-29",
            "time_slots": [
                {"start_time": "2023-12-29T09:30:00", "end_time": "2023-12-29T10:00:00", "booked": False},
                # Add more time slots as needed
            ]
        }

        response = self.client.post('/availability/', json=data)
        self.assertStatus(response, 201)
        self.assertIn('availability', json.loads(response.data))

    def test_get_availability_route(self):
        response = self.client.get('/availability/get_availability?dentist_email=dentist@test.com')
        self.assertStatus(response, 200)
        self.assertIn('availability', json.loads(response.data))

    def test_get_timeslots_route(self):
        response = self.client.get('/availability/get_timeslots?date=2023-12-29')
        self.assertStatus(response, 200)
        self.assertIn('available_slots', json.loads(response.data))

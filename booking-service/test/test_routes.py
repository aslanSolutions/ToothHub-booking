from flask_testing import TestCase
from unittest.mock import patch
from api import create_app
from bson import ObjectId

class TestAppointmentsRoutes(TestCase):
    # Class attribute to store the appointment ID
    appointment_id = None

    def create_app(self):
        app = create_app()
        app.config.from_pyfile('config.py')
        return app

    @patch('api.routes.times.publishMessage')
    @patch('api.routes.times.wait_for_acknowledgment', return_value=True)
    @patch('api.routes.times.insert_one')
    def test_create_appointment(self, mock_insert, mock_wait, mock_publish):
        data = {
            "dentist_email": "dentist@test.com",
            "patient_email": "patient@test.com",
            "appointment_datetime": "2023-12-29T09:30:00",
        }
    
        mock_insert.return_value.inserted_id = '60a7eb0452faff002206654b'
        self.appointment_id = mock_insert.return_value.inserted_id
    
        response = self.client.post('/appointments/', json=data)
    
        try:
            self.assertStatus(response, 404)  # Update to the correct status code if necessary
            self.assertEqual(response.json['message'], "The chosen date is not available anymore")
        except AssertionError:
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.data}")
            raise

        

    @patch('api.routes.times.find_one')
    def test_get_appointment(self, mock_find_one):
        # Use the class attribute for the appointment ID
        appointment_id = self.appointment_id

        mock_find_one.return_value = {"_id": appointment_id, "dentist_email": "dentist@test.com"}

        response = self.client.get(f'/appointments/{appointment_id}')
        self.assertStatus(response, 200)

    @patch('api.routes.times.publishMessage')
    @patch('api.routes.times.wait_for_acknowledgment', return_value=True)
    @patch('api.routes.times.find_one')
    @patch('api.routes.times.delete_one')
    def test_delete_appointment(self, mock_delete_one, mock_find_one, mock_wait, mock_publish):
        # Use the class attribute for the appointment ID
        appointment_id = self.appointment_id

        mock_find_one.return_value = {"_id": appointment_id, "dentist_email": "dentist@test.com"}
        mock_delete_one.return_value.deleted_count = 1

        response = self.client.delete(f'/appointments/{appointment_id}')
        self.assertStatus(response, 200)

    @patch('api.routes.times.publishMessage')
    @patch('api.routes.times.wait_for_acknowledgment', return_value=True)
    @patch('api.routes.times.update_one')
    @patch('bson.ObjectId', return_value=ObjectId())  # Mock ObjectId
    def test_update_appointment(self, mock_update_one, mock_wait, mock_publish, mock_object_id):
        # Use the class attribute for the appointment ID
        appointment_id = self.appointment_id

        data = {
            "dentist_email": "new_dentist@test.com",
            "patient_email": "patient@test.com",
            "appointment_datetime": "2024-01-05T10:00:00",
        }

        mock_update_one.return_value.matched_count = 1

        with patch('bson.ObjectId', return_value=ObjectId()):  # Patch ObjectId in the context
            response = self.client.patch(f'/appointments/{appointment_id}', json=data)

        try:
            self.assertStatus(response, 200)  # Update to the correct status code if necessary
        except AssertionError:
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.data}")
            raise

    @patch('api.routes.times.find')
    def test_get_all_appointments(self, mock_find):
        mock_find.return_value = [{"_id": "1", "dentist_email": "dentist@test.com"},
                                  {"_id": "2", "dentist_email": "another_dentist@test.com"}]

        response = self.client.get('/appointments/')
        self.assertStatus(response, 200)

if __name__ == '__main__':
    unittest.main()

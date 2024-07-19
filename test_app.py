import os
from unittest import TestCase
from models import db, User, Exercise, Workout, WorkoutExercise
from app import app

# Set up environment variable to use a different database for tests
os.environ['DATABASE_URL'] = "postgresql:///workout-test"

# Create our tables once for all tests
db.create_all()


class AppRoutesTestCase(TestCase):
    """Test routes for the application."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.user_data = {
            'username': 'testuser',
            'password': 'testpass',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.register_user()

    def tearDown(self):
        """Clean up fouled transactions."""
        res = super().tearDown()
        db.session.rollback()
        return res

    def register_user(self):
        """Helper method to register a user."""
        u = User.signup(
            username=self.user_data['username'],
            password=self.user_data['password'],
            email=self.user_data['email'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name']
        )
        db.session.commit()
        self.user = u

    def login_user(self):
        """Helper method to log in a user."""
        return self.client.post('/login', data={
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })

    def test_register(self):
        """Test user registration."""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'password': 'newpass',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Successfully Created Your Account!', response.data)

    def test_login(self):
        """Test user login."""
        response = self.login_user()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back', response.data)

    def test_home(self):
        """Test home page access."""
        self.login_user()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Please log in or sign up.', response.data)

    def test_show_exercises(self):
        """Test showing exercises."""
        self.login_user()
        response = self.client.get('/exercises')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Exercises', response.data)

    def test_save_workout(self):
        """Test saving a workout."""
        self.login_user()

        # Add an exercise to the database for the workout
        exercise = Exercise(name='Push-up', type='strength', muscle='chest', difficulty='easy', instructions='Do push-ups')
        db.session.add(exercise)
        db.session.commit()

        workout_data = {
            'name': 'Test Workout',
            'exercises': [{'exerciseId': exercise.id, 'sets': 3, 'reps': 10}]
        }
        response = self.client.post('/workouts/save_workout', json=workout_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Workout saved successfully')


if __name__ == "__main__":
    import unittest
    unittest.main()

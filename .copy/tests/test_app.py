import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        """Create a test client and set up the testing environment."""
        self.app = app.test_client()
        self.app.testing = True

    def test_create_account_route(self):
        """Test the create account route with various inputs."""
        # Test with valid data
        response = self.app.post('/create_account', data=dict(
            name='Test User',
            username='testuser',
            password='password123',
            balance=1000
        ))
        self.assertEqual(response.status_code, 302)  # Expecting redirect after successful account creation

        # Test with missing required fields
        response = self.app.post('/create_account', data=dict(
            name='Test User'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid form data', response.data)

        # Add more tests if necessary (e.g., invalid data formats)

    def test_login_route(self):
        """Test the login route with valid and invalid credentials."""
        # Test with valid credentials
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='password123'
        ), follow_redirects=True)  # follow_redirects=True to follow the redirect after successful login
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account Details', response.data)

        # Test with invalid credentials
        response = self.app.post('/login', data=dict(
            username='invaliduser',
            password='invalidpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid credentials', response.data)

    def test_withdraw_money_route(self):
        """Test the withdraw money route with valid and invalid data."""
        # Test with valid data
        response = self.app.post('/withdraw_money/1', data=dict(
            amount=100
        ), follow_redirects=True)  # Follow redirect to check result after withdrawal
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Withdrawal successful', response.data)

        # Test with invalid data (e.g., insufficient balance)
        response = self.app.post('/withdraw_money/1', data=dict(
            amount=999999
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Insufficient funds', response.data)

    def test_deposit_money_route(self):
        """Test the deposit money route."""
        # Test with valid data
        response = self.app.post('/deposit_money/1', data=dict(
            amount=100
        ), follow_redirects=True)  # Follow redirect to check result after deposit
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Deposit successful', response.data)

        # Add more tests if necessary (e.g., invalid data formats)

    def test_send_money_route(self):
        """Test the send money route with valid and invalid data."""
        # Test with valid data
        response = self.app.post('/send_money/1', data=dict(
            recipient_id=2,
            amount=100
        ), follow_redirects=True)  # Follow redirect to check result after sending money
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Transfer successful', response.data)

        # Test with invalid data (e.g., insufficient balance)
        response = self.app.post('/send_money/1', data=dict(
            recipient_id=2,
            amount=999999
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Insufficient funds', response.data)

    def test_account_route(self):
        """Test the account route with valid and invalid account IDs."""
        # Test with a valid account ID
        response = self.app.get('/account/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account Details', response.data)

        # Test with an invalid account ID
        response = self.app.get('/account/999999')
        self.assertEqual(response.status_code, 404)

    # Add more test cases for other routes as needed

if __name__ == '__main__':
    unittest.main()

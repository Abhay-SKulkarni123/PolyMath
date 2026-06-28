import pytest
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from faker import Faker

fake = Faker()


class UserRegistrationTests(APITestCase):
    """Test user registration flow"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.valid_data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'password': 'TestPass123!',
            'confirm_password': 'TestPass123!'
        }
    
    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['error'])
        self.assertEqual(response.data['message'], 'User registered successfully')
    
    def test_user_registration_password_mismatch(self):
        """Test registration fails with mismatched passwords"""
        data = self.valid_data.copy()
        data['confirm_password'] = 'DifferentPass123!'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['error'])
    
    def test_user_registration_duplicate_email(self):
        """Test registration fails with duplicate email"""
        # Create first user
        self.client.post(self.register_url, self.valid_data, format='json')
        
        # Try to create second user with same email
        response = self.client.post(self.register_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['error'])
    
    def test_user_registration_weak_password(self):
        """Test registration fails with weak password"""
        data = self.valid_data.copy()
        data['password'] = 'weak'
        data['confirm_password'] = 'weak'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['error'])
    
    def test_user_registration_invalid_email(self):
        """Test registration fails with invalid email"""
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['error'])


class UserLoginTests(APITestCase):
    """Test user login flow"""
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        # Create a test user
        from users.models import User
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )
    
    def test_login_success(self):
        """Test successful login returns tokens"""
        data = {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['error'])
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
        self.assertIn('user', response.data)
    
    def test_login_wrong_password(self):
        """Test login fails with wrong password"""
        data = {
            'email': 'test@example.com',
            'password': 'WrongPass123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response.data['error'])
    
    def test_login_nonexistent_user(self):
        """Test login fails with non-existent email"""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response.data['error'])


class UserProfileTests(APITestCase):
    """Test authenticated user endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        # Create and login user
        from users.models import User
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )
        
        # Get tokens
        login_url = reverse('login')
        login_data = {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        self.access_token = login_response.data['tokens']['access']
        
        # Set auth header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    def test_get_profile_authenticated(self):
        """Test getting user profile when authenticated"""
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['error'])
        self.assertEqual(response.data['user']['email'], 'test@example.com')
    
    def test_get_profile_unauthenticated(self):
        """Test getting user profile without auth fails"""
        self.client.credentials()  # Remove auth
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class JWTTokenTests(APITestCase):
    """Test JWT token operations"""
    
    def setUp(self):
        self.client = APIClient()
        from users.models import User
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )
    
    def test_access_token_works(self):
        """Test access token can be used to access protected endpoint"""
        # Get tokens
        login_url = reverse('login')
        login_data = {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        access_token = login_response.data['tokens']['access']
        
        # Use access token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_refresh_token_rotation(self):
        """Test refresh token rotation works"""
        # Get initial tokens
        login_url = reverse('login')
        login_data = {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        refresh_token = login_response.data['tokens']['refresh']
        
        # Use refresh token
        refresh_url = reverse('token_refresh')
        response = self.client.post(refresh_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
        # Old refresh token should be blacklisted
        response2 = self.client.post(refresh_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)
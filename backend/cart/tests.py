import pytest
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from faker import Faker
from users.models import User
from products.models import Product

fake = Faker()


class CartTests(APITestCase):
    """Test cart operations"""
    
    def setUp(self):
        self.client = APIClient()
        # Create and login user
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
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Create test product
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=29.99,
            stock=10,
            type='physical',
            is_active=True,
            vendor_name='Test Vendor'
        )
    
    def test_get_empty_cart(self):
        """Test getting empty cart"""
        url = reverse('cart-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['error'])
        self.assertEqual(len(response.data['items']), 0)
    
    def test_add_item_to_cart(self):
        """Test adding item to cart"""
        url = reverse('cart-add-item')
        data = {
            'product_id': self.product.id,
            'quantity': 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['error'])
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['quantity'], 2)
    
    def test_add_item_unauthorized(self):
        """Test adding item without auth fails"""
        self.client.credentials()  # Remove auth
        url = reverse('cart-add-item')
        data = {
            'product_id': self.product.id,
            'quantity': 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_add_item_invalid_quantity(self):
        """Test adding item with invalid quantity fails"""
        url = reverse('cart-add-item')
        data = {
            'product_id': self.product.id,
            'quantity': 0  # Invalid
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_add_item_exceeds_stock(self):
        """Test adding item exceeding stock fails"""
        url = reverse('cart-add-item')
        data = {
            'product_id': self.product.id,
            'quantity': 100  # Exceeds stock of 10
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_remove_item_from_cart(self):
        """Test removing item from cart"""
        # First add item
        add_url = reverse('cart-add-item')
        self.client.post(add_url, {
            'product_id': self.product.id,
            'quantity': 1
        }, format='json')
        
        # Then remove it
        remove_url = reverse('cart-remove-item')
        response = self.client.delete(remove_url, {
            'product_id': self.product.id
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['error'])
        self.assertEqual(len(response.data['items']), 0)
    
    def test_update_cart_item_quantity(self):
        """Test updating cart item quantity"""
        # First add item
        add_url = reverse('cart-add-item')
        self.client.post(add_url, {
            'product_id': self.product.id,
            'quantity': 1
        }, format='json')
        
        # Update quantity
        update_url = reverse('cart-update-item')
        response = self.client.put(update_url, {
            'product_id': self.product.id,
            'quantity': 5
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['error'])
        self.assertEqual(response.data['items'][0]['quantity'], 5)
    
    def test_clear_cart(self):
        """Test clearing entire cart"""
        # Add multiple items
        add_url = reverse('cart-add-item')
        self.client.post(add_url, {
            'product_id': self.product.id,
            'quantity': 2
        }, format='json')
        
        # Clear cart
        clear_url = reverse('cart-clear')
        response = self.client.delete(clear_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['error'])
        self.assertEqual(len(response.data['items']), 0)
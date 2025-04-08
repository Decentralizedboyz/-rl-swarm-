import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8000"

def register_user():
    """Register a test user"""
    url = f"{BASE_URL}/users/register"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    response = requests.post(url, params=data)
    print("Register User Response:", response.json())
    return response.json()

def login():
    """Login and get access token"""
    url = f"{BASE_URL}/token"
    data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    response = requests.post(url, data=data)
    print("Login Response:", response.json())
    return response.json()["access_token"]

def get_user_info(token):
    """Get user information"""
    url = f"{BASE_URL}/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print("User Info Response:", response.json())
    return response.json()

def create_investment(token, plan_name, amount):
    """Create a test investment"""
    url = f"{BASE_URL}/investments"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "plan_name": plan_name,
        "amount": amount
    }
    response = requests.post(url, headers=headers, params=data)
    print(f"Create Investment Response ({plan_name}):", response.json())
    return response.json()

def create_payment(token, amount, payment_method):
    """Create a test payment"""
    url = f"{BASE_URL}/payments"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "amount": amount,
        "payment_method": payment_method
    }
    response = requests.post(url, headers=headers, params=data)
    print(f"Create Payment Response ({payment_method}):", response.json())
    return response.json()

def get_investments(token):
    """Get all investments"""
    url = f"{BASE_URL}/investments"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print("Get Investments Response:", response.json())
    return response.json()

def get_payments(token):
    """Get all payments"""
    url = f"{BASE_URL}/payments"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print("Get Payments Response:", response.json())
    return response.json()

def main():
    print("Starting Dashboard Test...")
    
    # Register a new user
    register_user()
    
    # Login and get token
    token = login()
    
    # Get user info
    user_info = get_user_info(token)
    
    # Create some investments
    investments = [
        ("Basic Plan", 1000),
        ("Premium Plan", 5000),
        ("VIP Plan", 10000)
    ]
    
    for plan_name, amount in investments:
        create_investment(token, plan_name, amount)
    
    # Create some payments
    payments = [
        (1000, "BTC"),
        (5000, "USDT"),
        (10000, "ETH")
    ]
    
    for amount, method in payments:
        create_payment(token, amount, method)
    
    # Get all investments and payments
    all_investments = get_investments(token)
    all_payments = get_payments(token)
    
    print("\nDashboard Test Complete!")
    print("\nSummary:")
    print(f"User: {user_info['username']}")
    print(f"Balance: ${user_info['balance']}")
    print(f"Total Earnings: ${user_info['total_earnings']}")
    print(f"Total Investments: {len(all_investments)}")
    print(f"Total Payments: {len(all_payments)}")

if __name__ == "__main__":
    main() 
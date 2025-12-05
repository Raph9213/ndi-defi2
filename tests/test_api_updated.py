import os
import time
import requests

BASE = os.getenv('API_URL', 'http://127.0.0.1:5000')

def test_register_and_authenticate():
    # Register a new user
    email = f"testuser.{int(time.time()*1000)}@example.com"
    r = requests.post(f"{BASE}/register", json={'name': 'TestUser', 'email': email, 'password': 'password'})
    assert r.status_code == 201

    # Authenticate the user
    auth = (email, 'password')
    r = requests.get(f"{BASE}/users", auth=auth)
    assert r.status_code == 200

def test_add_user_to_team():
    # Register and authenticate admin
    admin_email = f"admin.{int(time.time()*1000)}@example.com"
    requests.post(f"{BASE}/register", json={'name': 'Admin', 'email': admin_email, 'password': 'password'})
    auth = (admin_email, 'password')

    # Add a new user to the team
    user_email = f"user.{int(time.time()*1000)}@example.com"
    r = requests.post(f"{BASE}/add-user", json={'name': 'User', 'email': user_email}, auth=auth)
    assert r.status_code == 201

def test_list_missions():
    # Register and authenticate user
    email = f"testuser.{int(time.time()*1000)}@example.com"
    requests.post(f"{BASE}/register", json={'name': 'TestUser', 'email': email, 'password': 'password'})
    auth = (email, 'password')

    # List missions
    r = requests.get(f"{BASE}/missions", auth=auth)
    assert r.status_code == 200
    missions = r.json()
    assert len(missions) > 0

def test_complete_mission():
    # Register and authenticate user
    email = f"testuser.{int(time.time()*1000)}@example.com"
    requests.post(f"{BASE}/register", json={'name': 'TestUser', 'email': email, 'password': 'password'})
    auth = (email, 'password')

    # Complete a mission
    r = requests.post(f"{BASE}/missions/1/complete", auth=auth)
    assert r.status_code == 200
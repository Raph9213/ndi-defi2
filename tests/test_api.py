import os
import time
import requests


BASE = os.getenv('API_URL', 'http://127.0.0.1:5000')


def unique_email():
    return f"test.{int(time.time()*1000)}@example.com"


def test_create_user_team_point_sequence():
    # create a user
    r = requests.post(f"{BASE}/users", json={'name': 'TestUser', 'email': unique_email()})
    assert r.status_code in (200, 201)
    user = r.json()
    assert 'id' in user

    # create a team with owner
    r = requests.post(f"{BASE}/teams", json={'name': 'TestTeam', 'owner_id': user['id']})
    assert r.status_code in (200, 201)
    team = r.json()
    assert 'id' in team

    # create a point for the user
    r = requests.post(f"{BASE}/points", json={'title': 'testpoint', 'value': 10, 'user_id': user['id'], 'team_id': team['id']})
    assert r.status_code in (200, 201)
    point = r.json()
    assert point.get('title') == 'testpoint'

    # list points and check presence
    r = requests.get(f"{BASE}/points", params={'user_id': user['id']})
    assert r.status_code == 200
    pts = r.json()
    assert any(p.get('id') == point.get('id') for p in pts)


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


if __name__ == "__main__":
    test_register_and_authenticate()
    test_add_user_to_team()
    test_list_missions()
    test_complete_mission()

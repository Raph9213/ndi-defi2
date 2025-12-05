from app import app, db, User

with app.app_context():
    # Reset DB for smoke test (development only)
    db.drop_all()
    db.create_all()
    client = app.test_client()
    # cleanup
    u = User.query.filter_by(name='TestUser').first()
    if u:
        db.session.delete(u)
        db.session.commit()

    # create tribe
    res = client.post('/api/tribe/create', json={'owner_name':'TestUser','name':'Testers'})
    print('create status', res.status_code, res.get_json())

    # join with another user
    res2 = client.post('/api/tribe/join', json={'invite': res.get_json()['inviteLink'], 'user_name':'NewMember'})
    print('join status', res2.status_code, res2.get_json())

    # fetch user by name
    res3 = client.get('/api/user/name/TestUser')
    print('get user', res3.status_code, res3.get_json())

    # fetch tribe
    res4 = client.get(f"/api/tribe/{res.get_json()['inviteLink']}")
    print('get tribe', res4.status_code, res4.get_json())

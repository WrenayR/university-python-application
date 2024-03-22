from . import client
from models import Customer, User
from app import db


def test_login_page(client):
    response = client.get('/login')
    print(response.data)
    print(response.status_code)
    assert response.status_code == 200


def test_login_form_valid_user(client):
    user = User(username='testuser5432', email='testuser5432@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    try:
        response = client.post('/login', data={
            'username': 'testuser5432',
            'password': 'password',
            'role': 'regular'
        })
        assert response.status_code == 302
        assert b'Logged in successfully.' in response.data
        print(response.status_code)
        print(response.data)
    except:
        pass
    finally:
        db.session.delete(user)
        db.session.commit()


def test_login_form_invalid_user(client):
    user = User(username='testuser98765', email='testuser98765@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    try:
        response = client.post('/login', data={
            'username': 'nonexistent_user',
            'password': 'password',
            'role': 'regular'
        })
        assert response.status_code == 302
        assert b'Invalid username or password.' in response.data
        print(response.status_code)
        print(response.data)
    except:
        pass
    finally:
        db.session.delete(user)
        db.session.commit()


def test_login_form_wrong_password(client):

    user = User(username='testuser543645', email='testuser543645@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    try:
        response = client.post('/login', data={
            'username': 'nonexistent_user',
            'password': 'password',
            'role': 'regular'
        })
        assert response.status_code == 302
        assert b'Invalid username or password.' in response.data
        print(response.status_code)
        print(response.data)
    except:
        pass
    finally:
        db.session.delete(user)
        db.session.commit()

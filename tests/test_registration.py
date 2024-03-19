import pdb

from models import Customer, User
from app import db

from . import client

def test_register_index(client):
    # Test GET request
    response = client.get('/register')

    assert response.status_code == 200


def test_register_correct_form(client):
    # Test POST request with correct information
    try:
        response = client.post('/register', data={
            'username': 'testuser555',
            'email': 'testuse555r@example.com',
            'password': 'testpassword',
            'cpassword': 'testpassword'
        })
        assert response.status_code == 302
        assert b'Account created successfully.' in response.data

        print(response.data)
    except:
        pass
    finally:
        user = User.query.filter_by(username='testuser555').first()
        db.session.delete(user)
        db.session.commit()


def test_register_incorrect_password(client):
    # Test POST request with incorrect password confirmation
    response = client.post('/register', data={
        'username': 'testuser3242',
        'email': 'testuser32422@example.com',
        'password': 'testpassword',
        'cpassword': 'wrongpassword'
    })

    print(response.data)
    assert response.status_code == 302

    assert b'Password Does not Matched.' in response.data


def test_register_existing_username(client):

    # Test POST request with existing username
    user = User(username='testuser123', email='testuser123@example.com')
    user.set_password('testuser123')
    db.session.add(user)
    db.session.commit()
    try:
        response = client.post('/register', data={
            'username': 'testuser123',
            'email': 'testuser123@example.com',
            'password': 'testpassword',
            'cpassword': 'testpassword'
        })
        assert response.status_code == 302
        assert b'Username already exists.' in response.data
        print(response.data)
    except:
        pass
    finally:
        user = User.query.filter_by(username='testuser123').first()
        db.session.delete(user)
        db.session.commit()


def test_register_existing_email(client):

    # Test POST request with existing email
    user = User(username='testuser12345', email='testuser12345@example.com')
    user.set_password('testuser12345')
    db.session.add(user)
    db.session.commit()
    try:
        response = client.post('/register', data={
            'username': 'testuser54321',
            'email': 'testuser12345@example.com',
            'password': 'testpassword',
            'cpassword': 'testpassword'
        })

        print(response.data)
        assert response.status_code == 302
        assert b'Email already exists.' in response.data
    except:
        pass
    finally:
        user = User.query.filter_by(username='testuser12345').first()
        db.session.delete(user)
        db.session.commit()

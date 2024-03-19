import pdb

from flask_login import login_user, logout_user

from . import client
from models import Customer, User
from app import db



def test_add_customer(client):

    user = User(username='testuser4343', email='testemail4343@example.com')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    client.post('/login', data={
        'username': 'testuser4343',
        'password': 'testpassword',
        'role': 'regular',
    })

    # Given
    form_data = {
        'fname': 'John',
        'lname': 'Doe',
        'email': 'john.doe@example.com',
        'account': 1234567890,
        'balance': 1000,
        'scode': 123456,
    }

    # When
    response = client.post('/add-customer', data=form_data)

    # Then
    assert response.status_code == 302
    assert response.data == b'Customer Added'

    # with app.app_context():
    # Query the database for the customer
    customer = Customer.query.filter_by(first_name='John', last_name='Doe').first()
    assert customer is not None
    assert customer.email == 'john.doe@example.com'
    assert customer.account_number == 1234567890
    assert customer.balance == 1000
    assert customer.sort_code == 123456
    # assert customer.user_id == 1  # assuming the user is logged in as the first user in the database
    db.session.delete(user)
    db.session.delete(customer)
    db.session.commit()

    client.get('/logout')

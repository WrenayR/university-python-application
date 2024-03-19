import pdb

from flask_login import login_user, logout_user

from . import client
from models import Customer, User
from app import db



def test_delete_customer(client):
    admin = User(username='testuser1122', email='testuser1122@example.com', role='admin')
    admin.set_password('testpassword')
    db.session.add(admin)
    db.session.commit()

    client.post('/login', data={
        'username': 'testuser1122',
        'password': 'testpassword',
        'role': 'regular',
    })

    # Given
    form_data = {
        'fname': 'testcustomer',
        'lname': 'testcustomer',
        'email': 'testcustomer@example.com',
        'account': 1234567890,
        'balance': 1000,
        'scode': 123456,
    }
    client.post('/add-customer', data=form_data)
    customer = Customer.query.filter_by(email='testcustomer@example.com').first()



    response = client.get(f'/delete-customer/{customer.id}')
    # Then
    assert response.status_code == 302
    assert response.data == b'Customer Deleted'

    db.session.delete(admin)
    db.session.commit()

    client.get('/logout')

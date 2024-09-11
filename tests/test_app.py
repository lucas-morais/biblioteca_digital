from http import HTTPStatus

from fastapi.testclient import TestClient

from biblioteca_digital.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user():
    client = TestClient(app)

    response = client.post(
        '/users',
        json={
            'username': 'ringo',
            'email': 'ringo@email.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'ringo',
        'email': 'ringo@email.com',
        'id': 1,
    }

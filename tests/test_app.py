from http import HTTPStatus

from biblioteca_digital.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
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


def test_should_return_an_error_if_username_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'test@email.com',
            'password': 'testSecret',
        },
    )

    response.status_code = HTTPStatus.BAD_REQUEST
    response.json = {'detail': 'Username already exists'}


def test_should_return_an_error_if_email_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste 2',
            'email': 'teste@teste.com',
            'password': 'testSecret',
        },
    )

    response.status_code = HTTPStatus.BAD_REQUEST
    response.json = {'detail': 'Email already exists'}


def test_read_users(client, user):
    db_user = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [db_user]}


def test_read_user(client, user):
    db_user = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')

    response.status_code == HTTPStatus.OK
    response.json() == db_user


def test_get_when_user_does_not_exist(client):
    response = client.get('/users/55')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'george',
            'email': 'george@email.com',
            'password': 'new secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'email': 'george@email.com',
        'username': 'george',
        'id': 1,
    }


def test_update_when_user_does_not_exist(client):
    response = client.put(
        '/users/55',
        json={
            'username': 'some name',
            'email': 'email@email.com',
            'password': 'super new secret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_when_user_does_not_exist(client):
    response = client.delete('/users/55')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token

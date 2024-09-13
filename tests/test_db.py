from sqlalchemy import select

from biblioteca_digital.models import User


def test_create_user(session):
    new_user = User(
        username='ringo', password='secret', email='test@email.com'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'ringo'))

    assert user.username == 'ringo'

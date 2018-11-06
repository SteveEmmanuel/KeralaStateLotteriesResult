from getpass import getpass
import sys

from flask import current_app
from app import app, bcrypt, db
from db_creator import User

def main():
    """Main entry point for script."""
    with app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.all():
            print('A user already exists! Create another? (y/n):')
            create = input()
            if create == 'n':
                return

        print('Enter user id: ')
        user_id = input()
        password = getpass()
        assert password == getpass('Password (again):')

        user = User(
            user_id=user_id,
            password=bcrypt.generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print('User added.')


if __name__ == '__main__':
    sys.exit(main())
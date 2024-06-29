from .models import Word, User, JustFlipped, Failure
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class WordsController:
    @staticmethod
    def get_all_words():
        return Word.query.all()

    @staticmethod
    def get_word_by_id(word_id):
        return Word.query.get_or_404(word_id)

    @staticmethod
    def add_word(data):
        new_word = Word(Italian=data['Italian'], English=data['English'])
        db.session.add(new_word)
        db.session.commit()
        return new_word

    @staticmethod
    def update_word(word_id, data):
        word = WordsController.get_word_by_id(word_id)
        word.Italian = data['Italian']
        word.English = data['English']
        db.session.commit()
        return word

    @staticmethod
    def delete_word(word_id):
        word = WordsController.get_word_by_id(word_id)
        db.session.delete(word)
        db.session.commit()
        return word

class UsersController:
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get_or_404(user_id)

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def add_user(data):
        new_user = User(username=data['username'], password=generate_password_hash(data['password']), role=data['role'])
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_user(user):
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = UsersController.get_user_by_id(user_id)
        db.session.delete(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate_user(username, password):
        user = UsersController.get_user_by_username(username)
        if user and check_password_hash(user.password, password):
            user.last_login = datetime.now()
            UsersController.update_user(user)
        
            return user
        return None

class JustFlippedController:
    @staticmethod
    def get_all_just_flipped():
        return JustFlipped.query.all()

    @staticmethod
    def get_just_flipped_by_user(user_id):
        return JustFlipped.query.filter_by(user_id=user_id).all()

    @staticmethod
    def add_just_flipped(italian, english, user_id, language_direction):
        new_just_flipped = JustFlipped(
            italian=italian,
            english=english,
            user_id=user_id,
            language_direction=language_direction
        )
        db.session.add(new_just_flipped)
        db.session.commit()
        return new_just_flipped

    @staticmethod
    def delete_just_flipped(just_flipped_id):
        just_flipped = JustFlipped.query.get(just_flipped_id)
        db.session.delete(just_flipped)
        db.session.commit()
        return just_flipped


class FailureController:
    @staticmethod
    def get_all_failures():
        return Failure.query.all()

    @staticmethod
    def get_failures_by_user(user_id):
        return Failure.query.filter_by(user_id=user_id).all()

    @staticmethod
    def add_failure(italian, english, user_id, language_direction):
        new_failure = Failure(
            italian=italian,
            english=english,
            user_id=user_id,
            language_direction=language_direction
        )
        db.session.add(new_failure)
        db.session.commit()
        return new_failure

    @staticmethod
    def delete_failure(failure_id):
        failure = Failure.query.get(failure_id)
        db.session.delete(failure)
        db.session.commit()
        return failure

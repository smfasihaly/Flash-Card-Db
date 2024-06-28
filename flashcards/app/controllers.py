from .models import Word, User, JustFlipped, Failure
from . import db

def get_all_words():
    return Word.query.all()

def get_word_by_id(word_id):
    return Word.query.get_or_404(word_id)

def add_word(data):
    new_word = Word(Italian=data['Italian'], English=data['English'])
    db.session.add(new_word)
    db.session.commit()
    return new_word

def update_word(word_id, data):
    word = get_word_by_id(word_id)
    word.Italian = data['Italian']
    word.English = data['English']
    db.session.commit()
    return word

def delete_word(word_id):
    word = get_word_by_id(word_id)
    db.session.delete(word)
    db.session.commit()
    return word

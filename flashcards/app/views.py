from flask import render_template, jsonify, request, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

import random
from .models import db, Word, User, JustFlipped, Failure
from .controllers import *

main = Blueprint('main', __name__)
words_list = []
@main.route('/')
def index():
    global words_list
    user_logged_in = 'user' in session
    username = session['user'] if user_logged_in else ''
    words_list = WordsController.get_all_words()
    random.shuffle(words_list)
    return render_template('index.html', user_logged_in=user_logged_in, username=username)

@main.route('/get_verbs')
def get_verbs():
    if 'user' not in session:
        return jsonify({"error": "User not logged in", "data": []}), 401  # 401 Unauthorized

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 9))        

    total_words = len(words_list)
    total_pages = (total_words + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page

    paginated_words = words_list[start:end]

    response_data = {
        'verbs': [{'Italian': word.italian, 'English': word.english} for word in paginated_words],
        'total_pages': total_pages,
        'current_page': page
    }
    return jsonify(response_data)

@main.route('/get_verbs/<sheet_name>')
def get_verbs_from_sheet(sheet_name):
    if 'user' not in session:
        return jsonify({"error": "User not logged in"}), 401

    username = session['user']
    user = UsersController.get_user_by_username(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    language_direction = request.args.get('language_direction')
    is_random = request.args.get('isRandom', 'true') == 'true'
    
    if sheet_name == 'JustFlipped':
        query = JustFlipped.query.filter_by(user_id=user.id, language_direction=language_direction)
    elif sheet_name == 'Failure':
        query = Failure.query.filter_by(user_id=user.id, language_direction=language_direction)
    else:
        return jsonify({"error": "Invalid sheet name"}), 400
    
    sheet_data = query.all()
    if is_random and sheet_data:
        random.shuffle(sheet_data)

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 9))
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(sheet_data) + per_page - 1) // per_page

    response_data = {
        'verbs': [{'Italian': word.italian, 'English': word.english} for word in sheet_data[start:end]],
        'total_pages': total_pages,
        'current_page': page
    }
    return jsonify(response_data)

@main.route('/save_stats', methods=['POST'])
def save_stats():
    stats_data = request.json
    just_flipped = stats_data.get('justFlipped', [])
    failure = stats_data.get('failure', [])
    language_direction = stats_data.get('languageDirection')
    username = session['user']
    user = UsersController.get_user_by_username(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    for verb in just_flipped:
        JustFlippedController.add_just_flipped(verb['Italian'], verb['English'], user.id, language_direction)
  

    for verb in failure:
        FailureController.add_failure(verb['Italian'], verb['English'], user.id, language_direction)
  
    return jsonify({"status": "success"})

@main.route('/signup', methods=['POST'])
def signup():
    user_data = request.json
    username = user_data.get('username')
    password = user_data.get('password')

    if UsersController.get_user_by_username(username):
        return jsonify({"error": "Username already exists"}), 400

    new_user = UsersController.add_user({
        'username': username,
        'password': password,
        'role': 'user'
    })

    return jsonify({"status": "success"})

@main.route('/login', methods=['POST'])
def login():
    user_data = request.json
    username = user_data.get('username')
    password = user_data.get('password')

    user = UsersController.authenticate_user(username, password)
    if user:
        session['user'] = username  # Set session for the logged-in user
        return jsonify({"status": "success"})
    else:
        return jsonify({"error": "Invalid username or password"}), 400

@main.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear the session
    return jsonify({"status": "success"})

@main.route('/remove_verb', methods=['POST'])
def remove_verb():
    data = request.json
    verb = data['verb']
    sheet_name = data['sheetName']
    username = session['user']
    user = UsersController.get_user_by_username(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if sheet_name == 'JustFlipped':
        JustFlipped.query.filter_by(italian=verb['Italian'], english=verb['English'], user_id=user.id).delete()
    elif sheet_name == 'Failure':
        Failure.query.filter_by(italian=verb['Italian'], english=verb['English'], user_id=user.id).delete()
    else:
        return jsonify({"error": "Invalid sheet name"}), 400

    db.session.commit()
    return jsonify({"status": "success"})

from flask import render_template, jsonify, request, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
from .models import db, Word, User, JustFlipped, Failure

main = Blueprint('main', __name__)

@main.route('/')
def index():
    user_logged_in = 'user' in session
    username = session['user'] if user_logged_in else ''
    return render_template('index.html', user_logged_in=user_logged_in, username=username)

@main.route('/get_verbs')
def get_verbs():
    if 'user' not in session:
        return jsonify({"error": "User not logged in", "data": []}), 401  # 401 Unauthorized

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 9))
    words = Word.query.paginate(page=page, per_page=per_page, error_out=False)
    total_pages = words.pages

    response_data = {
        'verbs': [{'Italian': word.italian, 'English': word.english} for word in words.items],
        'total_pages': total_pages,
        'current_page': page
    }
    return jsonify(response_data)

@main.route('/get_verbs/<sheet_name>')
def get_verbs_from_sheet(sheet_name):
    if 'user' not in session:
        return jsonify({"error": "User not logged in"}), 401

    username = session['user']
    user = User.query.filter_by(username=username).first()
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
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    for item in just_flipped:
        if not JustFlipped.query.filter_by(italian=item['Italian'], english=item['English'], user_id=user.id, language_direction=language_direction).first():
            new_just_flipped = JustFlipped(italian=item['Italian'], english=item['English'], user_id=user.id, language_direction=language_direction)
            db.session.add(new_just_flipped)

    for item in failure:
        if not Failure.query.filter_by(italian=item['Italian'], english=item['English'], user_id=user.id, language_direction=language_direction).first():
            new_failure = Failure(italian=item['Italian'], english=item['English'], user_id=user.id, language_direction=language_direction)
            db.session.add(new_failure)

    db.session.commit()
    return jsonify({"status": "success"})

@main.route('/signup', methods=['POST'])
def signup():
    user_data = request.json
    username = user_data.get('username')
    password = user_data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success"})

@main.route('/login', methods=['POST'])
def login():
    user_data = request.json
    username = user_data.get('username')
    password = user_data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['user'] = username  # Set session for the logged-in user
        user.last_login = datetime.utcnow()
        db.session.commit()
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
    user = User.query.filter_by(username=username).first()
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

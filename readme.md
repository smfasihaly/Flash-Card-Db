


# Flashcards App

This is a Flashcards web application built with Flask, designed to help users learn Italian verbs through various interactive features.

## Features

- User authentication (signup, login, logout)
- Flashcards for Italian verbs
- Track user progress with statistics
- Pagination support for verb lists
- Randomized verb lists from different categories
- Save user statistics and progress

## Project Structure

```plaintext
Flash-Card-Db/
├── flashcards/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── controllers.py
│   │   ├── models.py
│   │   └── views.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── script.js
│   │   └── images/
│   │       └── logo.png
│   ├── templates/
│   │   └── index.html
│   ├── data/
│   │   └── words.xlsx
│   ├── config.py
│   ├── db.sqlite3
├── app.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/smfasihaly/Flash-Card-Db.git
    cd Flash-Card-Db
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up the database:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. Run the application:
    ```bash
    flask run
    ```

## Configuration

The application configuration is defined in `config.py`. You can adjust the configuration settings as needed.

## Usage

### Authentication

- **Signup**: Create a new user account.
- **Login**: Log into your account.
- **Logout**: Log out of your account.

### Flashcards

- **View Verbs**: View a paginated list of Italian verbs.
- **Randomized Verbs**: Get a randomized list of verbs.
- **Save Statistics**: Save your progress and track statistics.

## API Endpoints

### User Authentication

- **Signup**: `POST /signup`
- **Login**: `POST /login`
- **Logout**: `POST /logout`

### Flashcards

- **Get Verbs**: `GET /get_verbs`
- **Get Verbs from Sheet**: `GET /get_verbs/<sheet_name>`
- **Save Stats**: `POST /save_stats`
- **Remove Verb**: `POST /remove_verb`

## Models

### User

- **id**: Integer, primary key
- **username**: String, unique
- **password**: String
- **last_login**: DateTime

### Word

- **id**: Integer, primary key
- **italian**: String
- **english**: String

### JustFlipped

- **id**: Integer, primary key
- **italian**: String
- **english**: String
- **user_id**: Integer, ForeignKey to User.id
- **language_direction**: String

### Failure

- **id**: Integer, primary key
- **italian**: String
- **english**: String
- **user_id**: Integer, ForeignKey to User.id
- **language_direction**: String


from flask import Flask
from .models import db, Word  # Ensure models are imported
from flashcards.config import Config  
from flask_migrate import Migrate

migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')  # Adjusted static_folder path
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
     
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    with app.app_context():
        if table_exists('words') and is_table_empty():
            import_data_from_excel(app.config['EXCEL_FILE_PATH'])
    return app

def table_exists(table_name):
    inspector = db.inspect(db.engine)
    return inspector.has_table(table_name)


def is_table_empty():
    return db.session.query(Word).count() == 0


def import_data_from_excel(file_path):
    import pandas as pd
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    for index, row in df.iterrows():
        new_word = Word(italian=row['Italian'], english=row['English'])
        db.session.add(new_word)
    db.session.commit()

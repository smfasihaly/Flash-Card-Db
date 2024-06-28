from flask import Flask
from flashcards.config import Config
from .models import db,Word

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')  # Adjusted static_folder path
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        import_data_from_excel(app.config['EXCEL_FILE_PATH'])
        
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app

def import_data_from_excel(file_path):
    import pandas as pd
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    for index, row in df.iterrows():
        new_word = Word(italian=row['Italian'], english=row['English'])
        db.session.add(new_word)
    db.session.commit()

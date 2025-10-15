from webbrowser import get
from flask import Flask, render_template
from routes.events import events_blueprint
from routes.fights import fights_blueprint
from routes.fighters import fighters_blueprint
from extensions import db, page_list
from datetime import date, timedelta
from models import Event, Fight, Fighter
from sqlalchemy import func
import logging
import dotenv
import os

logging.basicConfig(filename='application.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

env = dotenv.load_dotenv()
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

db.init_app(app)

app.register_blueprint(events_blueprint)
app.register_blueprint(fights_blueprint)
app.register_blueprint(fighters_blueprint)

@app.context_processor
def inject_globals():
    return {
        'site_title': "UFC ARCHIVE"
    }


url = '/'
@app.route(url)
def index():
    previous_event_query = Event.query.filter(Event.date < func.current_date()).order_by(Event.date.desc()).first()

    fight_query = Fight.query.filter(Fight.event_id == previous_event_query.id).order_by(Fight.fight_order).all()

    fights = [f.json() for f in fight_query]

    return render_template(
        'index.html',
        page_list=page_list,
        url=url,
        fight_title=previous_event_query.name,
        fights=fights
    )

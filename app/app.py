from webbrowser import get
from flask import Flask, render_template
from routes.fighters import fighters_blueprint
from routes.fights import fights_blueprint
from routes.events import events_blueprint
from extensions import db, page_list
from datetime import date, timedelta
from models import Fight, Event
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
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

db.init_app(app)

app.register_blueprint(fighters_blueprint)
app.register_blueprint(fights_blueprint)
app.register_blueprint(events_blueprint)

url = '/'
@app.route(url)
def index():
    # query to get the next event
    date_query = Event.query.filter(
        Event.date >= date.today() - timedelta(days=1)
    ).order_by(
        Event.date.asc()
    ).first()

    if date_query:
        next_event: str = date_query.title
    fights_query = Fight.query.filter(Fight.event_title == next_event).all()

    # TODO: run the scraper if it is missing
    
    next_event_date = getattr(date_query, 'date')
    # calculate weeks from now to next event
    delta = next_event_date - date.today()
    weeks_to_event = delta.days // 7
    if weeks_to_event <= 0:
        weeks_to_event = 'This week'
    else:
        weeks_to_event = f'{weeks_to_event} weeks from now'

    return render_template(
        'index.html', 
        page_list=page_list, 
        fights=fights_query, 
        weeks_to_event=weeks_to_event,
        url=url, 
    )

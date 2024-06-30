from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models import Fighter, Fights
import dotenv
import os

env = dotenv.load_dotenv()
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/previous_events')
def previous_events():
    table_headers = [column.name for column in Fights.__table__.columns]
    events = Fights.query.order_by(Fights.event_title).all()
    return render_template('previous_events.html', table_headers=table_headers, events=events)

@app.route('/fighters')
def fighter_list():
    table_headers = [column.name for column in Fighter.__table__.columns]
    fighters = Fighter.query.order_by(Fighter.name).all()
    return render_template('fighters.html', fighters=fighters, table_headers=table_headers)

# on hold for now
@app.route('/fighter/<id>')
def fighter_detail(id):
    fighter = Fighter.query.get(id)
    return render_template('fighter_detail.html', fighter=fighter)

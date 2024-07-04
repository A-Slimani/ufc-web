from flask import Flask, render_template
from routes.fighters import fighters_blueprint
from routes.fights import fights_blueprint
from routes.events import events_blueprint
from extensions import db, page_list
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
    return render_template('index.html', page_list=page_list, url=url)

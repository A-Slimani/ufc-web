from flask import Blueprint, jsonify, render_template, request
from extensions import db, page_list
from sqlalchemy import func
from models import Event 


events_blueprint = Blueprint('events', __name__)

url = '/previous-events'
@events_blueprint.route(url)
def previous_events():
    return render_template(f'{url}.html', url=url, page_list=page_list)


@events_blueprint.route(f'/api{url}')
def previous_events_api():
    # base query
    query = Event.query.order_by(Event.date.desc())

    return jsonify({'events': query}) 





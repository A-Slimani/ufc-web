from flask import Blueprint, render_template, request
from extensions import db, page_list
from models import Fights


events_blueprint = Blueprint('events', __name__)

url = '/previous-events'
@events_blueprint.route(url)
def previous_events():
    return render_template(f'{url}.html', url=url, page_list=page_list)


# @events_blueprint.route(f'/api/{url}')
# def previous_events_api():
#     # base query
#     query = Fights.query.order_by(Fights.date.desc())
# 
#     # search
#     search_query = request.args.get('search', default=None, type=str)





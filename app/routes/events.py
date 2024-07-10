from flask import Blueprint, jsonify, render_template, request
from extensions import page_list
from sqlalchemy import func
from models import Event, Fight 
import re


events_blueprint = Blueprint('events', __name__)

url = '/previous-events'
@events_blueprint.route(url)
def previous_events():
    return render_template(f'{url}.html', url=url, page_list=page_list)


@events_blueprint.route(f'/api{url}')
def previous_events_api():
    # base query 
    query = Event.query.order_by(Event.date.desc())
    
    # searching
    search_query = request.args.get('search', default=None, type=str)
    if search_query:
        query = query.filter(func.lower(Event.title).like(f'%{search_query.lower()}%'))
        event_list = [fighter.json() for fighter in query] 
    
    # sorting
    column_name = request.args.get('col', type=str)
    direction = request.args.get('dir', type=str)
    if column_name and direction:
        if direction == 'desc':
            query = query.order_by(None).order_by(getattr(Event, column_name).desc())
        if direction == 'asc': 
            query = query.order_by(None).order_by(getattr(Event, column_name).asc())
    
    # pagination & filter out future events
    page = request.args.get('page', type=int)
    limit = request.args.get('limit', default=20, type=int)
    paginated_query = query.filter(Event.date < func.current_date()).order_by(Event.date).paginate(page=page, per_page=limit, error_out=True)

    event_list = []
    for event in paginated_query.items:
        event.date = event.date.strftime("%d %b %Y") 
        event_list.append(event.json())
    
    pagination_info = {
        'page': paginated_query.page,
        'pages': paginated_query.pages,
        'total': paginated_query.total,
        'prev_page': paginated_query.prev_num,
        'next_page': paginated_query.next_num,  
        'has_prev': paginated_query.has_prev,
        'has_next': paginated_query.has_next,
    }

    return jsonify({'event_list': event_list, 'pagination': pagination_info}) 

@events_blueprint.route('/event/<title>')
def fight_info(title): 
    query = Fight.query.filter(Fight.event_title_cleaned == title).order_by(Fight.fight_weight).all()
    fights = [fight.json() for fight in query]

    # title fix
    title = title.replace('-', ' ')
    title = re.sub(r'(?<=\d)(?=\D)', ':', title)

    return render_template('fight-data.html', title=title, fights=fights, url='/fight-data', page_list=page_list)

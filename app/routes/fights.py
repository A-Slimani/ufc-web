from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import func, case
from extensions import db, page_list
from models import Fights
import datetime as dt

fights_blueprint = Blueprint('fights', __name__)

url = '/previous-fights'
@fights_blueprint.route(url)
def previous_events():
    return render_template(f'/{url}.html', page_list=page_list, url=url)

@fights_blueprint.route('/api/previous-fights')
def previous_events_api():
    # base query
    query = Fights.query.order_by(Fights.date.desc())

    # search
    search_query = request.args.get('search', default=None, type=str)
    limit = request.args.get('limit', default=20, type=int)
    if search_query:
        query = query.filter(func.lower(Fights.event_title).like(f'%{search_query.lower()}%'))
        fight_list = [fight.json() for fight in query]
    
    # sorting
    column_name = request.args.get('col', type=str)
    direction = request.args.get('dir', type=str)
    if column_name and direction:
        if direction == 'asc':
            if column_name == 'event_title':
                query = query.order_by(None).order_by(Fights.date.asc())
            elif column_name == 'status':
                query = query.order_by(None).order_by(Fights.left_status.asc())
            elif column_name == 'weight_class':
                query = query.order_by(None).order_by(
                    case(
                        Fights.WEIGHT_CLASSES,
                        value=Fights.weight_class,
                    ).asc()
                )
            else:
                query = query.order_by(None).order_by(getattr(Fights, column_name).asc())
        else:
            if column_name == 'event_title':
                query = query.order_by(None).order_by(Fights.date.desc())
            elif column_name == 'status':
                query = query.order_by(None).order_by(Fights.left_status.desc())
            elif column_name == 'weight_class':
                query = query.order_by(None).order_by(
                    case(
                        Fights.WEIGHT_CLASSES,
                        value=Fights.weight_class,
                    ).desc()
                )
            else:
                query = query.order_by(None).order_by(getattr(Fights, column_name).desc())

        
    # pagination
    page = request.args.get('page', type=int)
    pagination = query.paginate(page=page, per_page=limit, error_out=True)
    fight_list = []
    for fight in pagination.items:
        fight_item = fight.json()
        if fight.left_status == 'win':
            fight_item['status'] = 'def.'
        elif fight.left_status == 'draw':
            fight_item['status'] = 'draw'
        elif fight.left_status == 'NC':
            fight_item['status'] = 'NC'
        fight_list.append(fight_item) 
    pagination_info = {
        'page': pagination.page,
        'pages': pagination.pages,
        'total': pagination.total,
        'prev_page': pagination.prev_num,
        'next_page': pagination.next_num,
        'has_prev': pagination.has_prev,
        'has_next': pagination.has_next,
    }

    return jsonify({
        'fights': fight_list,
        'pagination': pagination_info
    }) 

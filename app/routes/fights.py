from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import func, case
from extensions import page_list
from models import Fight, Event

fights_blueprint = Blueprint('fights', __name__)

url = '/previous-fights'
@fights_blueprint.route(url)
def previous_events():
    return render_template(f'/{url}.html', page_list=page_list, url=url)

@fights_blueprint.route('/api/previous-fights')
def previous_fights_api():
    # base query
    query = Fight.query.join(Event).order_by(Event.date.desc())

    # search
    search_query = request.args.get('search', default=None, type=str)
    limit = request.args.get('limit', default=20, type=int)
    if search_query:
        query = query.filter(func.lower(Fight.event_title).like(f'%{search_query.lower()}%'))
        fight_list = [fight.json() for fight in query]
    
    # sorting
    column_name = request.args.get('col', type=str)
    direction = request.args.get('dir', type=str)
    if column_name and direction:
        if direction == 'asc':
            if column_name == 'event_title':
                query = query.order_by(None).order_by(Event.date.asc()).order_by()
            elif column_name == 'status':
                query = query.order_by(None).order_by(Fight.left_status.asc())
            elif column_name == 'weight_class':
                query = query.order_by(None).order_by(
                    case(
                        Fight.WEIGHT_CLASSES,
                        value=Fight.weight_class,
                    ).asc()
                )
            else:
                query = query.order_by(None).order_by(getattr(Fight, column_name).asc())
        else:
            if column_name == 'event_title':
                query = query.order_by(None).order_by(Event.date.desc())
            elif column_name == 'status':
                query = query.order_by(None).order_by(Fight.left_status.desc())
            elif column_name == 'weight_class':
                query = query.order_by(None).order_by(
                    case(
                        Fight.WEIGHT_CLASSES,
                        value=Fight.weight_class,
                    ).desc()
                )
            else:
                query = query.order_by(None).order_by(getattr(Fight, column_name).desc())
    
    # sorting fights by card order
    query = query.order_by(Fight.fight_weight.asc())
        
    # pagination
    page = request.args.get('page', type=int)
    paginated_query = query.paginate(page=page, per_page=limit, error_out=True)
    fight_list = []
    for fight in paginated_query.items:
        fight_item = fight.json()
        if fight.left_status == 'win':
            fight_item['status'] = 'def.'
        elif fight.left_status == 'draw':
            fight_item['status'] = 'draw'
        elif fight.left_status == 'NC':
            fight_item['status'] = 'NC'
        fight_list.append(fight_item) 
    pagination_info = {
        'page': paginated_query.page,
        'pages': paginated_query.pages,
        'total': paginated_query.total,
        'prev_page': paginated_query.prev_num,
        'next_page': paginated_query.next_num,
        'has_prev': paginated_query.has_prev,
        'has_next': paginated_query.has_next,
    }

    return jsonify({
        'fights': fight_list,
        'pagination': pagination_info
    }) 
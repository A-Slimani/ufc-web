from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import func, case
from extensions import page_list
from models import Fighter

fighters_blueprint = Blueprint('fighters', __name__)

url = '/fighters'
@fighters_blueprint.route(url)
def fighter_list():
    return render_template(f'{url}.html', page_list=page_list, url=url)

@fighters_blueprint.route('/api/fighters')
def fighters_page_api():
    # base query
    query = Fighter.query.order_by(Fighter.name)

    # searching
    search_query = request.args.get('search', default=None, type=str)
    if search_query:
        query = query.filter(func.lower(Fighter.name).like(f'%{search_query.lower()}%'))
        fighters_list = [fighter.json() for fighter in query]
    
    # sorting
    column_name = request.args.get('col', type=str)
    direction = request.args.get('dir', type=str)
    if column_name and direction:
        if column_name == 'weight_class':
            if direction == 'asc':
                query = query.order_by(None).order_by(
                    case(
                        Fighter.WEIGHT_CLASSES, # gets the order
                        value=Fighter.weight_class, # gets the column
                    ).asc()
                )
            elif direction == 'desc':
                query = query.order_by(None).order_by(
                    case(
                        Fighter.WEIGHT_CLASSES,
                        value=Fighter.weight_class,
                    ).desc()
                )
        else: 
            if direction == 'desc':
                query = query.order_by(None).order_by(getattr(Fighter, column_name).desc())
            if direction == 'asc': 
                query = query.order_by(None).order_by(getattr(Fighter, column_name).asc())

    # pagination
    page = request.args.get('page', type=int)
    limit = request.args.get('limit', default=20, type=int)
    paginated_query = query.order_by(Fighter.name).paginate(page=page, per_page=limit, error_out=True)
    fighters_list = [fighter.json() for fighter in paginated_query.items]
    pagination_info = {
        'page': paginated_query.page,
        'pages': paginated_query.pages,
        'total': paginated_query.total,
        'prev_page': paginated_query.prev_num,
        'next_page': paginated_query.next_num,
        'has_prev': paginated_query.has_prev,
        'has_next': paginated_query.has_next,
    }    

    return jsonify({'fighters': fighters_list, 'pagination': pagination_info})


@fighters_blueprint.route('/fighter/<id>')
def fighter_detail(id):
    fighter = Fighter.query.get(id)
    return render_template('fighter-profile.html', fighter=fighter)

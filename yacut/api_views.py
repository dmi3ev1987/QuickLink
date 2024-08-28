import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id

SHORT_URL_MAX_LENGTH = 16


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    if not request.data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    else:
        data['original'] = data.pop('url')
    if 'custom_id' not in data or data['custom_id'] == '':
        data['short'] = get_unique_short_id()
    else:
        data['short'] = data.pop('custom_id')
        if (
            not re.match('^[a-zA-Z0-9]+$', data['short'])
            or len(data['short']) > SHORT_URL_MAX_LENGTH
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
    if URLMap.query.filter_by(short=data['short']).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    short_url = URLMap()
    short_url.from_dict(data)
    db.session.add(short_url)
    db.session.commit()
    return jsonify(short_url.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify(url_map.to_original_url()), 200

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import ShortLinkForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = ShortLinkForm()

    if not form.validate_on_submit():
        return render_template('short_link.html', form=form)

    original_link = form.original_link.data
    custom_id = form.custom_id.data

    if URLMap.query.filter_by(short=custom_id).first() is not None:
        flash(
            'Предложенный вариант короткой ссылки уже существует.',
            'unique',
        )
        return render_template('short_link.html', form=form)

    if not custom_id:
        custom_id = get_unique_short_id()

    url_map = URLMap(
        original=original_link,
        short=custom_id,
    )
    db.session.add(url_map)
    db.session.commit()
    url = url_for('redirect_view', short=custom_id, _external=True)
    flash(url, 'url')

    return render_template('short_link.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)

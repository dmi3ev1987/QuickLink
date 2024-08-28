from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from .constants import ORIGINAL_URL_MAX_LENGTH, SHORT_URL_MAX_LENGTH


class ShortLinkForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(
                max=ORIGINAL_URL_MAX_LENGTH, message='Слишком длинная ссылка'
            ),
        ],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(), Length(max=SHORT_URL_MAX_LENGTH)],
    )
    submit = SubmitField('Создать')

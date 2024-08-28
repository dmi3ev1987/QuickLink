from datetime import datetime, timezone

from flask import url_for

from yacut import db

from .constants import SHORT_URL_MAX_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(SHORT_URL_MAX_LENGTH), nullable=False)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.now(timezone.utc),
    )

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view', short=self.short, _external=True
            ),
        )

    def to_original_url(self):
        return dict(url=self.original)

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])

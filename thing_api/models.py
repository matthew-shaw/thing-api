from thing_api.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import json
import uuid


class Thing(db.Model):
    """Class represention of a Thing."""
    __tablename__ = 'thing'

    # Fields
    thing_id = db.Column(UUID, primary_key=True)
    foo = db.Column(db.String, nullable=False)
    bar = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    archived_at = db.Column(db.DateTime, nullable=True)

    # Methods
    def __init__(self, foo, bar):
        self.thing_id = str(uuid.uuid4())
        self.foo = foo
        self.bar = bar
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return json.dumps(self.as_dict(), separators=(',', ':'))

    def as_dict(self):
        if self.updated_at:
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        if self.archived_at:
            archived_at = self.archived_at.isoformat()
        else:
            archived_at = self.archived_at

        return {
            "thing_id": self.thing_id,
            "foo": self.foo,
            "bar": self.bar,
            "created_at": self.created_at.isoformat(),
            "updated_at": updated_at,
            "archived_at": archived_at
        }

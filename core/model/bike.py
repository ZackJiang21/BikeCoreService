from core.model import db
from core.model.user import User


class Bike(db.Model):
    __tablename__ = 't_bike'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    model = db.Column(db.String(32), nullable=False)
    size = db.Column(db.String(16), nullable=False)
    year = db.Column(db.SmallInteger, nullable=False)
    type = db.Column(db.String(16), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Bike  {}, userId: {}>'.format(self.model, self.user_id)

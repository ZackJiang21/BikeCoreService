from core.model import db


class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.SmallInteger)
    age = db.Column(db.INT)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(128))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<User  {}>'.format(self.name)

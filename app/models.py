from extensions import db


class Fighter(db.Model):
    __tablename__ = 'fighters'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    nationality = db.Column(db.String, nullable=True)
    locality = db.Column(db.String, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    weight_class = db.Column(db.String, nullable=True)
    wins = db.Column(db.Integer)
    wins_by_ko_tko = db.Column(db.Integer)
    wins_by_sub = db.Column(db.Integer)
    wins_by_dec = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    losses_by_ko_tko = db.Column(db.Integer)
    losses_by_sub = db.Column(db.Integer)
    losses_by_dec = db.Column(db.Integer)

    def __repr__(self):
        return f'<Fighter {self.id}>'
        

class Fights(db.Model):
    __tablename__ = "fights"

    id = db.Column(db.String, primary_key=True)
    event_title = db.Column(db.String)
    left_fighter_id = db.Column(db.String, db.ForeignKey('fighters.id'))
    left_fighter_name = db.Column(db.String, nullable=True)
    left_status = db.Column(db.String)
    right_fighter_id = db.Column(db.String, db.ForeignKey('fighters.id'))
    right_fighter_name = db.Column(db.String, nullable=True)
    right_status = db.Column(db.String)
    weight_class = db.Column(db.String, nullable=True)
    method = db.Column(db.String)
    round = db.Column(db.Integer, nullable=True)
    time = db.Column(db.String)
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

    WEIGHT_CLASSES = {
        'Strawweight': 1,
        'Flyweight': 5,
        'Bantamweight': 6,
        'Featherweight': 7,
        'Lightweight': 8,
        'Welterweight': 9,
        'Middleweight': 10,
        'Light Heavyweight': 11,
        'Heavyweight': 12,
        'Super Heavyweight': 13,
    }

    def __repr__(self):
        return f'<Fighter {self.id}>'

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'nationality': self.nationality,
            'locality': self.locality,
            'age': self.age,
            'weight_class': self.weight_class,
            'wins': self.wins,
            'wins_by_ko_tko': self.wins_by_ko_tko,
            'wins_by_sub': self.wins_by_sub,
            'wins_by_dec': self.wins_by_dec,
            'losses': self.losses,
            'losses_by_ko_tko': self.losses_by_ko_tko,
            'losses_by_sub': self.losses_by_sub,
            'losses_by_dec': self.losses_by_dec,
        }
        

class Fight(db.Model):
    __tablename__ = "fights"

    id = db.Column(db.String, primary_key=True)
    event = db.relationship('Event', backref=db.backref('fights', lazy=True))
    event_title = db.Column(db.String, db.ForeignKey('events.title'))
    event_title_cleaned = db.Column(db.String)
    left_fighter_id = db.Column(db.String, db.ForeignKey('fighters.id'))
    left_fighter_name = db.Column(db.String, nullable=True)
    left_status = db.Column(db.String)
    right_fighter_id = db.Column(db.String, db.ForeignKey('fighters.id'))
    right_fighter_name = db.Column(db.String, nullable=True)
    right_status = db.Column(db.String)
    weight_class = db.Column(db.String, nullable=True)
    fight_weight = db.Column(db.Integer)
    method = db.Column(db.String)
    round = db.Column(db.Integer, nullable=True)
    time = db.Column(db.String)

    WEIGHT_CLASSES = {
        'Strawweight': 1,
        'Flyweight': 5,
        'Bantamweight': 6,
        'Featherweight': 7,
        'Lightweight': 8,
        'Welterweight': 9,
        'Middleweight': 10,
        'Light Heavyweight': 11,
        'Heavyweight': 12,
        'Super Heavyweight': 13,
    }

    def json(self):
        return {
            'id': self.id,
            'event_title': self.event_title,
            'left_fighter_id': self.left_fighter_id,
            'left_fighter_name': self.left_fighter_name,
            'left_status': self.left_status,
            'right_fighter_id': self.right_fighter_id,
            'right_fighter_name': self.right_fighter_name,
            'right_status': self.right_status,
            'weight_class': self.weight_class,
            'method': self.method,
            'round': self.round,
            'time': self.time
        }
        
class Event(db.Model):
    __tablename__ = 'events'

    title = db.Column(db.String, primary_key=True)
    date = db.Column(db.DateTime)
    location = db.Column(db.String)

    def json(self):
        return {
            'title': self.title,
            'date': self.date,
            'location': self.location,
        }


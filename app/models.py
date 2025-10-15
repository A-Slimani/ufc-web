from extensions import db

class Event(db.Model):
    __tablename__ = 'dim_events'
    __table_args__ = {'schema': 'dbt_schema'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date = db.Column(db.DateTime)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    venue = db.Column(db.String)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "venue": self.venue,
        }

class Fight(db.Model):
    __tablename__ = 'fact_fights'
    __table_args__ = {'schema': 'dbt_schema'}

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('dbt_schema.dim_events.id'))
    r_fighter_id = db.Column(db.Integer)
    r_fighter_name = db.Column(db.String)
    r_fighter_status = db.Column(db.String)
    b_fighter_id = db.Column(db.Integer)
    b_fighter_name = db.Column(db.String)
    b_fighter_status = db.Column(db.String)
    bout_weight = db.Column(db.String) 
    method = db.Column(db.String)
    ending_round = db.Column(db.Integer)
    bout_rounds = db.Column(db.Integer)
    time = db.Column(db.String)
    fight_order = db.Column(db.Integer)

    event = db.relationship('Event', backref=db.backref('fact_fights', lazy=True))

    def json(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'event_name': self.event.name,
            'r_fighter_id': self.r_fighter_id,
            'r_fighter_name': self.r_fighter_name,
            'r_fighter_status': self.r_fighter_status,
            'b_fighter_id': self.b_fighter_id,
            'b_fighter_name': self.b_fighter_name,
            'b_fighter_status': self.b_fighter_status,
            'bout_weight': self.bout_weight,
            'method': self.method,
            'ending_round': self.ending_round,
            'bout_rounds': self.bout_rounds,
            'time': self.time,
            'fight_order': self.fight_order
        }


class Fighter(db.Model):
    __tablename__ = 'dim_fighters'
    __table_args__ = {'schema': 'dbt_schema'}

    fighter_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    nick_name = db.Column(db.String)
    # nationality = db.Column(db.String, nullable=True)
    # locality = db.Column(db.String, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    weight_class_id = db.Column(db.Integer)
    weight_class_description = db.Column(db.String, nullable=True)
    last_active = db.Column(db.Date)
    ufc_wins = db.Column(db.Integer)
    ufc_wins_by_ko_tko = db.Column(db.Integer)
    ufc_wins_by_sub = db.Column(db.Integer)
    ufc_wins_by_dec = db.Column(db.Integer)
    ufc_losses = db.Column(db.Integer)


    def __repr__(self):
        return f'<Fighter {self.id}>'

    def json(self):
        return {
            'fighter_id': self.fighter_id,
            'full_name': self.full_name,
            # 'nationality': self.nationality,
            # 'locality': self.locality,
            'age': self.age,
            'last_active': self.last_active,
            'weight_class_id': self.weight_class_id,
            'weight_class_description': self.weight_class_description,
            'ufc_wins': self.ufc_wins,
            'ufc_wins_by_ko_tko': self.ufc_wins_by_ko_tko,
            'ufc_wins_by_sub': self.ufc_wins_by_sub,
            'ufc_wins_by_dec': self.ufc_wins_by_dec,
            'ufc_losses': self.ufc_losses,
        }

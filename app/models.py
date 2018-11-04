from datetime import datetime

from app import db

class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"mysql_engine": "InnoDB"}

    user_id = db.Column(db.Integer, primary_key=True)
    fb_id = db.Column(db.String(64), index=True, unique=True)
    mid_conversation = db.Column(db.Boolean, index=True)
    has_onboarded = db.Column(db.Boolean, index=True)
    last_action = db.Column(db.String(64), index=True)
    checkins = db.relationship("CheckIn", backref="user", lazy="dynamic")
    messages = db.relationship("Message", backref="user", lazy="dynamic")

    def __repr__(self):
        return "<User: {}>".format(self.user_id)

class Message(db.Model):
    __tablename__ = "Message"
    __table_args__ = {"mysql_engine": "InnoDB"}

    message_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), 
        onupdate="cascade")
    datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow) 
    text = db.Column(db.String(64), index=True)

    def __repr__(self):
        return "<Message: {}>".format(self.text)

class Intervention(db.Model):
    __tablename__ = "intervention"
    __table_args__ = {"mysql_engine": "InnoDB"}

    intervention_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2048))
    checkins = db.relationship("CheckIn", backref="intervention", 
        lazy="dynamic")

    def __repr__(self):
        return "<Intervention: {}>".format(self.text)

class UserIntervention(db.Model):
    __tablename__ = "user_intervention"
    __table_args__ = {"mysql_engine": "InnoDB"}

    uid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"),
        onupdate="cascade")
    intervention_id = db.Column(db.Integer, 
        db.ForeignKey("intervention.intervention_id"), onupdate="cascade")

    def __repr__(self):
        return "<User: {}; Intervention: {}>".format(
            self.user_id,
            self.intervention_id)

class CheckIn(db.Model):
    __tablename__ = "check_in"
    __table_args__ = {"mysql_engine": "InnoDB"}

    checkin_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), 
        onupdate="cascade")
    datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    baseline = db.Column(db.Integer, index=True)
    tried_intervention = db.Column(db.Boolean, index=True)
    intervention_id = db.Column(db.Integer, 
        db.ForeignKey("intervention.intervention_id"), onupdate="cascade")
    impact = db.Column(db.Integer, index=True)

    def __repr__(self):
        return "<Check in: {}>".format(self.checkin_id)
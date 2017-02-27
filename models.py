
import os
from app import db


class user(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    pswd = db.Column(db.String(64))

    def __repr__(self):
        return '<User %r>' % self.username


def check_user(username,pswd):
    u = user.query.filter_by(username=username).first()
    if u:
        if 


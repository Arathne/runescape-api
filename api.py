from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__, static_folder="./static")

## DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///runescape.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Item Table
#
class Items (db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    name =          db.Column(db.String(100))
    description =   db.Column(db.String(200))
    member =        db.Column(db.String(20))
    type_name =     db.Column(db.String(30))
    type_icon =     db.Column(db.String(200))
    icon =          db.Column(db.String(200))
    icon_large =    db.Column(db.String(200))
    current_price = db.Column(db.String(30))
    current_trend = db.Column(db.String(30))
    today_price =   db.Column(db.String(30))
    today_trend =   db.Column(db.String(30))
    day30_change =  db.Column(db.String(10))
    day30_trend =   db.Column(db.String(30))
    day90_change =  db.Column(db.String(10))
    day90_trend =   db.Column(db.String(30))
    day180_change = db.Column(db.String(10))
    day180_trend =  db.Column(db.String(30))

    def to_string(self):
        data = '\"id\": \"%s\",'            % self.id
        data += '\"name\": \"%s\",'         % self.name
        data += '\"description\": \"%s\",'  % self.description
        data += '\"member\": \"%s\",'        % self.member
        data += '\"type\": \"%s\",'          % self.type_name
        data += '\"type_icon\": \"%s\",'     % self.type_icon
        data += '\"icon\": \"%s\",'          % self.icon
        data += '\"icon_large\": \"%s\",'    % self.icon_large
        data += '\"current_price\": \"%s\",' % self.current_price
        data += '\"current_trend\": \"%s\",' % self.current_trend
        data += '\"today_price\": \"%s\",'   % self.today_price
        data += '\"today_trend\": \"%s\",'   % self.today_trend
        data += '\"day30_change\": \"%s\",'  % self.day30_change
        data += '\"day30_trend\": \"%s\",'   % self.day30_trend
        data += '\"day90_change\": \"%s\",'  % self.day90_change
        data += '\"day90_trend\": \"%s\",'   % self.day90_trend
        data += '\"day180_change\": \"%s\",' % self.day180_change
        data += '\"day180_trend\": \"%s\"'  % self.day180_trend
        return '{ %s }' % data


# returns an array of items
#
@app.route('/api/all')
def all():
    itemList = Items.query.all()
    
    json = ""
    for i in range( len(itemList) ):
        json += itemList[i].to_string()
        if i < len(itemList)-1:
            json += ', ';

    return '[ %s ]' % json

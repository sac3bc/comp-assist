import os
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
# app.config['SECRET_KEY'] = "random string"
app.secret_key = os.urandom(24)


db = SQLAlchemy(app)



class Event(db.Model):

   id = db.Column(db.Integer,  primary_key=True)
   name = db.Column(db.String(128))
   rounds = db.relationship('Round', backref='event')


   def __init__(self, name):
      self.name = name 

   def __repr__(self):
      return '<Event %r>' % (self.name)



class Round(db.Model):

   id = db.Column(db.Integer,  primary_key=True)
   # event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
   number = db.Column(db.Integer)


   #define the one to many relationship with the scoresheets
   competitors = db.relationship('Scoresheet', backref="round")
   event_id = db.Column(db.Integer, db.ForeignKey('event.id')) #author_id 


   def __init__(self, number):
        self.number = number 

   def __repr__(self):
      return '<Round:{}>'.format(self.number)


class Scoresheet(db.Model):

   id = db.Column(db.Integer, primary_key=True) #id
   time1 = db.Column(db.String(16))
   time2 = db.Column(db.String(16))
   time3 = db.Column(db.String(16))
   time4 = db.Column(db.String(16))
   time5 = db.Column(db.String(16))
   competitor_name = db.Column(db.String(80)) #title 
   round_id = db.Column(db.Integer, db.ForeignKey('round.id')) #author_id                               

   # id = db.Column(db.Integer, primary_key=True)
   # title = db.Column(db.Text)
   # content = db.Column(db.Text)
   # author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

   def __init__(self, competitor_name):
     self.competitor_name = competitor_name



   def __repr__(self):
      return '<Scoresheet %r: %r, %r, %r, %r, %r>' % (self.competitor_name, self.time1, self.time2, self.time3, self.time4, self.time5) 


def __init__(self, name, city, addr, pin):
   self.name = name
   self.city = city
   self.addr = addr
   self.pin = pin

@app.route('/')
def index(): 
    return render_template('new_comp.html', events = Event.query.all())


@app.route("/event/<id>")
def show_event(id): 
    event = Event.query.get(id)
    # return render_emplate("event.html", event = event)
    return render_template("event.html", event=event)
    # return'Event %s!' % event.name 


@app.route('/new_event', methods = ['GET', 'POST'])
def new_event(): 
   if request.method == 'POST':
         if not request.form['name']:
            flash('Please enter all the fields', 'error')
         else:
            event = Event(name=request.form['name'])
            
            db.session.add(event)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('index'))
   return render_template('new_event.html')

@app.route('/new_round/<id>', methods = ['GET', 'POST'])
def new_round(id): 

   event = Event.query.get(id)
   if request.method == 'POST':
         if not request.form['number']:
            flash('Please enter all the fields', 'error')
         else:
            round = Round(number=request.form['number'])
            
           
            event.rounds.append(round)
            db.session.add(round)
            db.session.add(event)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_event', id=id))

   return render_template('new_round.html', id=id)



@app.route('/round/<id>')
def show_round(id): 
   round = Round.query.get(id)
   event=Event.query.get(round.event_id)

    # return render_emplate("event.html", event = event)
   return render_template("round.html",  round = round, event=event)
    # return'Event %s!' % event.name 


@app.route('/new_competitor/<id>', methods = ['GET', 'POST'])
def new_competitor(id): 

   round = Round.query.get(id)
   if request.method == 'POST':
         if not request.form['name']:
            flash('Please enter all the fields', 'error')
         else:
            competitor = Scoresheet(competitor_name=request.form['name'])
            
           
            round.competitors.append(competitor)
            db.session.add(competitor)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_round', id=id))

   return render_template('new_competitor.html', id=id)

if __name__ == '__main__':
   db.drop_all()
   db.create_all()
   
   app.run()
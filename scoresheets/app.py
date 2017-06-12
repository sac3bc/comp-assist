
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, g, redirect, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)
# app.debug = True


hit_count = 0
#for our database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\sesic\\Desktop\\test.db'
#for our images
UPLOAD_FOLDER = 'C:\\Users\\sesic\\Desktop\\scoreshees\\sheets'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']) #for our image

db = SQLAlchemy(app) #passes db to application 

"""
DIRECTORY: Classes, Routing, Database 

"""



"""

CLASSES: Event, Round, Scoresheet 

"""
class Event(db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String(128))
    rounds = db.relationship('Round', backref='event')


    def __init__(self, name):
        self.name = name 

    def __repr__(self):
        return '<Event %r>' % (self.name)



class Round(db.Model):
    #Template for creating an Event
    #In this iteration, we'll use a 1 to many relationship
    # event_id = db.Column(db.Integer, primary_key=True)
    # event_name = db.Column(db.String(16))
    id = db.Column(db.Integer,  primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    number = db.Column(db.Integer)

 
    #define the one to many relationship with the scoresheets
    competitors = db.relationship('Scoresheet', backref="round", lazy="dynamic")
    

    def __init__(self, number):
        self.number = number 

   

    def __repr__(self):
        return '<Event Round %r: %r>' % (self.event.name, self.number)

class Scoresheet(db.Model):
    #Template for creating a Scoresheet for a competitor
    #NO FOREIGN KEYS LINKING THIS TABLES - fix
    id = db.Column(db.Integer, primary_key=True)
    time1 = db.Column(db.String(16))
    time2 = db.Column(db.String(16))
    time3 = db.Column(db.String(16))
    time4 = db.Column(db.String(16))
    time5 = db.Column(db.String(16))
    competitor_name = db.Column(db.String(80))

    #define foreign key for the child table
    #comes from the parent table's primary key 
    #will later be id, but for now lets make it the name 
    # event = db.relationship()



    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))
    

    def __init__(self, competitor_name):
        self.competitor_name = competitor_name
   

    def __repr__(self):
        return '<Scoresheet %r: %r, %r, %r, %r, %r>' % (self.competitor_name, self.time1, self.time2, self.time3, self.time4, self.time5) 

"""

ROUTING

/: Main page with Hit Count, takes in name
/results: Result of entering name in main page
/checkcards: Allows data entry for scorecards
/checkresults: Result of data entry for scorecards, shows times
/list: List database results 
/scorecarsds<id>

"""

@app.route("/")
def index():
    events = Event.query.all()
    return render_template("index.html", events = events)

@app.route("/event/<id>")
def show_event(id): 
    event = Event.query.get(id)
    return render_emplate("event.html", event = event)


@app.route("/results", methods = ['POST'])
def results():
	name = request.form['name']
	return render_template("index.html", name=name, hit_count=0)


#Form to fill in the time on the scorecards
@app.route("/checkcards")
def checkcards(): 
    return render_template("scorechecker.html", time_1="", time_2="", time_3="", time_4="", time_5="")

#Updates the scorechecker.html with the input from the HTML form 
@app.route("/checkresults", methods= ['POST'])
def checkresults():
    
    #Use Post to get variables from form and store
    comp_name = request.form['comp_name']
    time_1 = request.form['time_1']
    time_2 = request.form['time_2']
    time_3 = request.form['time_3']
    time_4 = request.form['time_4']
    time_5 = request.form['time_5']

    #Create and commit a new database entry 
    new_scoresheet = Scoresheet(comp_name)

    new_scoresheet.time1 = time_1
    new_scoresheet.time2 = time_2
    new_scoresheet.time3 = time_3
    new_scoresheet.time4 = time_4
    new_scoresheet.time5 = time_5
   
    db.session.add(new_scoresheet)
    db.session.commit()

    


    return render_template("scorechecker.html", time_1=time_1, time_2=time_2, time_3=time_3, time_4=time_4, time_5=time_5, comp_name = comp_name)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/list")
def list_all(): 
    return render_template('list.html', )

def show_scorecard(id): 
    scorecard = Scoresheet.query.filter_by(id=id).first()
    print(scorecard)
    return render_template("scorecard.html", card=scorecard)

@app.route("/scorecards/<id>")
def show_scorecard(id): 
    scorecard = Scoresheet.query.filter_by(id=id).first()
    print(scorecard)
    return render_template("scorecard.html", card=scorecard)



"""
DATABASE

"""

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def seed():
    db.drop_all()
    db.create_all()
    three_by_three = Event("3x3")
    round1 = Round(1)
    comp1 = Scoresheet("John")
    comp2 = Scoresheet("Lars")
    three_by_three.rounds = [round1]
    round1.scoresheets = [comp1, comp2]

    db.session.add(three_by_three)
    db.session.commit()

if __name__ == "__main__":
    #app.run(debug=True)
    seed()
    app.run()
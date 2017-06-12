
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, g, redirect, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)
# app.debug = True


hit_count = 0

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\sesic\\Desktop\\test.db'
app.config['UPLOADS_FOLDER']
db = SQLAlchemy(app) #passes db to application 

"""
DIRECTORY: Classes, Routing, Database 

"""



"""

CLASSES: Event, Scoresheet 

"""

class Event(db.Model):
    #Template for creating an Event
    #In this iteration, we'll use a 1 to many relationship
    # event_id = db.Column(db.Integer, primary_key=True)
    # event_name = db.Column(db.String(16))
    event_id = db.Column(db.Integer)
    event_name = db.Column(db.String(16), primary_key=True)
    current_round = db.Column(db.String(16))

 
    #define the one to many relationship with the scoresheets
    competitors = db.relationship('Scoresheet', backref="event", lazy="dynamic")
    

    def __init__(self, event_name, current_round):
        self.event_name = event_name
        self.current_round = current_round 

   

    def __repr__(self):
        return '<Event %r: %r>' % (self.event_name, self.current_round)

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
    comp_event = db.Column(db.Integer, db.ForeignKey('event.event_name'))
    

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
    global hit_count
    hit_count += 1
    return render_template("index.html", name="", hit_count=hit_count)

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


if __name__ == "__main__":
    app.run()

import os

from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template, request, g





app = Flask(__name__)
hit_count = 0

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\sesic\\Desktop\\test.db'
db = SQLAlchemy(app)


class Scoresheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time1 = db.Column(db.String(16))
    time2 = db.Column(db.String(16))
    time3 = db.Column(db.String(16))
    time4 = db.Column(db.String(16))
    time5 = db.Column(db.String(16))
    competitor_name = db.Column(db.String(80))
    

    def __init__(self, competitor_name):
        self.competitor_name = competitor_name
   

    def __repr__(self):
        return '<Scoresheet %r: %r, %r, %r, %r, %r>' % (self.competitor_name, self.time1, self.time2, self.time3, self.time4, self.time5) 



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
    time_1 = request.form['time_1']
    time_2 = request.form['time_2']
    time_3 = request.form['time_3']
    time_4 = request.form['time_4']
    time_5 = request.form['time_5']

    return render_template("scorechecker.html", time_1=time_1, time_2=time_2, time_3=time_3, time_4=time_4, time_5=time_5)

@app.route("/scorecards/<id>")
def show_scorecard(id): 
    scorecard = Scoresheet.query.filter_by(id=id).first()
    print(scorecard)
    return render_template("scorecard.html", card=scorecard)





#DATABASE 
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
"""
A simple recipe flask app.
"""
from flask import Flask, redirect, request, url_for, render_template
from flask.views import MethodView
import dashboard
import removeDashboard
from add import AddTeam
from add import AddStudent
from index import Index
from remove import RemoveStudent
from remove import RemoveTeam
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/anguyen/Desktop/470/capstone/capstone360.db'
app.config['SECRET_KEY'] = '06ca1f7f68edd3eb7209a5fca2cc6ca0'
engine = create_engine('sqlite:////Users/anguyen/Desktop/470/capstone/capstone360.db', convert_unicode=True, echo=False)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
db_session = scoped_session(sessionmaker(bind=engine))

app.add_url_rule('/',
                 view_func=Index.as_view('index'))

@app.route('/dashboard/')
@app.route('/dashboard/', methods=['GET','POST'])
def get():
    lists = dashboard.get()
    return render_template('dashboard.html', lists = lists)  

@app.route('/removeDashboard/')
@app.route('/removeDashboard/', methods=['GET','POST'])
def get_rm():
    lists = removeDashboard.get_rm()
    return render_template('removeDashboard.html', lists = lists)

app.add_url_rule('/addStudent/',
                view_func=AddStudent.as_view('addStudent'),
                methods=['GET', 'POST'])
                
app.add_url_rule('/addTeam/',
                view_func=AddTeam.as_view('addTeam'),
                methods=['GET', 'POST'])

app.add_url_rule('/removeStudent/',
                view_func=RemoveStudent.as_view('removeStudent'),
                methods=['GET', 'POST'])

app.add_url_rule('/removeTeam/',
                view_func=RemoveTeam.as_view('removeTeam'),
                methods=['GET', 'POST'])

if __name__ == '__main__':
  
    app.run(host='0.0.0.0', port=8000, debug=True)

import email
from email.policy import default
from enum import unique
from flask import Flask,render_template,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# creating a flask instance
app = Flask(__name__)
app.config['SECRET_KEY']="It's me"

#creating a form class
class UserForm(FlaskForm):
    name=StringField("What's Your Name?",validators=[DataRequired()])
    email=StringField("What's Your Email?",validators=[DataRequired()])
    submit=SubmitField("Submit")

class NamerForm(FlaskForm):
    name=StringField("What's Your Name?",validators=[DataRequired()])
    submit=SubmitField("Submit")

#add database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'

db=SQLAlchemy(app)

class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False,unique=True)
    date_added=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name=None
    form=UserForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user=Users(name=form.name.data,email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name=form.name.data
        form.name.data=''
        form.email.data=''
        flash("User Added Successfully")

    our_users=Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
    form=form,
    name=name,
    our_users=our_users)

@app.route('/')

def index():
    first_name="Rudra"
    favorite_pizza=["Cheese","Margeretta","phoini",41]
    stuff="This is bold text"
    return render_template('index.html',
    first_name=first_name,
    stuff=stuff,
    favorite_pizza=favorite_pizza)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',user_name=name)

#invalid url
@app.errorhandler(404)

def page_not_found(e):
    return render_template('404.html'), 404

#internal error found 

@app.errorhandler(500)

def page_not_found(e):
    return render_template('500.html'), 500

# create name page
@app.route('/name',methods=['GET','POST'])
def name():
    name=None
    form=NamerForm()
    #validate form 
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
        flash("Successfully Login!!!")
    return render_template('name.html',
    name=name,
    form=form)



if __name__=="__main__":
    app.run(debug=True)
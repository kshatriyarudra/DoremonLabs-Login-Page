'''Output of this project is to perform crud and learn about flask and flask modules'''

#render_template is used to generate output from a template file
#url_for is used for creating a URL to prevent the overhead of having to change URLs throughout an application
#To access the incoming data in Flask, you have to use the request object
#The request object holds all incoming data from the request
#redirect will returns a response object and redirects the user to another target location with specified status code
from flask import Flask, render_template,url_for,request,redirect

#Flask-SQLAlchemy provides a queryattribute on your Modelclass.
#When you access it you will get back a new query object over all records
from flask_sqlalchemy import SQLAlchemy

#If none of that works, Flask will assume the return value is a valid WSGI application and convert that into a response object.
#Since your datetime object does not meet 1, 2 or 3, Flask tries to treat it as 4 and call it as a WSGI application
from datetime import datetime

#__name__is the name of the current Python module. 
#The app needs to know where it’s located to set up some paths and __name__is a convenient way to tell it that.
app = Flask(__name__)

#Lets configure variable's directly into app.config and store the data in sqlite as test.db
#old db
#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'

#new db
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:rudra@localhost/test'
#object relational mapper (ORM) that enables Python to communicate with the SQL database(sqlite)
db = SQLAlchemy(app)

#The baseclass for model is called db.Model
class DoremonLabs(db.Model):
    #Use Column to define a column and use first argument as types(datatypes)
    #for id it is integer
    id = db.Column(db.Integer,primary_key=True)

    #for content it is String of length 250 
    content = db.Column(db.String(250),nullable=False)

    #for completed use integer
    completed = db.Column(db.Integer, default=0)

    #for creation date it is type of datetime
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    #pass the returned string of the object_name.__repr__ () method to 
    #the eval () function, you’ll get the same value as the object_name
    def __repr__(self):
        return '<Task %r>' % self.id

#Render a template when the route is triggered with GET method
#Read form inputs and register a user if route is triggered with POST
#route is a mapping of a URL with a function or any other piece of code to be rendered on the webserver
@app.route('/', methods=['POST','GET'])
def index():

    '''return render_template ("index.html") We have imported the render_template 
    function from the Flask module and added a route'''

    #POST request is used as an HTTP protocol method that enables users to send HTML form data to server
    if request.method == 'POST':

        #reading the content or to access form data in our route, we use request.form
        project_content = request.form['content']

        #pass the new project content to todo
        project_task=DoremonLabs(content=project_content)

        try:
            #creates the session at the request start 
            #and it destroys it at the request end
            db.session.add(project_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There is an issue adding your task"
    else:
        projects = DoremonLabs.query.order_by(DoremonLabs.date_created).all()
        return render_template('index.html',projects=projects)

@app.route('/delete/<int:id>')
def delete(id):

    '''this function is used for deleting an id from the todo'''

    #query.get_or_404 we can call it to class object and return the object
    project_to_delete = DoremonLabs.query.get_or_404(id)

    try:
        #unlink the project using session.delete
        db.session.delete(project_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem when deleting that projects"

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):

    '''this function is for updating any information when we need to change'''

    project = DoremonLabs.query.get_or_404(id)
    if request.method=='POST':
        project.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue while updating project"
    else:
        return render_template('update.html',project=project)

if __name__=="__main__":

    #app.run(debug=True) making available the code you need to build web apps with flask
    app.run(debug=True)
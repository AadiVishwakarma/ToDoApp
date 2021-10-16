from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date
app = Flask(__name__)

#<<<""for database"">>>
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"

#<to handle a warning>
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
 

#<< defining table structure in class for database>>
class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(300), nullable = False)
    desc = db.Column(db.String(1000), nullable = False)
    date_created = db.Column(db.Date,default = date.today , nullable = False)

# what do you want to print-- > repr function is used
    def __repr__(self) -> str:
        return f"{self.sno} - {self. title}"

#routes
@app.route('/', methods  = ['GET', 'POST'])
def hello_world():

    if request.method =="POST":
        title = request.form['title']
        desc=  request.form['desc']
        #print(request.form['title'])
    
        #create instance
        todo = ToDo(title = title , desc = desc )
        db.session.add(todo)
        db.session.commit()
    alltodo = ToDo.query.all()
    
    return render_template('index.html',alltodo = alltodo)

@app.route('/show')
def show():
    alltodo = ToDo.query.all()
    print(alltodo)
    return 'this is products page'

@app.route('/modify/<sno>', methods =['GET','POST'])
def modify(sno):
    if request.method == "POST":
        title = request.form['title']
        desc=  request.form['desc']
    
        #create instance
        alltodo = ToDo.query.filter_by(sno=sno).first()
        alltodo.title = title
        alltodo.desc = desc
        db.session.add(alltodo)
        db.session.commit()
        return redirect("/")
        
    alltodo = ToDo.query.filter_by(sno=sno).first()

    return render_template('update.html',alltodo = alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    alltodo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask , render_template,request,redirect,url_for
from sqlalchemy import text
from sqlalchemy.sql.expression import func
from model import *
from flask_restful import Api
#from api import *
import os


current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)  

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(current_dir, "database.sqlite3")


db.init_app(app)

app.app_context().push()


@app.route("/",methods=['POST','GET'])
def into():
    user_type = request.form.get('userType')

    if user_type == 'user':
        # Redirect to /user if the user is a regular user
        return redirect(url_for('login'))
    elif user_type == 'librarian':
        # Redirect to /admin if the user is an admin
        # return redirect(url_for('librarian'))
        return render_template("adaccess.html")
    return render_template("into.html")



@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        valueemail=request.form['email']
        valuepassword=request.form['password']
        if Users.query.filter(Users.email==valueemail and Users.password == valuepassword).first():
            return redirect(url_for('home'))
        return redirect(url_for('signup'))       
    return render_template("login.html")

@app.route("/signup",methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        valueusername = request.form['username']
        valueemail = request.form['email']
        valuepassword = request.form['password']

        if not Users.query.filter(Users.email == valueemail).all():
                newuser = Users(username=valueusername,email=valueemail,password=valuepassword)
                db.session.add(newuser)
                db.session.commit()
                return redirect(url_for('into'))#use func name for redirect
        return render_template("signup.html", error='This user already exists')
    
    return render_template('signup.html')



@app.route("/home")
def home():
    listofbooks = Books.query.all()
    return render_template("page.html", read = listofbooks) 


@app.route("/Stats")
def Stats():
    return render_template("Stats.html")

@app.route("/Statsadm")
def Statsadm():
    return render_template("Statsadm.html")

@app.route("/requestb", methods=['POST','GET'])
def requestb():
    if request.method == 'POST':
        book_id = int(request.form['bookId'])
        # Process the request here...
    # Assuming the request processing is successful, redirect back to page.html
    return redirect('/home')

@app.route("/MyBooks", methods=['POST','GET'])
def MyBooks():
    if request.method=='POST':
        value=request.form["searchKey"]
        print(value) 
    return render_template("MyBooks.html")

@app.route("/add")
def add():
    return "Data was added"

@app.route("/filter", methods=["POST"])
def filter():
    value=request.form['searchKey']
    searchType= request.form['filterOptions']

    if searchType == "name":
        result = Books.query.filter(Books.name.like('%'+value+'%')).all()
    elif searchType == "section":
        value=value.name()
        result = Books.query.filter(Books.section.any(type=value)).all()
    elif searchType == "author":
        result = Books.query.filter(Books.author.like(value+'%')).all()
   
    return render_template("filter.html",data=result)
    
#password for librarian access: sumit_nehra
@app.route("/librarian",methods=['POST','GET'])
def librarian():
    if request.method == 'POST':
        if request.form['formtype']=='add':
            valuetitle = request.form['name']
            valuerating = request.form['rating']
            valueposter = request.form['poster']

            if Books.query.filter(Books.title == valuetitle).first() == None:
                newdata = Books(title=valuetitle,rating=valuerating,poster=valueposter)
                db.session.add(newdata)
                db.session.commit()
                return "new movie added"
            else:
                return "try adding a new movie"
        elif request.form['formtype']=='delete':
            valuetitle = request.form['title']
            tobedelted= Books.query.filter(Books.title == valuetitle).first()
            if tobedelted:
                db.session.delete(tobedelted)
                db.session.commit()
                return "movie deleted"
            else:
                return "movie does not exist"

    
    return render_template("librarian.html")


@app.route("/api")
def Demoapi():
    return render_template("api.html")


if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run(host='0.0.0.0')
































if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run(host='0.0.0.0')
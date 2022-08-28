from flask import Flask, render_template, request, flash
import redis

def creat_app():
    app = Flask(__name__)
    app.secret_key = 'secretkey'
    #Create a redis database instanse
    r = redis.Redis(host='localhost', port = 6379)
    @app.route("/")
    def home():
        return render_template("home.html")
    @app.route("/students")
    def index():
        #List_of_students = []
        flash ("Give the name of the student to add to the database")
        return render_template("index.html")

    @app.route("/add", methods = ["POST"])
    def add():
        try :
            id = r.get('id').decode('UTF-8')
        except:
            r.incr('id')
            id = r.get('id').decode('UTF-8')
        if (id=='id'):
            r.incr('id')
            id = r.get('id').decode('UTF-8')
        r.set(id,str(request.form['student_name']))
        r.incr('id')
        flash ('A new student name was added to the list, Please change end of URL to "/liststudents" to see the list of student names')
        print('The student was added to the database:',str(request.form['student_name']))
        return render_template("index.html")

    @app.route("/liststudents", methods = ["POST","GET"])
    def liststudents():
        studentslist = []
        keys = r.keys()
        val = {}
        for i in keys:
            if (i.decode("UTF-8")!= 'id'):
                val[i.decode("UTF-8")]=str(r.get(i.decode("UTF-8")).decode("UTF-8"))
        flash ('The name of students in the database are:')
        return render_template("index.html", val = val)

    @app.route("/remove", methods = ["POST"])
    def remove():
        r.flushdb()
        print('Database reset')
        flash ('The list on names has been reset to initial state successfully')
        return render_template("index.html")
    return app

    app = creat_app()
    app.run(debug=True) 


from flask import Flask, request, redirect, session

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# DATABASE
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))


# HOME
@app.route('/')
def home():

    if 'user' in session:

        return f"""
        <html>
        <head>

        <style>

        body{{
            margin:0;
            font-family:Arial;
            background:linear-gradient(135deg,#1e3c72,#2a5298,#00c6ff);
            background-size:400% 400%;
            animation:bg 8s infinite alternate;
            color:white;
            text-align:center;
        }}

        @keyframes bg{{
            0%{{background-position:left;}}
            100%{{background-position:right;}}
        }}

        .box{{
            width:350px;
            margin:120px auto;
            padding:40px;
            background:rgba(255,255,255,0.15);
            border-radius:20px;
            backdrop-filter:blur(10px);
            box-shadow:0px 0px 20px rgba(0,0,0,0.4);
            animation:zoom 1s;
        }}

        @keyframes zoom{{
            from{{transform:scale(0.5);opacity:0;}}
            to{{transform:scale(1);opacity:1;}}
        }}

        a{{
            text-decoration:none;
            color:white;
            background:red;
            padding:10px 20px;
            border-radius:10px;
        }}

        </style>

        </head>

        <body>

        <div class="box">

        <h1>Welcome {session['user']}</h1>

        <br>

        <a href='/logout'>Logout</a>

        </div>

        </body>
        </html>
        """

    return redirect('/login')


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        old_user = User.query.filter_by(username=username).first()

        if old_user:
            return "User already exists"

        new_user = User(username=username, password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return """
    <html>

    <head>

    <style>

    body{
        margin:0;
        font-family:Arial;
        background:linear-gradient(135deg,#ff512f,#dd2476,#1e90ff);
        background-size:400% 400%;
        animation:bg 8s infinite alternate;
    }

    @keyframes bg{
        0%{background-position:left;}
        100%{background-position:right;}
    }

    .box{
        width:350px;
        margin:80px auto;
        padding:40px;
        background:white;
        border-radius:20px;
        text-align:center;
        animation:slide 1s;
        box-shadow:0px 0px 20px rgba(0,0,0,0.4);
    }

    @keyframes slide{
        from{transform:translateY(-100px);opacity:0;}
        to{transform:translateY(0);opacity:1;}
    }

    input{
        width:90%;
        padding:12px;
        margin:10px;
        border-radius:10px;
        border:1px solid gray;
    }

    button{
        background:#1e90ff;
        color:white;
        border:none;
        padding:12px 25px;
        border-radius:10px;
        cursor:pointer;
        transition:0.3s;
    }

    button:hover{
        transform:scale(1.1);
        background:#ff1493;
    }

    a{
        color:blue;
    }

    </style>

    </head>

    <body>

    <div class="box">

    <h1>Register</h1>

    <form method='POST'>

    <input type='text' name='username' placeholder='Enter Username' required>

    <input type='password' name='password' placeholder='Enter Password' required>

    <button type='submit'>Register</button>

    </form>

    <br>

    Already have account?
    <a href='/login'>Login</a>

    </div>

    </body>
    </html>
    """


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            session['user'] = username
            return redirect('/')

        return "<h2 style='color:red;text-align:center'>Invalid Username or Password</h2>"

    return """
    <html>

    <head>

    <style>

    body{
        margin:0;
        font-family:Arial;
        background:linear-gradient(135deg,#00c6ff,#0072ff,#8e2de2);
        background-size:400% 400%;
        animation:bg 8s infinite alternate;
    }

    @keyframes bg{
        0%{background-position:left;}
        100%{background-position:right;}
    }

    .box{
        width:350px;
        margin:80px auto;
        padding:40px;
        background:white;
        border-radius:20px;
        text-align:center;
        animation:slide 1s;
        box-shadow:0px 0px 20px rgba(0,0,0,0.4);
    }

    @keyframes slide{
        from{transform:translateY(-100px);opacity:0;}
        to{transform:translateY(0);opacity:1;}
    }

    input{
        width:90%;
        padding:12px;
        margin:10px;
        border-radius:10px;
        border:1px solid gray;
    }

    button{
        background:#0072ff;
        color:white;
        border:none;
        padding:12px 25px;
        border-radius:10px;
        cursor:pointer;
        transition:0.3s;
    }

    button:hover{
        transform:scale(1.1);
        background:#ff1493;
    }

    a{
        color:blue;
    }

    </style>

    </head>

    <body>

    <div class="box">

    <h1>Login</h1>

    <form method='POST'>

    <input type='text' name='username' placeholder='Enter Username' required>

    <input type='password' name='password' placeholder='Enter Password' required>

    <button type='submit'>Login</button>

    </form>

    <br>

    New User?
    <a href='/register'>Register</a>

    </div>

    </body>
    </html>
    """


# LOGOUT
@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/login')


# RUN
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
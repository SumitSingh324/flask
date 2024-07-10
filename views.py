from app import app
from flask import request, render_template, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt 
from flask_wtf import CSRFProtect 
from models import User, db
from flask_session import Session 
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, logout_user
from mail import generate_confirmation_token, confirm_token
from flask_mail import Mail, Message
from mail import mail

bcrypt = Bcrypt(app)
csrf = CSRFProtect(app) 

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)

@app.route("/", methods=['GET','POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    elif request.method=='GET':
        return render_template("index.html")

    else:
        password=request.form.get("password")
        user = User(name=request.form.get("name"),password=bcrypt.generate_password_hash(password).decode('utf-8'), email=request.form.get("email"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    elif request.method=='GET':
        return render_template("login.html")

    else:
        user = User.query.filter_by(email=request.form.get("email")).first()
        if user:
            if bcrypt.check_password_hash(user.password, request.form.get("password")):
                db.session.add(user)
                db.session.commit()
                if login_user(user,remember=False):
                    flash("logged in", "success")
                    return redirect(url_for("home"))
                else:
                    return "Failed to log in"
            else:
                flash("Wrong Credentials", "warning")
                return render_template("login.html")
        
@app.route("/home")
def home():
    if current_user.is_authenticated:
        return render_template("home.html")
    else:
        flash("Please log in first", "info")
        return redirect(url_for("login"))

# @login_manager.unauthorized_handler
# def unauthorized():
#     flash("You must be logged in to access this page.", "error")
#     return redirect(url_for("login"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/forgot")
def forgot_password():
    return render_template("forgot_password.html")


@app.route("/send", methods=['GET','POST'])
def send_email():
    email = request.form.get('email')
    user=User.query.filter_by(email=email).first()
    if user:
        msg = Message( 
                'Hello', 
                sender ='manish@thoughtwin.com', 
                recipients = [email] 
               ) 
        token = generate_confirmation_token(email)
        msg.body = f"http://127.0.0.1:5000/update/{token}"
        mail.send(msg) 
        flash("Reset link has been sent on your mail", "success")
        return render_template("login.html")
    else:
        flash("Email is not present", "warning")
        return render_template("index.html")

@app.route("/update/<token>", methods=['GET','POST'])
def update_password(token):
    if request.method=='GET':
        return render_template("update_password.html",token=token)
    else:
        password = request.form.get('password')
        email = confirm_token(token)
        user = User.query.filter_by(email=email).first()
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.commit()
        flash("password has been updated", "success")
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
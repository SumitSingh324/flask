from app import app
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer


mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'manish@thoughtwin.com'
app.config['MAIL_PASSWORD'] = 'xpdd stad tfjw lush'
app.config['MAIL_USE_TLS'] = True

mail = Mail(app) 

app.config['SECURITY_PASSWORD_SALT']='sumit@123'


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


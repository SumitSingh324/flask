from flask import Flask
from flask_bootstrap import Bootstrap4, Bootstrap

app = Flask(__name__)
app.secret_key = b'_53oi3uriq9pifpff;apl'

bootstrap = Bootstrap4(app)

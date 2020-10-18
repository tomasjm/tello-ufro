from flask import Flask
app = Flask(__name__)
# Mínima aplicación de Flask
@app.route('/')
def hello_world():
    return 'Hello, World!'
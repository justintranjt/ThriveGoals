# Simply test app with command "python thriveApp.py" and navigate to 
# localhost:5000 in your browser

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run()

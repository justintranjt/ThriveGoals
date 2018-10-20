# Simply test app with command "python thriveApp.py" and navigate to 
# localhost:5000 in your browser

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/register' # createdb register (in postgress.app)
db = SQLAlchemy(app)


# source: http://blog.sahildiwan.com/posts/flask-and-postgresql-app-deployed-on-heroku/
# Create database model. Right now, only saving the netid's. In future, goals, tasks, etc. will be added.
# this may tie into CAS ?
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

# Save e-mail to database and send to success page
@app.route('/register', methods=['POST'])
def prereg():
    email = None
    if request.method == 'POST':
        email = request.form['email'] # may not be needed
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
            # return render_template('success.html') # don't have html pages set up
    # return render_template('index.html')




@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run()

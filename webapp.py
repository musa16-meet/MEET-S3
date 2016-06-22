from flask import Flask, render_template, request, redirect, url_for
from flask import session as web_session
app = Flask(__name__)


#SQLAlchemy stuff
from database import Base, User, Contact #tables
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///Webpage.db')
Base.metadata.create_all(engine) 
DBSession = sessionmaker(bind=engine)
session = DBSession()
#APP CODE GOES HERE

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
	if request.method == 'GET':
		return render_template('signup.html')
	else:
		new_firstname = request.form['first_name']
		new_lastname = request.form['last_name']
		new_email = request.form['email']
		new_username = request.form['username']
		new_password = request.form['password']
		person = User(first_name = new_firstname, last_name = new_lastname, email = new_email, username = new_username, password = new_password)
		session.add(person)
		session.commit()

		return redirect(url_for('view_profile', user_id = person.id))


@app.route("/login", methods = ['GET', 'POST'])
def login():
	error = None
	if request.method == 'GET':
		return render_template('login.html')
	else:
		web_session['username'] = request.form['username']
		person = session.query(User).filter_by(username = request.form['username']).first()
		if person == None:
			error = 'User does not exist '
			return render_template('login.html', error = error)
		else:
			return redirect(url_for('view_profile', user_id = person_id))


@app.route("/profile/<int:user_id>")
def view_profile(user_id):
	person = session.query(User).filter_by(id = user_id).first()
	return render_template('view_profile.html', person = person)


@app.route("/delete/<int:user_id>")
def delete():
	person = session.query(User).filter_by(id = user_id).first()
	if request.method == 'GET':
		return render_template('delete.html', person = person)
	else:
		session.delete(person)
		session.commit()
		return redirect(url_for('home'))


@app.route("/aboutus")
def aboutus():
	return render_template('aboutus.html')



if __name__ == '__main__':
    app.run(debug=True)
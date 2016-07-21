from flask import Flask, render_template, request, redirect, url_for
from flask import session as web_session
app = Flask(__name__)

app.secret_key = 'MEETS3'
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
		confirm_password = request.form['confirm_password']
		print ("beginig of the test")
		print (confirm_password)
		print (new_password)
		print ("the end of the test")
		if confirm_password == new_password:
			person = User(first_name = new_firstname, last_name = new_lastname, email = new_email, username = new_username, password = new_password)
			session.add(person)
			session.commit()
			return redirect(url_for('view_profile', user_id = person.id))
		else:
			error = 'The passwords do not match'
			return error


@app.route("/login", methods = ['GET', 'POST'])
def login():
	error = None
	if request.method == 'GET':
		return render_template('login.html')
	else:
		web_session['email'] = request.form['email']
		person = session.query(User).filter_by(email = request.form['email']).first()
		if person == None:
			error = 'User does not exist '
			return render_template('login.html', error = error)
		else:
			if person.password == request.form['password']:
				return redirect(url_for('view_profile', user_id = person.id))
			return render_template('login.html', error = error)


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

@app.route("/contact", methods = ['POST','GET'])
def contactus():

	if request.method == 'GET':
		return render_template('contactus.html')

	else:
		user_name = request.form['name']
    	user_email = request.form['email']
    	user_message = request.form['message']
    	msg = Contact(name = user_name, email = user_email, messege= user_message)
    	session.add(msg)
    	session.commit()
    	return render_template('sent.html')



@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_profile(user_id):
    person = session.query(User).filter_by(id=user_id).first()
    print([person])
    if request.method == 'GET':
        return render_template('edit_profile.html', person = person)
    else:
        new_username = request.form['username']
        new_password = request.form['password']
        new_conpass = request.form['conpass']
        new_email = request.form['email']


        person.username = new_username
        person.password = new_password
        person.email = new_email

        session.commit()

        return redirect(url_for('view_profile', user_id = person.id))


@app.route("/aboutus")
def aboutus():
	return render_template('aboutus.html')

@app.route("/newsfeed")
def newsfeed(user_name):
	person = session.query(User).filter_by()

	return render_template('newsfeed.html/<username>')


if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug=True)
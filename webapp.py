from flask import Flask, render_template, request, redirect, url_for, flash
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
		picture = ""
		question = ""
		A1 = ""
		A2 = ""
		A3 = ""

		if confirm_password == new_password:
			person = User(first_name = new_firstname, picture = picture, last_name = new_lastname, email = new_email, username = new_username, password = new_password)
			session.add(person)
			session.commit()
			return redirect(url_for('newsfeed', user_id = person.id))
		else:
			return render_template('signup.html')



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
			web_session['id'] = person.id
			if person.password == request.form['password']:
				return redirect(url_for('newsfeed', user_id = person.id)) #, user_id = person.id)
			return render_template('login.html', error = error)




@app.route("/profile/<int:user_id>", methods = ['POST', 'GET'])
def view_profile(user_id):
	if request.method == 'POST':
		person = session.query(User).filter_by(id = user_id).first()
		return render_template('view_profile.html', person = person, user_id = person.id)
	else:
		return render_template('view_profile.html')


@app.route("/delete/<int:user_id>", methods = ["GET", "POST"])
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
    print("EDIT ")
    person = session.query(User).filter_by(id=user_id).first()
    web_session['id'] = person.id
    if request.method == 'GET':
        return render_template('edit_profile.html', person = person)
    else:
        print("POSTING edit")
        new_username = request.form['username']
        new_password = request.form['pass']
        new_conpass = request.form['conpass']
        new_email = request.form['email']
        new_firstname = request.form['first_name']
        new_lastname = request.form['last_name']
        new_picture = request.form['picture']
        new_location = request.form['location']
        new_question = request.form['question']
        new_A1 = request.form['A1']
        new_A2 = request.form['A2']
        new_A3 = request.form['A3']



        person.username = new_username
        person.password = new_password
        person.email = new_email
        person.first_name = new_firstname
        person.last_name = new_lastname
        person.picture = new_picture
        person.location = new_location
        person.question = new_question
        person.A1 = new_A1
        person.A2 = new_A2
        person.A3 = new_A3

        session.commit()

        return redirect(url_for('newsfeed', user_id = person.id))


@app.route("/aboutus")
def aboutus():
	return render_template('aboutus.html')

	

@app.route("/newsfeed/<int:user_id>", methods = ['GET', 'POST'])
def newsfeed(user_id):
	num = len(session.query(User).all())
	var = request.args.get('next')
	new_id = user_id
	if(var != None):
		if(web_session['id']== user_id + int(var)):
			user_id += int(var)
		if(var == '-1'):
			new_id = num if user_id == 1 else user_id-1
		if(var == "1"):
			new_id = 1 if user_id == num else user_id+1
		if(new_id == web_session['id']):
			new_id += int(var)
		return redirect(url_for('newsfeed', user_id=new_id))

	person = session.query(User).filter_by(id = new_id).first()
	return render_template("newsfeed.html",person = person)




@app.route("/chatroom", methods = ['GET','POST'])
def chatroom():
	user_id = request.args.get("chatusr")
	x = request.args.get("x")
	y = request.args.get("y")
	print(x)
	print(y)
	person = session.query(User).filter_by(id = user_id).first()
	print(person)
	return render_template('chatroom.html', person = person)



@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')


if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug=True)
 
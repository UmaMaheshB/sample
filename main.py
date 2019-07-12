# Another example chaining Bokeh's to Flask.

from flask import Flask, render_template, flash, request, session
from flask_login import LoginManager,login_user,current_user,logout_user,login_required
from database_setup import Owner
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base

app = Flask(__name__)

engine = create_engine("sqlite:///mydb.db", 
	                    connect_args={'check_same_thread':False},
	                    echo=True)

Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/nav")
def nav():
    return render_template("index.html")

@app.route("/login",methods=["POST","GET"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	try:
		if request.method == "POST":
			owner=session.query(Owner).filter_by(email=request.form['email'],password=request.form['password']).first()
			print("\n\n\n\n",owner)
			if owner:
				login_user(owner)
				next_page=request.args.get('next')
				return redirect(next_page) if next_page else redirect(url_for('home'))
			else:
				flash("Login Failed, Please Check & Try Again ...!","danger")
				return "else"
		else:
			return render_template("userlogin.html",title="Login")
	except Exception as e:
		print("\n\n\n\n\nerrorrrrrrrrrrrr",e)
		flash("Login Failed, Please Check & Try Again ...!","danger")
		return render_template("userlogin.html",title="Login")

@app.route('/logout')
def logout():
	logout_user()
	return render_template("userlogin.html")



if __name__ == "__main__":
	app.config['SECRET_KEY']='jhgklgkl,hbjb'
	login_manager=LoginManager(app)
	login_manager.login_view='login'
	login_manager.login_message_category='info'

	@login_manager.user_loader
	def load_user(user_id):
		return session.query(Owner).get(int(user_id))
	app.debug = True
	app.run(host='0.0.0.0' ,port=5000)
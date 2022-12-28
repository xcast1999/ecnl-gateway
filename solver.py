import requests as req,json , sqlite3

from flask import Flask , jsonify ,request, send_file , render_template
from uuid import uuid4
from flask_cors import CORS
  
app = Flask(__name__)
CORS(app)

con = sqlite3.connect("AUTHORIZE",check_same_thread=False)

@app.errorhandler(404)
def page_not_found(e):

	result = {"result":False,"word":"None"}
	
	return jsonify(result), 404


@app.route("/add/<username>")
def add_user(username):
  
	query = con.execute(f"INSERT OR REPLACE INTO tblUsers (user_name) VALUES ('{username}')")

	con.commit()

	return "Added Successfully"


@app.route("/authorize/<username>")
def authorize(username):

	users = con.execute(f"SELECT * FROM tblUsers WHERE user_name = '{username}'").fetchone()

	if users is not None:

		user_session = uuid4()
  
		query = con.execute(f"UPDATE tblUsers SET user_session = '{user_session}' WHERE user_name = '{username}'")

		con.commit()
	
	else:

		user_session = "Not Authorized"

	return str(user_session)


@app.route("/")
def hello_world():
  
  return 'Hello Ecandl.net'

# if __name__ == '__main__':
# 	app.run(debug=True, port=5000)
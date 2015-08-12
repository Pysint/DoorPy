import sqlite3, datetime, subprocess, os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flask_bootstrap import Bootstrap
from flask.ext.bcrypt import Bcrypt
import settings as sett  

# configuration
DATABASE = sett.database
DEBUG = sett.debug
SECRET_KEY = sett.secretkey

# Create application
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('app_settings', silent=True)
Bootstrap(app)
bcrypt = Bcrypt(app)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()
    #Global variables
    g.sitename = sett.name
    g.siteslogan = sett.slogan

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# Routes
@app.route('/')
def home():
    if session.get('logged_in'):    
    	cur = g.db.execute('select * from news order by id desc, date asc')
    	entries = [dict(title=row[1], content=row[2], date=row[3]) for row in cur.fetchall()]
        return render_template('home.html', entries=entries)
    else:
    	return render_template('home.html')

@app.route('/add-news', methods=['GET','POST'])
def add_news():
    if not session.get('logged_in'):
        abort(404)
    if not session['admin'] == True:
        abort(404)
    if request.method == 'POST':
   	g.db.execute('insert into news (title, content, date) values (?, ?, ?)', \
[request.form['title'], request.form['content'], datetime.datetime.now().strftime('%d-%m-%Y %H:%M')])
    	g.db.commit()
    	flash('Newsitem successfully posted', 'success')
    	return redirect(url_for('home'))
    else: 
   	return render_template('addnews.html')

@app.route('/add-user', methods=['GET','POST'])
def add_user():
    if not session.get('logged_in'):
        abort(404)
    if not session['admin'] == True:
        abort(404)
    if request.method == 'POST':
	pwd = request.form['pwd']
    	if pwd != request.form['pwdc']:
		flash('Sorry, new password and verification do not match. :(', 'error')
   		return render_template('adduser.html')
    	else:
		pwd_hash = bcrypt.generate_password_hash(pwd)
		g.db.execute('insert into users (username, realname, password) values (?, ?, ?)', \
[request.form['uname'], request.form['rname'], pwd_hash])
    		g.db.commit()
    		flash('User successfully added', 'success')
		return redirect(url_for('home'))
    else: 
   	return render_template('adduser.html')

@app.route('/account', methods=['GET','POST'])
def account():
    cur = g.db.execute("select * from users where username = (?)", (session['user'],))
    fromusers = [dict(id=row[0], username=row[1], realname=row[2],) for row in cur.fetchall()]
    if not session.get('logged_in'):
        abort(404)
    if request.method == 'POST':
	old = request.form['pwold']
	new1 = request.form['pwnew1']
	new2 = request.form['pwnew2']
	
    	if (old and new1 and new2):
		if new1 != new2:
			flash('Sorry, new password and verification do not match.', 'error')
		else:
			pwdquery = g.db.execute("select password from users where username = (?)", (session['user'],))
			(pwd,) = pwdquery.fetchone()
			pcheck = bcrypt.check_password_hash(pwd, old)
			if pcheck is True:
				newhash = bcrypt.generate_password_hash(new1)
				g.db.execute("UPDATE users SET password= (?) WHERE username= (?)", (newhash, session['user'],))
    				g.db.commit()
				flash('Password successfully changed.', 'success')
			else:
				flash('Sorry, your old password is incorrect.','error')
	else:
		flash('Error, not all field filled in.', 'error')
	
    return render_template('account.html', user=fromusers)

@app.route('/status')
def status():
    if not session.get('logged_in'):
        abort(404)
    return render_template('status.html')

@app.route('/log')
def log():
    if not session.get('logged_in'):
        abort(404)
    else:
    	cur = g.db.execute('select * from doorlogs order by id asc')
    	logs = [dict(id=row[0], date=row[1], description=row[2], note=row[3]) for row in cur.fetchall()]
        return render_template('log.html', logs=logs)

@app.route('/delete-log/<log_id>', methods=['POST'])
def delete_log(log_id):
    if not session.get('logged_in'):
        abort(404)
    else:
        g.db.execute("delete from doorlogs where id=?", [log_id])
        g.db.commit()
        flash('Log has been deleted','success')
        return redirect(url_for('log'))

@app.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
                usrin = request.form['username']
                pwdin = request.form['password']
                if pwdin and usrin:
                        usr = g.db.execute("select count(*) from users where username = (?)", (usrin,))
                        if usr.fetchone()[0]:
                                pwdquery = g.db.execute("select password from users where username = (?)", (usrin,))
                                (pwd,) = pwdquery.fetchone()
                                pcheck = bcrypt.check_password_hash(pwd, pwdin)
                                if pcheck is True:
                                        qry = g.db.execute("select realname from users where username = (?)", (request.form['username'],))
                                        name = "".join(qry.fetchone())
                                        session['logged_in'] = True
                                        if usrin == "hugo": 
                                                session['admin'] = True
                                        else:   
                                                session['admin'] = False 
                                        session['user'] = request.form['username']
                                        flash('Welcome ' + name, 'info') 
                                        return redirect(url_for('home'))
                                else:   
                                        flash('Invalid username and/or password','error')
                        else:
                                flash('Invalid username and/or password','error')
                else:
                        flash('Please fill out all fields','error')
        return render_template('login.html')

@app.route('/profile/<profile_id>')
def profile_details(profile_id):
    if not session.get('logged_in'):
        abort(404)
    cur = g.db.execute('select * from profiles where id = ?', [profile_id])
    profiles = [dict(id=row[0], edited=row[1], firstname=row[2], lastname=row[3], company=row[4]) for row in cur.fetchall()]
    if profiles:
       	g.id = str(profile_id)
	return render_template('profiles.html', profile=profiles)
    else:
	flash("That user doesn't exist, u mad bruh? :(", 'error')
	return redirect(url_for('overview'))

@app.route('/logout')
def logout():
    if not session.get('logged_in'):
        abort(404)
    session.pop('logged_in', None)
    flash('You were logged out', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(host='0.0.0.0')

from flask import Flask, render_template, g, request, redirect, url_for
import os
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'flunschlist.db'),
    SECRET_KEY='secret',
    USERNAME='admin',
    PASSWORD='flunsch'
))

def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()
		
def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()
	
@app.cli.command('initdb')
def initdb_command():
	init_db()
	print "Database initialized"
	
@app.route('/')
def show_entries():
	flunsch_dict = {}
	db = get_db()
	
	cur = db.execute('select name from flunscher')
	flunscher = cur.fetchall()
	print flunscher
	for flser in flunscher:
		flunsch_dict[flser[0]] = []
	
	cur2 = db.execute('select flunschs.title, flunschs.owner, flunscher.name, flunschs.description, flunschs.id from flunschs inner join flunscher on flunschs.owner=flunscher.id')
	flunschs = cur2.fetchall()
	print flunschs
	for flunsch in flunschs:
		flunsch_dict[flunsch[2]].append({"title" : flunsch[0], "description" : flunsch[3], "id" : flunsch[4]})
		
	return render_template('index.html', fls = flunsch_dict)

@app.route('/add_flunsch', methods=['POST'])
def add_flunsch():
	db = get_db()
	cur = db.execute('select name, id from flunscher where name= ?', [request.form['name']])
	flunscher = cur.fetchall()
	return render_template('addflunsch.html', flser = flunscher)

@app.route('/add_flunsch_to_db', methods=['POST'])
def add_flunsch_to_db():
	db = get_db()
	print request.form['title']
	db.execute('insert into flunschs (title, owner, description) values (?, ?, ?)',
				[request.form['title'], request.form['owner'], request.form['desc']])
	db.commit()
	return redirect(url_for('show_entries'))

@app.route('/remove_flunsch', methods=['POST'])
def remove_flunsch_from_db():
	db = get_db()
	print request.form['id']
	db.execute("delete from flunschs where id=?", [request.form['id']])
	db.commit()
	return redirect(url_for('show_entries'))

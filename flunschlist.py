from flask import Flask, render_template, g, request, flash, redirect, url_for
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
	db = get_db()
	cur = db.execute('select flunschs.title, flunschs.owner, flunscher.name from flunschs inner join flunscher on flunschs.owner=flunscher.id')
	flunschs = cur.fetchall()
	print flunschs
	flunsch_dict = {}
	for flunsch in flunschs:
		if flunsch[2] not in flunsch_dict:
			flunsch_dict[flunsch[2]] = []
		flunsch_dict[flunsch[2]].append(flunsch[0])
		
	return render_template('index.html', fls = flunsch_dict)

@app.route('/add_flunsch', methods=['POST'])
def add_flunsch():
	db = get_db()
	cur = db.execute('select name, id from flunscher')
	flunscher = cur.fetchall()
	print flunscher
	return render_template('addflunsch.html', flser = flunscher)

@app.route('/add_flunsch_to_db', methods=['POST'])
def add_flunsch_to_db():
	db = get_db()
	db.execute('insert into flunschs (title, owner, desc) values (?, ?, ?)',
				[request.form['title'], request.form['owner'], request.form['desc']])
	db.commit()
	flash("Added Flunsch!")
	return redirect(url_for('show_entries'))

@app.route('/remove_flunsch', methods=['POST'])
def remove_flunsch_from_db():
	db = get_db()
	print request.form['title']
	db.execute("delete from flunschs where title=?", [request.form['title']])
	db.commit()
	return redirect(url_for('show_entries'))

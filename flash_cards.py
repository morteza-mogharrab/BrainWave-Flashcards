import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

# Create Flask application instance
app = Flask(__name__)

# Configuration settings
app.config.from_object(__name__)

# Load default configuration and override settings from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db', 'cards.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('CARDS_SETTINGS', silent=True)

# Connect to the database
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

# Get the database connection
def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# Close the database connection at the end of the request
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# Route for the home page
@app.route('/')
def index():
    """Redirects to the appropriate page based on whether the user is logged in or not."""
    if session.get('logged_in'):
        return redirect(url_for('general'))
    else:
        return redirect(url_for('login'))

# Route for displaying all cards
@app.route('/cards')
def cards():
    """Displays all cards."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    query = '''
        SELECT id, type, front, back, known
        FROM cards
        ORDER BY id DESC
    '''
    cur = db.execute(query)
    cards = cur.fetchall()
    return render_template('cards.html', cards=cards, filter_name="all")

# Route for filtering cards based on type
@app.route('/filter_cards/<filter_name>')
def filter_cards(filter_name):
    """Filters and displays cards based on the specified filter."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    filters = {
        "all":          "where 1 = 1",
        "general":      "where type = 1",
        "academic":     "where type = 2",
        "personal":     "where type = 3",
        "mastered":     "where known = 1",
        "amateur":      "where known = 0",
    }

    query = filters.get(filter_name)

    if not query:
        return redirect(url_for('cards'))

    db = get_db()
    fullquery = "SELECT id, type, front, back, known FROM cards " + query + " ORDER BY id DESC"
    cur = db.execute(fullquery)
    cards = cur.fetchall()
    return render_template('cards.html', cards=cards, filter_name=filter_name)

# Route for adding a new card
@app.route('/add', methods=['POST'])
def add_card():
    """Adds a new card to the database."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    db.execute('INSERT INTO cards (type, front, back) VALUES (?, ?, ?)',
               [request.form['type'],
                request.form['front'],
                request.form['back']
                ])
    db.commit()
    flash('New card was successfully added.')
    return redirect(url_for('cards'))

# Route for editing a card
@app.route('/edit/<card_id>')
def edit(card_id):
    """Displays the form for editing a card."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    query = '''
        SELECT id, type, front, back, known
        FROM cards
        WHERE id = ?
    '''
    cur = db.execute(query, [card_id])
    card = cur.fetchone()
    return render_template('edit.html', card=card)

# Route for saving edited card details
@app.route('/edit_card', methods=['POST'])
def edit_card():
    """Updates the details of an edited card."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    selected = request.form.getlist('known')
    known = bool(selected)
    db = get_db()
    command = '''
        UPDATE cards
        SET
          type = ?,
          front = ?,
          back = ?,
          known = ?
        WHERE id = ?
    '''
    db.execute(command,
               [request.form['type'],
                request.form['front'],
                request.form['back'],
                known,
                request.form['card_id']
                ])
    db.commit()
    flash('Card saved.')
    return redirect(url_for('cards'))

# Route for deleting a card
@app.route('/delete/<card_id>')
def delete(card_id):
    """Deletes a card from the database."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    db.execute('DELETE FROM cards WHERE id = ?', [card_id])
    db.commit()
    flash('Card deleted.')
    return redirect(url_for('cards'))

# Routes for different types of cards
@app.route('/general')
@app.route('/general/<card_id>')
def general(card_id=None):
    """Displays and manages general type cards."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return memorize("general", card_id)

@app.route('/academic')
@app.route('/academic/<card_id>')
def academic(card_id=None):
    """Displays and manages academic type cards."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return memorize("academic", card_id)

@app.route('/personal')
@app.route('/personal/<card_id>')
def personal(card_id=None):
    """Displays and manages personal type cards."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return memorize("personal", card_id)

# Function to memorize cards
def memorize(card_type, card_id):
    """Displays cards for memorization."""
    if card_type == "general":
        type = 1
    elif card_type == "academic":
        type = 2
    elif card_type == "personal":
        type = 3
    else:
        return redirect(url_for('cards'))

    if card_id:
        card = get_card_by_id(card_id)
    else:
        card = get_card(type)
    if not card:
        flash("You've learned all the " + card_type + " cards.")
        return redirect(url_for('cards'))
    short_answer = (len(card['back']) < 75)
    return render_template('memorize.html',
                           card=card,
                           card_type=card_type,
                           short_answer=short_answer)

# Function to get a card for memorization
def get_card(type):
    """Gets a card for memorization."""
    db = get_db()

    query = '''
      SELECT
        id, type, front, back, known
      FROM cards
      WHERE
        type = ?
        and known = 0
      ORDER BY RANDOM()
      LIMIT 1
    '''

    cur = db.execute(query, [type])
    return cur.fetchone()

# Function to get a card by its ID
def get_card_by_id(card_id):
    """Gets a card by its ID."""
    db = get_db()

    query = '''
      SELECT
        id, type, front, back, known
      FROM cards
      WHERE
        id = ?
      LIMIT 1
    '''

    cur = db.execute(query, [card_id])
    return cur.fetchone()

# Route for marking a card as known
@app.route('/mark_known/<card_id>/<card_type>')
def mark_known(card_id, card_type):
    """Marks a card as known."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    db.execute('UPDATE cards SET known = 1 WHERE id = ?', [card_id])
    db.commit()
    flash('Card marked as known.')
    return redirect(url_for(card_type))

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log in functionality."""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session.permanent = True  # stay logged in
            return redirect(url_for('cards'))
    return render_template('login.html', error=error)

# Route for user logout
@app.route('/logout')
def logout():
    """Log out functionality."""
    session.pop('logged_in', None)
    flash("You've logged out")
    return redirect(url_for('index'))

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0')

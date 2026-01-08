from flask import Flask, render_template, request, session
from flask_session import Session
import sqlite3

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = False

app.secret_key = 'secret'
Session(app)

#   SESSION HANDLING

@app.before_request
def make_session_permanent():
    # Initialize session on first request
    # Need this here so cookies actually work 🤷🏻‍♀️
    if 'init' not in session:
        session['init'] = True
    # This forces the session to be created/updated on every request
    # ensuring the cookie is sent immediately when the page loads.
    session.modified = True


#   ROUTING

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/princess", methods=["GET", "POST"])
def princess():
    return render_template("princess.html")

@app.route("/bedroom", methods=["GET", "POST"])
def bedroom():
    return render_template("bedroom.html")

@app.route("/dungeon", methods=["GET", "POST"])
def dungeon():
    return render_template("dungeon.html")

@app.route("/balcony", methods=["GET", "POST"])
def balcony():
    return render_template("balcony.html")



#  INTERACTIONS AND SCORING

ITEM_POINTS = {
    'test_good': 3,
    'test_bad': -1,
    'stairs': 2,
    'hole': -2,
    'balcony': 5,
    'yarn': 5,
    'bed': 3,
    'no_rest': -3,
}

@app.route('/save', methods=['POST'])
def save():
    # Grab the value sent by JavaScript
    item_name = request.form.get('value')
    
    #  Use session ID as user identifier
    user_id = session.sid

    #  Look up the points (default to 0 if item isn't in the list)
    points = ITEM_POINTS.get(item_name, 0)

    # SQL to save data in database
    conn = sqlite3.connect('database.db')
    db = conn.cursor()

    # Ask the database if the user clicked this item before
    db.execute('SELECT 1 FROM history WHERE user = ? AND item = ?', (user_id, item_name))
    already_clicked = db.fetchone() # This will be None if it's new

    if not already_clicked:
        # Only insert if it is NOT in the database yet
        db.execute('INSERT INTO history (user, item, score) VALUES (?, ?, ?)', (user_id, item_name, points))
        conn.commit()
        print(f"--- SAVED: {item_name} (Points: {points}) User: {user_id}---")
    else:
        # If it exists, just print a message (don't save)
        print(f"--- IGNORED: {item_name} was already clicked by this user (User: {user_id}) ---")
    conn.close()

    return '', 204 # Returns "No Content" success code to the browser

# Function to get total score for a user
def get_score(user_id):
    conn = sqlite3.connect('database.db')
    db = conn.cursor()
    
    # SQL 'SUM' adds up all the numbers in the score column for this user
    db.execute('SELECT SUM(score) FROM history WHERE user = ?', (user_id,))
    
    result = db.fetchone()[0]
    conn.close()
    
    return result if result else 0

if __name__ == "__main__":
    app.run(port=8000, debug=True)
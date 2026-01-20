from flask import Flask, render_template, request, session, redirect, url_for
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
    if check_escape(session.sid) != 0:
        return render_template("home.html", windowclass="windowleft scoreable", windowlink="/escape")
    else:
        return render_template("home.html", windowclass="windowleft", windowlink="#")

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

@app.route("/computer", methods=["GET", "POST"])
def computer():
    template_name, bestie_name = check_quiz(session.sid)
    
    # **bestie_name unpacks the dictionary into arguments
    # It becomes: render_template("page4.html", bestie="balouba")
    return render_template(template_name, **bestie_name)

    #return render_template("page4.html", bestie ="balouba")

@app.route("/escape", methods=["GET", "POST"])
def escape():
    if check_escape(session.sid) == 2:
        return render_template("escape.html", yarnvisibility="visibility: visible", cablevisibility="visibility: hidden", windowlink="/yarn_escape", noreturn="yarn_escape")
    elif check_escape(session.sid) == 1:
        return render_template("escape.html", yarnvisibility="visibility: hidden", cablevisibility="visibility: visible", windowlink="/cable_escape", noreturn="cable_escape")
    else:
        if get_score(session.sid) >= 0:
            return render_template("escape.html", yarnvisibility="visibility: visible", cablevisibility="visibility: visible", windowlink="/yarn_escape", noreturn="yarn_escape")
        else:
            return render_template("escape.html", yarnvisibility="visibility: visible", cablevisibility="visibility: visible", windowlink="/cable_escape", noreturn="cable_escape")

@app.route("/yarn_escape", methods=["GET", "POST"])
def yarn_escape():

    return render_template("yarn_escape.html") 

@app.route("/cable_escape", methods=["GET", "POST"])
def cable_escape():
    return render_template("cable_escape.html")

@app.route("/you_are_free", methods=["GET", "POST"])
def you_are_free():
    return render_template("yarn_final.html") 

@app.route("/are_you_free", methods=["GET", "POST"])
def are_you_free():
    return render_template("cable_final.html")

@app.route("/lol", methods=["GET", "POST"])
def lol():
    return render_template("lol.html")


#  INTERACTIONS AND SCORING

ITEM_POINTS = {
    'test_good': 3,
    'test_bad': -1,
    'yarn_escape': 99,
    'cable_escape': -99,
    'quiz_finished': 0,
    'enter': 0,
    'portrait': 0,
    'window':0,
    'restart': 0,
    'balouba': 1,
    'yes_horse': 1,
    'stars':1,
    'plant': 1,
    'painting': 1,
    'quit': 2,
    'stairs': 2,  
    'bed': 3,
    'balcony': 5,
    'yarn': 5,
    'pepis': -1,
    'electric': -1,
    'telescope': -1,
    'no_horse': -2,
    'hole': -2,
    'home': -2,
    'no_rest': -4,
    'computer': -5,
    'cable': -5,
}

@app.route('/save', methods=['POST'])
def save():
    # Grab the value sent by JavaScript
    item_name = request.form.get('value')

    #  Use session ID as user identifier
    user_id = session.sid

    if item_name == "restart":
        #clear database
        conn = sqlite3.connect('database.db')
        db = conn.cursor()
        db.execute('DELETE FROM history WHERE user = ?', (user_id,))
        conn.commit()
        conn.close()

        #clear session
        session.clear() 
        
        print("SESSION WIPED: User will get a new ID")
        
        #force a page reload so Flask generates the new ID
        return redirect(url_for("index"))
    

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

def check_escape(user_id):
    conn = sqlite3.connect('database.db')
    db = conn.cursor()
    
    # Check if the user has collected the yarn
    db.execute('SELECT 1 FROM history WHERE user = ? AND item = ?', (user_id, 'yarn'))
    
    yarn = db.fetchone()

    db.execute('SELECT 1 FROM history WHERE user = ? AND item = ?', (user_id, 'cable'))

    cable = db.fetchone()

    conn.close()
    
    if yarn and cable:
        return 3
    elif yarn:
        return 2
    elif cable:
        return 1
    else:
        return 0
    
def check_quiz(user_id):
    conn = sqlite3.connect('database.db')
    db = conn.cursor()
    
    # Check if the user is horse
    db.execute('SELECT 1 FROM history WHERE user = ? AND item = ?', (user_id, 'yes_horse'))
    
    is_horse = db.fetchone()

    db.execute('SELECT 1 FROM history WHERE user = ? AND item = ?', (user_id, 'no_horse'))

    isnt_horse = db.fetchone()
    
    #check if user has a bestie
    db.execute('SELECT item FROM history WHERE user = ? AND item IN (?, ?)', (user_id, 'balouba', 'pepis'))

    has_friend = db.fetchone()

    #check if user has finished the quiz(and went back by arrow)
    db.execute('SELECT 1 FROM history WHERE user = ? AND item = ?', (user_id, 'quiz_finished'))

    quiz_ended = db.fetchone()

    conn.close()

    if quiz_ended:
        conn = sqlite3.connect('database.db')
        db = conn.cursor()

        db.execute('DELETE FROM history WHERE user = ? AND item IN (?, ?, ?, ?, ?)', (user_id, 'yes_horse', 'no_horse', 'balouba', 'pepis','quiz_finished'))
        conn.commit()
        conn.close()

        print(f"--- Data deleted. Quiz reset for this user {user_id}) ---")
        return "page1.html", {} # Empty dict because page1 needs no variables
        
        
    elif is_horse:
        return "page2.html", {}
        
    elif isnt_horse and not has_friend:
        return "page3.html", {}
        
    elif has_friend:
        return "page4.html", {"bestie": has_friend[0]}
        
    else:
        return "page1.html", {}

    

if __name__ == "__main__":
    app.run(port=8000)
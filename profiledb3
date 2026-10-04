from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "workshop-secret"

# --- Simple SQLite users ---
db = sqlite3.connect("users.db")
db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
db.execute("DELETE FROM users")
db.execute("INSERT INTO users VALUES ('anjar', 'bintaro')")
db.execute("INSERT INTO users VALUES ('arazka', 'tangerang')")
db.commit()
db.close()


def page(title, content):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: Arial; max-width: 800px; margin: 40px auto; }}
            nav a {{ margin-right: 20px; text-decoration: none; }}
            h1 {{ color: #1f4e79; }}
        </style>
    </head>
    <body>
        <nav>
            <a href="/">Home</a>
            <a href="/about">About Me</a>
            <a href="/expertise">Expertise</a>
            <a href="/experience">Experience</a>
            <a href="/knowledge">Knowledge Base</a>
        </nav>
        <hr>
        {content}
    </body>
    </html>
    """


@app.route("/")
def home():
    return page("Home", """
        <h1>Hello World! by Anjar (Sun 4 October 2026 at 06:12)</h1>
        <p>Welcome to my simple corporate website.</p>
        <p>Built with Python and Flask.</p>
    """)


@app.route("/about")
def about():
    return page("About Me", """
        <h1>About Me</h1>
        <p><b>Anjar Priandoyo</b></p>
        <p>IT professional with experience in technology, governance and cybersecurity.</p>
    """)


@app.route("/expertise")
def expertise():
    return page("My Expertise", """
        <h1>My Expertise</h1>
        <ul>
            <li>IT Governance</li>
            <li>Cybersecurity</li>
            <li>Digital Transformation</li>
            <li>AI & Technology</li>
        </ul>
    """)


@app.route("/experience")
def experience():
    return page("My Experience", """
        <h1>My Experience</h1>
        <ul>
            <li>Banking & Financial Services</li>
            <li>Technology Consulting</li>
            <li>IT Risk & Governance</li>
            <li>Digital Transformation</li>
        </ul>
    """)


# --- Login ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = sqlite3.connect("users.db")
        user = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (request.form["username"], request.form["password"])
        ).fetchone()
        db.close()

        if user:
            session["user"] = user[0]
            return redirect("/knowledge")

    return page("Login", """
        <h1>Knowledge Base Login</h1>
        <form method="POST">
            Username:<br>
            <input name="username"><br><br>
            Password:<br>
            <input name="password" type="password"><br><br>
            <button type="submit">Login</button>
        </form>
    """)


# --- Protected Knowledge Base ---
@app.route("/knowledge")
def knowledge():
    if "user" not in session:
        return redirect("/login")

    return page("Knowledge Base", """
        <h1>IT Knowledge Base</h1>
        <p>Latest technology developments:</p>
        <ul>
            <li><b>September 2026:</b> GPT-6 Astra introduced by OpenAI.</li>
            <li><b>September 2026:</b> ChatGPT Images 2.5 introduced.</li>
            <li><b>January 2026:</b> ChatGPT Go became available worldwide.</li>
            <li><b>2026:</b> AI agents and AI-assisted software development continue to expand.</li>
            <li><b>2026:</b> AI governance and cybersecurity become increasingly important.</li>
        </ul>

        <p>Logged in as: <b>""" + session["user"] + """</b></p>
        <a href="/logout">Logout</a>
    """)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)

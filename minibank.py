```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>MiniBank</h1>
    <p>Cybersecurity Training Application</p>

    <ul>
        <li><a href="/login">Login</a></li>
        <li><a href="/customers">Customers</a></li>
        <li><a href="/guestbook">Guestbook</a></li>
        <li><a href="/admin">Admin</a></li>
        <li><a href="/about">About</a></li>
    </ul>
    """


@app.route("/login")
def login():
    return """
    <h1>Login</h1>

    <form>
        Username:
        <input type="text" name="username"><br><br>

        Password:
        <input type="password" name="password"><br><br>

        <input type="submit" value="Login">
    </form>
    """


@app.route("/customers")
def customers():
    return """
    <h1>Customers</h1>

    <ul>
        <li>001 - Andi</li>
        <li>002 - Budi</li>
        <li>003 - Citra</li>
    </ul>
    """


@app.route("/guestbook")
def guestbook():
    return """
    <h1>Guestbook</h1>

    <form>
        Name:
        <input type="text" name="name"><br><br>

        Message:
        <input type="text" name="message"><br><br>

        <input type="submit" value="Submit">
    </form>
    """


@app.route("/admin")
def admin():
    return """
    <h1>Admin Panel</h1>
    <p>MiniBank administration area.</p>
    """


@app.route("/about")
def about():
    return """
    <h1>About MiniBank</h1>
    <p>This is a cybersecurity training application.</p>
    <p>Do not use real customer information.</p>
    """


@app.route("/robots.txt")
def robots():
    return """
    User-agent: *
    Disallow: /admin
    Disallow: /customers
    """


app.run(host="0.0.0.0", port=5000)
```

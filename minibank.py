from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>MiniBank</title>
    </head>
    <body>
        <h1>MiniBank</h1>
        <p>Cybersecurity Training Application</p>

        <h2>Menu</h2>
        <ul>
            <li><a href="/login">Login</a></li>
            <li><a href="/customers">Customers</a></li>
            <li><a href="/guestbook">Guestbook</a></li>
            <li><a href="/admin">Admin</a></li>
            <li><a href="/about">About</a></li>
        </ul>
    </body>
    </html>
    """


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        return f"""
        <h1>Login</h1>
        <p>Login attempt received for: {username}</p>
        <a href="/">Back</a>
        """

    return """
    <h1>Login</h1>

    <form method="POST">
        Username:<br>
        <input type="text" name="username"><br><br>

        Password:<br>
        <input type="password" name="password"><br><br>

        <input type="submit" value="Login">
    </form>

    <br>
    <a href="/">Back</a>
    """


@app.route("/customers")
def customers():
    return """
    <h1>Customers</h1>

    <table border="1">
        <tr>
            <th>ID</th>
            <th>Name</th>
        </tr>
        <tr>
            <td>001</td>
            <td>Andi</td>
        </tr>
        <tr>
            <td>002</td>
            <td>Budi</td>
        </tr>
        <tr>
            <td>003</td>
            <td>Citra</td>
        </tr>
    </table>

    <br>
    <a href="/">Back</a>
    """


@app.route("/guestbook", methods=["GET", "POST"])
def guestbook():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")

        return f"""
        <h1>Guestbook</h1>

        <p>Thank you, {name}.</p>
        <p>Your message: {message}</p>

        <a href="/guestbook">Back</a>
        """

    return """
    <h1>Guestbook</h1>

    <form method="POST">
        Name:<br>
        <input type="text" name="name"><br><br>

        Message:<br>
        <input type="text" name="message"><br><br>

        <input type="submit" value="Submit">
    </form>

    <br>
    <a href="/">Back</a>
    """


@app.route("/admin")
def admin():
    return """
    <h1>MiniBank Admin</h1>

    <p>Administrative area.</p>

    <ul>
        <li>User Management</li>
        <li>Transaction Management</li>
        <li>System Configuration</li>
    </ul>

    <a href="/">Back</a>
    """


@app.route("/about")
def about():
    return """
    <h1>About MiniBank</h1>

    <p>MiniBank is a cybersecurity training application.</p>
    <p>This application contains simulated banking data.</p>

    <a href="/">Back</a>
    """


@app.route("/robots.txt")
def robots():
    return """
    User-agent: *
    Disallow: /admin
    Disallow: /customers
    Disallow: /backup
    """


@app.route("/backup")
def backup():
    return """
    <h1>Backup Area</h1>

    <p>This is a simulated backup directory.</p>

    <a href="/">Back</a>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

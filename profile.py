from flask import Flask

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

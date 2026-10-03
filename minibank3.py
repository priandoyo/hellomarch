from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "minibank-abc.db"

HTML = """
<!doctype html>
<html>
<head>
    <title>MiniBank-ABC by Anjar (Sat 3 Oct 2026)</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; background:#f5f5f5; }
        .card { background:white; padding:20px; margin-bottom:20px; border-radius:10px; box-shadow:0 2px 8px #ddd; }
        h1 { margin-bottom:5px; }
        table { width:100%; border-collapse:collapse; }
        th, td { padding:10px; border-bottom:1px solid #ddd; text-align:left; }
        input, select, button { padding:10px; margin:5px 0; width:100%; box-sizing:border-box; }
        button { cursor:pointer; background:#222; color:white; border:0; border-radius:5px; }
        .balance { font-size:30px; font-weight:bold; }
        .positive { color:green; }
        .negative { color:red; }
    </style>
</head>
<body>
    <h1>🏦 MiniBank-ABC</h1>
    <p>Simple banking application for a web/API workshop</p>

    {% if message %}
    <div class="card"><strong>{{ message }}</strong></div>
    {% endif %}

    <div class="card">
        <h2>Accounts</h2>
        <table>
            <tr><th>Account</th><th>Customer</th><th>Balance</th></tr>
            {% for a in accounts %}
            <tr>
                <td>{{ a[0] }}</td>
                <td>{{ a[1] }}</td>
                <td>Rp {{ "{:,.0f}".format(a[2]) }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <div class="card">
        <h2>Deposit</h2>
        <form method="post" action="/deposit">
            <select name="account">
                {% for a in accounts %}
                <option value="{{ a[0] }}">{{ a[0] }} - {{ a[1] }}</option>
                {% endfor %}
            </select>
            <input type="number" name="amount" placeholder="Amount" min="1" required>
            <button>Deposit</button>
        </form>
    </div>

    <div class="card">
        <h2>Transfer</h2>
        <form method="post" action="/transfer">
            <select name="from_account">
                {% for a in accounts %}
                <option value="{{ a[0] }}">{{ a[0] }} - {{ a[1] }}</option>
                {% endfor %}
            </select>

            <select name="to_account">
                {% for a in accounts %}
                <option value="{{ a[0] }}">{{ a[0] }} - {{ a[1] }}</option>
                {% endfor %}
            </select>

            <input type="number" name="amount" placeholder="Amount" min="1" required>
            <button>Transfer</button>
        </form>
    </div>

    <div class="card">
        <h2>Transaction History</h2>
        <table>
            <tr><th>Time</th><th>Type</th><th>From</th><th>To</th><th>Amount</th></tr>
            {% for t in transactions %}
            <tr>
                <td>{{ t[0] }}</td>
                <td>{{ t[1] }}</td>
                <td>{{ t[2] or "-" }}</td>
                <td>{{ t[3] or "-" }}</td>
                <td>Rp {{ "{:,.0f}".format(t[4]) }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <div class="card">
        <h2>API Endpoints</h2>
        <ul>
            <li><a href="/api/accounts">GET /api/accounts</a></li>
            <li><a href="/api/transactions">GET /api/transactions</a></li>
            <li>POST /api/deposit</li>
            <li>POST /api/transfer</li>
        </ul>
    </div>
</body>
</html>
"""

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_no TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            balance INTEGER NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            type TEXT NOT NULL,
            from_account TEXT,
            to_account TEXT,
            amount INTEGER NOT NULL
        )
    """)

    count = conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]

    if count == 0:
        conn.executemany(
            "INSERT INTO accounts VALUES (?, ?, ?)",
            [
                ("ABC001", "Anjar", 10000000),
                ("ABC002", "Arazka", 5000000),
                ("ABC003", "Customer ABC", 7500000)
            ]
        )

    conn.commit()
    conn.close()

def accounts():
    conn = db()
    rows = conn.execute(
        "SELECT account_no, name, balance FROM accounts ORDER BY account_no"
    ).fetchall()
    conn.close()
    return rows

def transactions():
    conn = db()
    rows = conn.execute("""
        SELECT created_at, type, from_account, to_account, amount
        FROM transactions
        ORDER BY id DESC
    """).fetchall()
    conn.close()
    return rows

@app.route("/")
def home():
    return render_template_string(
        HTML,
        accounts=accounts(),
        transactions=transactions(),
        message=request.args.get("message")
    )

@app.route("/deposit", methods=["POST"])
def deposit():
    account = request.form["account"]
    amount = int(request.form["amount"])

    if amount <= 0:
        return redirect(url_for("home", message="Invalid amount"))

    conn = db()

    conn.execute(
        "UPDATE accounts SET balance = balance + ? WHERE account_no = ?",
        (amount, account)
    )

    conn.execute("""
        INSERT INTO transactions
        (created_at, type, from_account, to_account, amount)
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "DEPOSIT",
        None,
        account,
        amount
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("home", message="Deposit successful"))

@app.route("/transfer", methods=["POST"])
def transfer():
    sender = request.form["from_account"]
    receiver = request.form["to_account"]
    amount = int(request.form["amount"])

    if sender == receiver:
        return redirect(url_for("home", message="Cannot transfer to the same account"))

    if amount <= 0:
        return redirect(url_for("home", message="Invalid amount"))

    conn = db()

    sender_row = conn.execute(
        "SELECT balance FROM accounts WHERE account_no = ?",
        (sender,)
    ).fetchone()

    receiver_row = conn.execute(
        "SELECT balance FROM accounts WHERE account_no = ?",
        (receiver,)
    ).fetchone()

    if not sender_row or not receiver_row:
        conn.close()
        return redirect(url_for("home", message="Account not found"))

    if sender_row["balance"] < amount:
        conn.close()
        return redirect(url_for("home", message="Insufficient balance"))

    conn.execute(
        "UPDATE accounts SET balance = balance - ? WHERE account_no = ?",
        (amount, sender)
    )

    conn.execute(
        "UPDATE accounts SET balance = balance + ? WHERE account_no = ?",
        (amount, receiver)
    )

    conn.execute("""
        INSERT INTO transactions
        (created_at, type, from_account, to_account, amount)
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "TRANSFER",
        sender,
        receiver,
        amount
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("home", message="Transfer successful"))

@app.route("/api/accounts")
def api_accounts():
    return [
        {
            "account_no": a["account_no"],
            "name": a["name"],
            "balance": a["balance"]
        }
        for a in accounts()
    ]

@app.route("/api/transactions")
def api_transactions():
    return [
        {
            "time": t["created_at"],
            "type": t["type"],
            "from": t["from_account"],
            "to": t["to_account"],
            "amount": t["amount"]
        }
        for t in transactions()
    ]

@app.route("/api/deposit", methods=["POST"])
def api_deposit():
    data = request.get_json()

    account = data.get("account")
    amount = int(data.get("amount", 0))

    if amount <= 0:
        return {"error": "Invalid amount"}, 400

    conn = db()

    account_row = conn.execute(
        "SELECT account_no FROM accounts WHERE account_no = ?",
        (account,)
    ).fetchone()

    if not account_row:
        conn.close()
        return {"error": "Account not found"}, 404

    conn.execute(
        "UPDATE accounts SET balance = balance + ? WHERE account_no = ?",
        (amount, account)
    )

    conn.execute("""
        INSERT INTO transactions
        (created_at, type, from_account, to_account, amount)
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "DEPOSIT",
        None,
        account,
        amount
    ))

    conn.commit()
    conn.close()

    return {"message": "Deposit successful", "account": account, "amount": amount}

@app.route("/api/transfer", methods=["POST"])
def api_transfer():
    data = request.get_json()

    sender = data.get("from_account")
    receiver = data.get("to_account")
    amount = int(data.get("amount", 0))

    if amount <= 0:
        return {"error": "Invalid amount"}, 400

    if sender == receiver:
        return {"error": "Cannot transfer to the same account"}, 400

    conn = db()

    sender_row = conn.execute(
        "SELECT balance FROM accounts WHERE account_no = ?",
        (sender,)
    ).fetchone()

    receiver_row = conn.execute(
        "SELECT balance FROM accounts WHERE account_no = ?",
        (receiver,)
    ).fetchone()

    if not sender_row or not receiver_row:
        conn.close()
        return {"error": "Account not found"}, 404

    if sender_row["balance"] < amount:
        conn.close()
        return {"error": "Insufficient balance"}, 400

    conn.execute(
        "UPDATE accounts SET balance = balance - ? WHERE account_no = ?",
        (amount, sender)
    )

    conn.execute(
        "UPDATE accounts SET balance = balance + ? WHERE account_no = ?",
        (amount, receiver)
    )

    conn.execute("""
        INSERT INTO transactions
        (created_at, type, from_account, to_account, amount)
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "TRANSFER",
        sender,
        receiver,
        amount
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Transfer successful",
        "from": sender,
        "to": receiver,
        "amount": amount
    }

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

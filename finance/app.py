import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers  import lookup
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session['user_id']

    # Obtener el saldo de efectivo del usuario
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]['cash']

    # Obtener las transacciones del usuario
    transactions = db.execute(
        "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
        user_id
    )

    portfolio = []
    total_value = 0

    for transaction in transactions:
        symbol = transaction['symbol']
        shares = transaction['total_shares']

        # Obtener información del stock
        stock_info = lookup(symbol)

        if stock_info:
            price = stock_info['price']
            total_stock_value = shares * price

            # Agregar información al portafolio
            portfolio.append({
                'symbol': symbol,
                'shares': shares,
                'price': price,
                'total_value': total_stock_value
            })

            # Sumar el valor total de las acciones
            total_value += total_stock_value

    # Calcular el total general (acciones + efectivo)
    grand_total = total_value + cash

    return render_template("index.html", portfolio=portfolio, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    #return apology("TODO")
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("el símbolo no puede estar vacío,")

        if not shares.isdigit() or int(shares) <= 0:
            return apology("El número de acciones debe ser un entero positivo")
        shares = int(shares)
        stock_info = lookup(symbol)

        if stock_info is None:
            return apology("No se encontró información para el símbolo proporcionado.")

        price = stock_info['price']
        user_id = session['user_id']
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]['cash']

        total_cost = price * shares

        if cash < total_cost:
            return apology("No tienes suficieente dinero para realizar estacompra.")

        existing_transaction  = db.execute ("SELECT * FROM transactions WHERE user_id = ? AND  symbol =?", user_id,symbol)

        if existing_transaction:
            existing_transaction = existing_transaction[0]
            new_shares = existing_transaction['shares'] + shares
            db.execute("UPDATE transactions SET  shares =? WHERE user_id =? AND symbol =?", new_shares, user_id, symbol)
        else:
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",user_id, symbol, shares, price, datetime.now())

        db.execute("UPDATE users SET  cash = cash - ? WHERE  id = ?", total_cost, user_id)

        return redirect("/")

    return render_template("buy.html")




@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    #return apology("TODO")
    user_id = session['user_id']

    transactions = db.execute("SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",user_id)

    history_list = []

    for transaction in transactions:
        if transaction['shares'] > 0:
            action = "Compra"
        else:
            action = "Venta"

        history_list.append({
            'action': action,
            'symbol': transaction['symbol'],
            'shares': abs(transaction['shares']),
            'price': transaction['price'],
            'timestamp': transaction['timestamp']
        })

    return render_template("history.html", history=history_list)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    #return apology("TODO")
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("El simbolo no puede estar vacío")

        stock_info = lookup(symbol)



        if stock_info is None:
            return apology("No se encontró información para el simbolo proporcionado")

        return render_template("quoted.html", symbol=stock_info['symbol'], price=stock_info['price'])
    return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology ("El nombre de usuario no puede estar vacío.")

        if not password:
             return apology (" la contraseña no puede estar vacía")

        if not confirmation:
              return apology("La confirmacion de la contraseña no puede estar vacía")

        if password != confirmation:
             return apology(" Las contraseñas no coinciden.")

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, generate_password_hash(password))
        except ValueError:
            return apology("El usuario ya existe")
        return redirect("/")


    #return apology("TODO")
    return render_template ("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session['user_id']

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Verificar si se seleccionó un símbolo
        if not symbol:
            return apology("Debes seleccionar un símbolo de acción.")

        # Verificar si se ingresó un número de acciones
        if not shares.isdigit() or int(shares) <= 0:
            return apology("El número de acciones debe ser un entero positivo.")

        shares = int(shares)

        # Verificar si el usuario posee acciones de ese símbolo
        owned_shares = db.execute("SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)

        if not owned_shares or owned_shares[0]['total_shares'] < shares:
            return apology("No posees suficientes acciones de este símbolo.")

        # Obtener información del stock
        stock_info = lookup(symbol)
        price = stock_info['price']

        # Actualizar la base de datos: registrar la venta
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
                   user_id, symbol, -shares, price, datetime.now())

        # Actualizar el saldo de efectivo del usuario
        total_sale_value = price * shares
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_sale_value, user_id)

        return redirect("/")

    # Si el método es GET, mostrar el formulario de venta
    symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
    return render_template("sell.html", symbols=[symbol['symbol'] for symbol in symbols])

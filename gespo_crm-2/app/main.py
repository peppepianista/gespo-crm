
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from .database import get_db
from .models import User, Account

APP_NAME = "Gespo CRM"
PLAN_PRICE = "25 EUR/mese"

app = FastAPI(title=APP_NAME)
app.add_middleware(SessionMiddleware, secret_key="change-me")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

def page(title, body):
    return f"""<!doctype html>
<html><head><meta charset='utf-8'/><meta name='viewport' content='width=device-width, initial-scale=1'/>
<title>{APP_NAME} - {title}</title>
<link rel='stylesheet' href='/static/style.css'/></head>
<body>
<header class='topbar'><div class='brand'><a href='/'>{APP_NAME}</a></div>
<nav><a href='/login'>Login</a><a class='btn' href='/signup'>Prova gratis</a></nav></header>
<main class='container'>
{body}
</main><footer class='footer'>{APP_NAME} - piano unico {PLAN_PRICE}</footer></body></html>"""

@app.get("/", response_class=HTMLResponse)
def landing():
    return page("Home", """
    <section class='hero'><h1>Gespo CRM</h1>
    <p>CRM per fotografi — semplice e veloce.</p>
    <div class='pricing'><div class='card'><h3>Piano Unico</h3><div class='price'>25 EUR/mese</div>
    <ul><li>Lead/Clienti/Progetti (base)</li><li>Dashboard leggera</li></ul>
    <a class='btn' href='/signup'>Inizia ora</a></div></div></section>
    """)

@app.get("/login", response_class=HTMLResponse)
def login_form():
    return page("Login", """
    <div class='login-card'><h1>Accedi</h1>
    <form method='post' action='/login'>
      <label>Username<input name='username' required></label>
      <label>Password<input type='password' name='password' required></label>
      <button type='submit'>Entra</button>
    </form>
    <p class='muted'>Oppure <a href='/signup'>crea un account</a></p>
    </div>""")

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = next(get_db())):
    u = db.query(User).filter(User.username == username).first()
    if not u or not bcrypt.verify(password, u.password_hash):
        return HTMLResponse(page("Login", "<div class='login-card'><p class='error'>Credenziali non valide</p></div>"))
    request.session["user"] = {"id": u.id, "account_id": u.account_id, "username": u.username}
    return RedirectResponse("/dashboard", status_code=303)

@app.get("/signup", response_class=HTMLResponse)
def signup_form():
    return page("Signup", """
    <div class='login-card'><h1>Crea il tuo studio</h1>
    <form method='post' action='/signup'>
      <label>Nome Studio<input name='studio_name' required></label>
      <label>Username admin<input name='username' required></label>
      <label>Password<input type='password' name='password' required></label>
      <button type='submit'>Crea account</button>
    </form></div>""")

@app.post("/signup")
def signup(request: Request, studio_name: str = Form(...), username: str = Form(...), password: str = Form(...), db: Session = next(get_db())):
    acc = Account(name=studio_name, slug=studio_name.lower().replace(' ','-'))
    db.add(acc); db.flush()
    u = User(account_id=acc.id, username=username, password_hash=bcrypt.hash(password))
    db.add(u); db.commit()
    request.session["user"] = {"id": u.id, "account_id": u.account_id, "username": u.username}
    return RedirectResponse("/dashboard", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)
    return page("Dashboard", "<h1>Dashboard</h1><p class='muted'>Benvenuto! Qui vedrai KPI e moduli.</p><p><a href='/logout'>Logout</a></p>")

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)

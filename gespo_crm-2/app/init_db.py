from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import Account, User

def init():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        if not db.query(Account).first():
            acc = Account(name="Gespo Demo", slug="gespo-demo")
            db.add(acc); db.flush()
            admin = User(account_id=acc.id, username="admin", password_hash=bcrypt.hash("admin"))
            db.add(admin); db.commit()
            print("Creati account demo e utente admin/admin")
        else:
            print("DB già inizializzato.")
    finally:
        db.close()

if __name__ == "__main__":
    init()

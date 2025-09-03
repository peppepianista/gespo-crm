# Gespo CRM

CRM per fotografi — tema verde petrolio, piano unico 25€/mese.

## Avvio locale
```bash
python -m venv .venv
source .venv/bin/activate    # su Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m app.init_db
uvicorn app.main:app --reload
# http://127.0.0.1:8000
```

## Deploy con 1 click su Render
1) Carica questo progetto su un tuo repo GitHub chiamato `gespo-crm`
2) Sostituisci `TUONOME` nel link qui sotto con il tuo username GitHub
3) Apri il README nel repo e clicca il bottone

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/TUONOME/gespo-crm)

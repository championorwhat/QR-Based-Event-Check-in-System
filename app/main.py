from fastapi import FastAPI
from app.routers import user, event
from app.database import ping_db  # Import ping_db
from app.database import db
from app.routers import registration
from app.utils.qr import generate_qr_code
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await ping_db()  # Check if DB connection works when app starts

app.include_router(user.router, prefix="/user", tags=["User"])

@app.get("/check-db")
async def check_db():
    collections = await db.list_collection_names()
    return {"collections": collections}


@app.get("/generate-qr", response_class=HTMLResponse)
def test_qr():
    data = {"user_id": "123", "event_id": "456", "name": "John Doe"}
    qr_base64 = generate_qr_code(data)

    html_content = f"""
    <html>
        <body>
            <h2>QR Code Preview</h2>
            <img src="data:image/png;base64,{qr_base64}" />
        </body>
    </html>
    """
    return html_content

@app.get("/")
async def root():
    return {"message": "QR Check-in System"}

app.include_router(event.router)
app.include_router(registration.router)
app.include_router(event.router, prefix="/event", tags=["event"])


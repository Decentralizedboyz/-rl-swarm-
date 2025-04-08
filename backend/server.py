import sys
import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import jwt
from passlib.context import CryptContext
from backend.database.database import get_db
from backend.database.models import User, Investment, Payment, Notification
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Get the absolute path to the frontend directory
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

# Mount static files
app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")

# Serve the main HTML file
@app.get("/")
async def read_root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Authentication endpoints
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users/register")
async def register_user(username: str, email: str, full_name: str, password: str, db: Session = Depends(get_db)):
    try:
        # Check if user exists
        if db.query(User).filter(User.username == username).first():
            raise HTTPException(status_code=400, detail="Username already registered")
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        hashed_password = get_password_hash(password)
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {"message": "User created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# User endpoints
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    try:
        return {
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "balance": current_user.balance,
            "total_earnings": current_user.total_earnings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Investment endpoints
@app.get("/investments")
async def get_investments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        investments = db.query(Investment).filter(Investment.user_id == current_user.id).all()
        return investments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/investments")
async def create_investment(
    plan_name: str,
    amount: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Create investment
        investment = Investment(
            user_id=current_user.id,
            plan_name=plan_name,
            amount=amount,
            status="active",
            expected_return=amount * 1.1,  # 10% return for example
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=60)  # 60 days for example
        )
        db.add(investment)
        db.commit()
        db.refresh(investment)
        
        return investment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Payment endpoints
@app.get("/payments")
async def get_payments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        payments = db.query(Payment).filter(Payment.user_id == current_user.id).all()
        return payments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/payments")
async def create_payment(
    amount: float,
    payment_method: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Create payment
        payment = Payment(
            user_id=current_user.id,
            amount=amount,
            payment_method=payment_method,
            status="pending",
            transaction_id=f"TRX-{datetime.utcnow().timestamp()}"
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        return payment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Notification endpoints
@app.get("/notifications")
async def get_notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        notifications = db.query(Notification).filter(Notification.user_id == current_user.id).all()
        return notifications
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        ).first()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        notification.read = True
        db.commit()
        return {"message": "Notification marked as read"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
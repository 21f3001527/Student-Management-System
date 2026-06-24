from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlmodel import Session, select

from database import get_session
from models import Admin

# Config
SECRET_KEY = "student-management-secret-key"
ALGORITHM = "HS256"

# Setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")

# ── Password helpers ──────────────────────
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# ── Token helpers ─────────────────────────
def create_token(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# ── Get current admin ─────────────────────
def get_current_admin(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> Admin:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    admin = session.exec(select(Admin).where(Admin.username == username)).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found")
    return admin
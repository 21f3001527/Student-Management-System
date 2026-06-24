from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from database import get_session
from models import Admin
from schemas import AdminRegister, Token
from auth import hash_password, verify_password, create_token

router = APIRouter(prefix="/admin", tags=["Admin"])

# ── Register ──────────────────────────────
@router.post("/register")
def register(
    admin: AdminRegister,
    session: Session = Depends(get_session)
):
    # Already exist karta hai?
    existing = session.exec(
        select(Admin).where(Admin.username == admin.username)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Save karo
    new_admin = Admin(
        username=admin.username,
        password=hash_password(admin.password)
    )
    session.add(new_admin)
    session.commit()
    return {"message": f"Admin '{admin.username}' registered!"}

# ── Login ─────────────────────────────────
@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    # Admin dhundho
    admin = session.exec(
        select(Admin).where(Admin.username == form.username)
    ).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found")

    # Password verify karo
    if not verify_password(form.password, admin.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    # Token banao
    token = create_token({"sub": admin.username})
    return Token(access_token=token)
################# OTP GENERATION/VALIDATION ####################
import pyotp
from datetime import datetime, timedelta
from app.core.config import settings

def generate_otp() -> str:
    return pyotp.random_base32()[:6]  # 6-digit numeric? Actually random base32 chars; for simplicity use digits
    # Better: use pyotp.TOTP(pyotp.random_base32()).now()[:6] but we don't need TOTP.
    # For hackathon, just generate random 6-digit number:
    import random
    return f"{random.randint(100000, 999999)}"

def hash_otp(otp: str) -> str:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(otp)

def verify_otp(otp: str, hashed: str) -> bool:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(otp, hashed)
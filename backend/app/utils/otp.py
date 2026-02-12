################# OTP GENERATION/VALIDATION ####################
import pyotp
from datetime import datetime, timedelta
from app.core.config import settings

def generate_otp() -> str:
    return pyotp.random_base32()[:6]  # simple 6-digit

def hash_otp(otp: str) -> str:
    # use passlib or simply store plain for hackathon (not secure!)
    return otp  # in real use, hash with bcrypt

def verify_otp(otp: str, hashed: str) -> bool:
    return otp == hashed
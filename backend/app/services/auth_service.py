from sqlalchemy.orm import Session
from uuid import uuid4, UUID
from app.repositories.user_repo import UserRepository
from app.schemas.auth import UserCreate
from app.models.user import User  # ✅ IMPORT THE USER MODEL

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    # ⚠️ HACKATHON ONLY – NO BCRYPT, PLAIN TEXT PASSWORDS
    def hash_password(self, password: str) -> str:
        # Store password as plain text (NEVER do this in production!)
        return password

    def verify_password(self, plain: str, hashed: str) -> bool:
        # Direct string comparison
        return plain == hashed

    def create_access_token(self, data: dict) -> str:
        from jose import jwt
        from datetime import datetime, timedelta
        from app.core.config import settings
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def register_user(self, user_data: dict) -> User:
        # Check if email already exists
        existing = self.user_repo.get_by_email(user_data['email'])
        if existing:
            raise ValueError("Email already registered")

        # Handle hospital_id conversion
        if 'hospital_id' in user_data and user_data['hospital_id'] is not None:
            hid = user_data['hospital_id']
            if isinstance(hid, UUID):
                user_data['hospital_id'] = hid.bytes
            else:
                user_data['hospital_id'] = UUID(str(hid)).bytes
        else:
            user_data['hospital_id'] = None

        # Generate new ID
        user_data['id'] = uuid4().bytes

        # Store password as plain text (⚠️ HACKATHON ONLY)
        plain_password = user_data.pop('password')
        user_data['password_hash'] = plain_password  # Direct storage

        # Create user
        return self.user_repo.create(**user_data)

    def authenticate_user(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        # Direct comparison (plain text)
        if password != user.password_hash:
            return None
        return user
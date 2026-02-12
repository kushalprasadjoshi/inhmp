from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from functools import wraps

from app.core.config import settings
from app.core.database import get_db
from app.repositories.user_repo import UserRepository

security = HTTPBearer()

from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.repositories.user_repo import UserRepository

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    print("\n=== GET_CURRENT_USER DEBUG ===")
    print(f"Token (first 20): {token[:20]}...")
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str = payload.get("sub")
        print(f"user_id_str from token: {user_id_str}")
        
        if user_id_str is None:
            print("❌ No 'sub' in token")
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = UUID(user_id_str)
        print(f"Converted user_id: {user_id}")
    except JWTError as e:
        print(f"❌ JWT decode error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except ValueError as e:
        print(f"❌ UUID conversion error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = UserRepository(db).get(user_id)
    if not user:
        print(f"❌ User not found for id: {user_id}")
        raise HTTPException(status_code=401, detail="User not found")
    
    print(f"✅ User found: {user.email}, role: {user.role}")
    return user

def require_role(allowed_roles: list):
    """
    Dependency to check if the current user has one of the allowed roles.
    Usage: Depends(require_role(["Doctor", "Admin"]))
    """
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker
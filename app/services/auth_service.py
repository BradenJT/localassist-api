from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from uuid import uuid4
import hashlib

from app.models.user import User, UserCreate, Token, TokenData
from app.database.dynamodb import db
from app.utils.exceptions import UnauthorizedException, ConflictException

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

class AuthService:
    def __init__(self):
        self.db = db
    
    @staticmethod
    def _prepare_password(password: str) -> str:
        """
        Prepare password for bcrypt hashing.
        bcrypt has a 72 byte limit, so we hash long passwords first.
        """
        password_bytes = password.encode('utf-8')
        
        # If password is longer than 72 bytes, hash it first
        if len(password_bytes) > 72:
            # Use SHA256 to hash long passwords, then encode as hex
            return hashlib.sha256(password_bytes).hexdigest()
        
        return password
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        prepared_password = AuthService._prepare_password(plain_password)
        return pwd_context.verify(prepared_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        prepared_password = AuthService._prepare_password(password)
        return pwd_context.hash(prepared_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    async def register_user(self, user_create: UserCreate) -> User:
        """Register a new user"""
        # Check if user already exists
        existing_user = await self.db.get_user_by_email(user_create.email)
        if existing_user:
            raise ConflictException("Email already registered")
        
        # Create new business_id for this user
        business_id = f"biz_{uuid4().hex[:12]}"
        
        # Hash password and create user
        user_data = {
            'id': str(uuid4()),
            'email': user_create.email,
            'business_name': user_create.business_name,
            'business_id': business_id,
            'hashed_password': self.get_password_hash(user_create.password),
            'is_active': True,
            'created_at': datetime.utcnow().isoformat()
        }
        
        await self.db.create_user(user_data)
        
        return User(
            id=user_data['id'],
            email=user_data['email'],
            business_name=user_data['business_name'],
            business_id=user_data['business_id'],
            is_active=user_data['is_active']
        )
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user"""
        user_data = await self.db.get_user_by_email(email)
        if not user_data:
            return None
        
        if not self.verify_password(password, user_data['hashed_password']):
            return None
        
        return User(
            id=user_data['id'],
            email=user_data['email'],
            business_name=user_data['business_name'],
            business_id=user_data['business_id'],
            is_active=user_data.get('is_active', True)
        )
    
    async def get_current_user(self, token: str) -> User:
        """Get current user from JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            business_id: str = payload.get("business_id")
            
            if email is None:
                raise UnauthorizedException("Could not validate credentials")
            
            token_data = TokenData(email=email, business_id=business_id)
        except JWTError:
            raise UnauthorizedException("Could not validate credentials")
        
        user_data = await self.db.get_user_by_email(email=token_data.email)
        if user_data is None:
            raise UnauthorizedException("Could not validate credentials")
        
        return User(
            id=user_data['id'],
            email=user_data['email'],
            business_name=user_data['business_name'],
            business_id=user_data['business_id'],
            is_active=user_data.get('is_active', True)
        )

auth_service = AuthService()
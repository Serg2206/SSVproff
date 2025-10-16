
"""
Security utilities for authentication and authorization.

This module contains JWT token handling, password hashing,
and other security-related utilities.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT algorithm
ALGORITHM = "HS256"


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token (typically {"sub": user_id})
        expires_delta: Token expiration time (defaults to ACCESS_TOKEN_EXPIRE_MINUTES)
        
    Returns:
        Encoded JWT token string
        
    Example:
        >>> from datetime import timedelta
        >>> token = create_access_token(
        ...     data={"sub": "user@example.com"},
        ...     expires_delta=timedelta(minutes=30)
        ... )
        >>> print(token)  # Returns encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create a JWT refresh token.
    
    Refresh tokens have a longer expiration time (7 days by default)
    and can be used to obtain new access tokens.
    
    Args:
        data: Data to encode in the token (typically {"sub": user_id})
        
    Returns:
        Encoded JWT refresh token string
        
    Example:
        >>> token = create_refresh_token(data={"sub": "user@example.com"})
        >>> print(token)  # Returns encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token to decode
        
    Returns:
        Token payload if valid, None otherwise
        
    Example:
        >>> token = create_access_token(data={"sub": "user@example.com"})
        >>> payload = decode_token(token)
        >>> print(payload["sub"])  # Returns "user@example.com"
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password to verify against
        
    Returns:
        True if password matches, False otherwise
        
    Example:
        >>> hashed = get_password_hash("mypassword")
        >>> is_valid = verify_password("mypassword", hashed)
        >>> print(is_valid)  # Returns True
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password for storage.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string
        
    Example:
        >>> hashed = get_password_hash("mypassword")
        >>> print(hashed)  # Returns bcrypt hashed password
    """
    return pwd_context.hash(password)

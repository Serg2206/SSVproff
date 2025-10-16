
"""
Tests for security utilities (password hashing and JWT tokens).
"""
import pytest
from datetime import timedelta

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token
)


class TestPasswordHashing:
    """Test password hashing and verification."""
    
    def test_password_hashing(self):
        """Test password can be hashed and verified."""
        password = "securepassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed) is True
    
    def test_wrong_password(self):
        """Test wrong password fails verification."""
        password = "securepassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_hash_consistency(self):
        """Test same password produces different hashes (due to salt)."""
        password = "securepassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        assert hash1 != hash2
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestJWTTokens:
    """Test JWT token generation and validation."""
    
    def test_create_access_token(self):
        """Test access token creation."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_refresh_token(self):
        """Test refresh token creation."""
        data = {"sub": "test@example.com"}
        token = create_refresh_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_decode_access_token(self):
        """Test access token can be decoded."""
        user_id = "test@example.com"
        data = {"sub": user_id}
        token = create_access_token(data)
        
        payload = decode_token(token)
        
        assert payload is not None
        assert payload["sub"] == user_id
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload
    
    def test_decode_refresh_token(self):
        """Test refresh token can be decoded."""
        user_id = "test@example.com"
        data = {"sub": user_id}
        token = create_refresh_token(data)
        
        payload = decode_token(token)
        
        assert payload is not None
        assert payload["sub"] == user_id
        assert payload["type"] == "refresh"
        assert "exp" in payload
        assert "iat" in payload
    
    def test_decode_invalid_token(self):
        """Test decoding invalid token returns None."""
        invalid_token = "invalid.token.here"
        payload = decode_token(invalid_token)
        
        assert payload is None
    
    def test_token_with_custom_expiration(self):
        """Test token with custom expiration time."""
        data = {"sub": "test@example.com"}
        expires_delta = timedelta(hours=1)
        token = create_access_token(data, expires_delta=expires_delta)
        
        payload = decode_token(token)
        
        assert payload is not None
        assert payload["sub"] == "test@example.com"

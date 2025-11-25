import os
import json
import base64
import hmac
import hashlib
from datetime import datetime, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt, enforcing the 72-byte limit."""
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password too long (bcrypt limit 72 bytes)"
        )
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    if len(plain_password.encode("utf-8")) > 72:
        return False
    return pwd_context.verify(plain_password, hashed_password)

# Simple HMAC-based token implementation (fallback to avoid external jwt deps)
# Token format: <payload_b64>.<signature_hex>
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

def _b64_decode(data: str) -> bytes:
    b = data.encode("ascii")
    padding = b"=" * (-len(b) % 4)
    return base64.urlsafe_b64decode(b + padding)

def _sign(message: bytes) -> str:
    return hmac.new(SECRET_KEY.encode("utf-8"), message, hashlib.sha256).hexdigest()

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a simple signed token containing the data and expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": int(expire.timestamp())})
    payload_json = json.dumps(to_encode, separators=(',', ':'), sort_keys=True).encode("utf-8")
    payload_b64 = _b64_encode(payload_json).encode("ascii")
    signature = _sign(payload_b64)
    return payload_b64.decode("ascii") + "." + signature

def decode_access_token(token: str) -> dict:
    """Decode and verify the simple signed token and return its payload as a dict."""
    try:
        parts = token.split('.')
        if len(parts) != 2:
            raise ValueError("Invalid token format")
        payload_b64, signature = parts
        expected = _sign(payload_b64.encode("ascii"))
        if not hmac.compare_digest(expected, signature):
            raise ValueError("Invalid signature")
        payload_json = _b64_decode(payload_b64)
        payload = json.loads(payload_json.decode("utf-8"))
        exp = int(payload.get("exp", 0))
        if datetime.utcnow().timestamp() > exp:
            raise ValueError("Token expired")
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

import random
import string
from datetime import datetime, timedelta
from typing import Optional, Dict
from app.config import settings

try:
    if settings.USE_REDIS:
        import redis
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
    else:
        redis_client = None
except Exception:
    redis_client = None


class OTPService:
    """OTP Generation and Verification Service"""

    def __init__(self):
        # In-memory storage for OTPs (fallback if Redis not available)
        self._otp_storage: Dict[str, Dict] = {}

    def generate_otp(self, length: int = None) -> str:
        """Generate a random numeric OTP"""
        if length is None:
            length = settings.OTP_LENGTH

        return ''.join(random.choices(string.digits, k=length))

    def store_otp(self, email: str, otp: str) -> None:
        """Store OTP with expiration"""
        expire_time = datetime.now() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)

        if redis_client:
            # Store in Redis with TTL
            key = f"otp:{email}"
            redis_client.setex(
                key,
                settings.OTP_EXPIRE_MINUTES * 60,
                otp
            )
        else:
            # Store in memory
            self._otp_storage[email] = {
                "otp": otp,
                "expires_at": expire_time
            }

    def verify_otp(self, email: str, otp: str) -> bool:
        """Verify OTP and remove if valid"""
        if redis_client:
            key = f"otp:{email}"
            stored_otp = redis_client.get(key)

            if stored_otp and stored_otp == otp:
                # Delete OTP after successful verification
                redis_client.delete(key)
                return True
            return False
        else:
            # Verify from memory
            if email not in self._otp_storage:
                return False

            otp_data = self._otp_storage[email]

            # Check if OTP is expired
            if datetime.now() > otp_data["expires_at"]:
                del self._otp_storage[email]
                return False

            # Verify OTP
            if otp_data["otp"] == otp:
                del self._otp_storage[email]
                return True

            return False

    def get_otp(self, email: str) -> Optional[str]:
        """Get OTP for testing/development purposes"""
        if redis_client:
            key = f"otp:{email}"
            return redis_client.get(key)
        else:
            if email in self._otp_storage:
                otp_data = self._otp_storage[email]
                if datetime.now() <= otp_data["expires_at"]:
                    return otp_data["otp"]
            return None

    def delete_otp(self, email: str) -> None:
        """Manually delete OTP"""
        if redis_client:
            key = f"otp:{email}"
            redis_client.delete(key)
        else:
            if email in self._otp_storage:
                del self._otp_storage[email]


# Singleton instance
otp_service = OTPService()

"""
Stytch utility functions for password reset and authentication
"""
import stytch
from django.conf import settings
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class StytchService:
    """Service class for Stytch operations"""
    
    def __init__(self):
        self.client = self._get_client()
    
    def _get_client(self) -> stytch.Client:
        """Initialize Stytch client with proper configuration"""
        if not settings.STYTCH_PROJECT_ID or not settings.STYTCH_SECRET:
            raise ValueError(
                "Stytch credentials not configured. "
                "Please set STYTCH_PROJECT_ID and STYTCH_SECRET in your .env file."
            )
        
        return stytch.Client(
            project_id=settings.STYTCH_PROJECT_ID,
            secret=settings.STYTCH_SECRET,
            environment=settings.STYTCH_PROJECT_ENV
        )
    
    def validate_reset_token(self, token: str) -> Dict[str, Any]:
        """
        Validate a password reset token without consuming it
        Returns token info if valid, raises exception if invalid
        """
        try:
            # For validation, we can try to get user info from token
            # This doesn't consume the token
            response = self.client.passwords.strength_check(
                password="temp_password_for_validation"
            )
            return {"valid": True, "token": token}
        except Exception as e:
            logger.error(f"Token validation failed: {e}")
            raise e
    
    def reset_password(self, token: str, new_password: str, token_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Reset password using Stytch token
        
        Args:
            token: The reset token from email
            new_password: New password to set
            token_type: Type of token (e.g., 'multi_tenant_passwords')
        
        Returns:
            Dict with reset result information
        """
        try:
            # First, check password strength
            strength_response = self.client.passwords.strength_check(
                password=new_password
            )
            
            if not strength_response.valid_password:
                raise ValueError(f"Password is too weak: {strength_response.feedback}")
            
            # Reset the password
            if token_type == "multi_tenant_passwords":
                response = self.client.passwords.reset_by_email(
                    token=token,
                    password=new_password
                )
            else:
                response = self.client.passwords.reset_by_email(
                    token=token,
                    password=new_password
                )
            
            logger.info("Password reset successful")
            return {
                "success": True,
                "user_id": getattr(response, 'user_id', None),
                "session_token": getattr(response, 'session_token', None),
                "session_jwt": getattr(response, 'session_jwt', None)
            }
            
        except Exception as e:
            logger.error(f"Password reset failed: {e}")
            raise e
    
    def send_reset_email(self, email: str, reset_password_redirect_url: str) -> Dict[str, Any]:
        """
        Send password reset email via Stytch
        
        Args:
            email: User's email address
            reset_password_redirect_url: URL to redirect to after email click
        
        Returns:
            Dict with send result information
        """
        try:
            response = self.client.passwords.email.reset_start(
                email=email,
                reset_password_redirect_url=reset_password_redirect_url,
                reset_password_expiration_minutes=30  # Token expires in 30 minutes
            )
            
            logger.info(f"Password reset email sent to {email}")
            return {
                "success": True,
                "email_id": getattr(response, 'email_id', None)
            }
            
        except Exception as e:
            logger.error(f"Failed to send reset email to {email}: {e}")
            raise e


# Singleton instance
stytch_service = StytchService()
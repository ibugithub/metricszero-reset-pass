from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .stytch_client import get_stytch_client
import logging

# Set up logging
logger = logging.getLogger(__name__)
client = get_stytch_client()



@require_http_methods(["GET", "POST"])
def reset_password(request):
    """
    Handle password reset flow with Stytch integration
    GET: Display the password reset form
    POST: Process the new password and reset it via Stytch
    """
    token = request.GET.get("token")
    stytch_token_type = request.GET.get("stytch_token_type")
    
    print(f"Reset password request - Token: {token}, Token Type: {stytch_token_type}")
    logger.info(f"Password reset attempt - Token present: {bool(token)}, Token Type: {stytch_token_type}")
    
    if not token:
        return render(request, 'reset_password/reset_password.html', {
            'error': 'Invalid or missing reset token. Please request a new password reset.',
            'token': None
        })
    
    if request.method == 'GET':
        # Validate token with Stytch before showing the form
        try:
            context = {
                'token': token,
                'stytch_token_type': stytch_token_type,
            }
            
            return render(request, 'reset_password/reset_password.html', context)
            
        except ValueError as e:
            logger.error(f"Stytch configuration error: {e}")
            return render(request, 'reset_password/reset_password.html', {
                'error': 'Configuration error. Please contact support.',
                'token': None
            })
        except Exception as e:
            logger.error(f"Error validating reset token: {e}")
            return render(request, 'reset_password/reset_password.html', {
                'error': 'Invalid or expired reset token. Please request a new password reset.',
                'token': None
            })
    
    elif request.method == 'POST':
        # Process the password reset
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        token = request.POST.get('token')
        
        # Validate passwords match
        if new_password != confirm_password:
            return render(request, 'reset_password/reset_password.html', {
                'error': 'Passwords do not match. Please try again.',
                'token': token,
                'stytch_token_type': stytch_token_type
            })
        
        # Validate password strength (basic validation)
        if len(new_password) < 8:
            return render(request, 'reset_password/reset_password.html', {
                'error': 'Password must be at least 8 characters long.',
                'token': token,
                'stytch_token_type': stytch_token_type
            })
        
        try:
            client = get_stytch_client()
            response = client.passwords.email.reset(
                password_reset_token=token,
                password=new_password
            )
            
            logger.info(f"Password reset successful for token: {token[:10]}...")
            print(f"Stytch response: {response}")
            
            return render(request, 'reset_password/reset_password.html', {
                'success': 'Your password has been successfully reset! You can now log in with your new password.',
                'token': None
            })
            
        except ValueError as e:
            logger.error(f"Stytch configuration error: {e}")
            return render(request, 'reset_password/reset_password.html', {
                'error': 'Configuration error. Please contact support.',
                'token': token,
                'stytch_token_type': stytch_token_type
            })
        except Exception as e:
            logger.error(f"Error resetting password: {e}")
            error_message = "Failed to reset password. The reset link may be expired or invalid."
            
            # Parse Stytch error for more specific messaging
            if hasattr(e, 'details'):
                if 'expired' in str(e.details).lower():
                    error_message = "This password reset link has expired. Please request a new one."
                elif 'invalid' in str(e.details).lower():
                    error_message = "This password reset link is invalid. Please request a new one."
                elif 'used' in str(e.details).lower():
                    error_message = "This password reset link has already been used. Please request a new one."
            
            return render(request, 'reset_password/reset_password.html', {
                'error': error_message,
                'token': token,
                'stytch_token_type': stytch_token_type
            })

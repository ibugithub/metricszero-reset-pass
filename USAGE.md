# Example Usage and Testing Guide

## Testing the Password Reset Feature

### 1. With Stytch Integration (Recommended)

After configuring your Stytch credentials in `.env`:

1. **Start the server:**
   ```bash
   poetry run python manage.py runserver
   ```

2. **Test Stytch configuration:**
   ```bash
   poetry run python manage.py test_stytch
   ```

3. **Send a real password reset email (if you have a user in Stytch):**
   ```bash
   poetry run python manage.py test_stytch --email your-email@example.com
   ```

4. **Access the reset form with a token:**
   ```
   http://localhost:8000/reset_password/?token=YOUR_STYTCH_TOKEN&stytch_token_type=multi_tenant_passwords
   ```

### 2. Testing Without Real Stytch Tokens (Development)

For development purposes, you can test the form UI:

1. **Access the form with a dummy token:**
   ```
   http://localhost:8000/reset_password/?token=dummy_token_for_testing
   ```

2. **The form will display, but password reset will fail without valid Stytch credentials.**

### 3. Example Stytch Token URL

A real Stytch password reset URL looks like:
```
http://localhost:8000/reset_password/?slug=fictionalcompany&stytch_token_type=multi_tenant_passwords&token=pBg6f1oP7lYFm6eIB4POIyWH8jbLu1PAxIgI3nXOBJcx
```

### 4. Expected Flow

1. **User receives email from Stytch**
2. **User clicks reset link → redirected to your Django app**
3. **Django app displays password reset form**
4. **User enters new password**
5. **Django app validates token with Stytch and resets password**
6. **Success or error message displayed**

### 5. Webhook Testing

To test webhooks, you can use tools like ngrok:

1. **Install ngrok:** https://ngrok.com/
2. **Expose local server:**
   ```bash
   ngrok http 8000
   ```
3. **Configure webhook URL in Stytch Dashboard:**
   ```
   https://your-ngrok-url.ngrok.io/webhook/password-reset/
   ```

## Error Scenarios to Test

1. **Invalid token:** Access `/reset_password/?token=invalid_token`
2. **Expired token:** Use an old Stytch token
3. **Password mismatch:** Enter different passwords in the form
4. **Weak password:** Enter a short password (< 8 characters)
5. **Missing token:** Access `/reset_password/` without token parameter

## Production Checklist

- [ ] Update `.env` with production Stytch credentials
- [ ] Set `STYTCH_PROJECT_ENV=live`
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Configure proper domain in Stytch Dashboard
- [ ] Set up HTTPS
- [ ] Configure email templates in Stytch Dashboard
- [ ] Test with real email addresses
- [ ] Set up monitoring and logging
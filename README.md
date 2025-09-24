# MetricsZero Password Reset

A Django application integrated with Stytch for handling secure password reset functionality.

## Features

- 🔐 Secure password reset with Stytch integration
- 📧 Email-based password reset tokens
- 🎨 Clean, responsive password reset form
- 🔒 Password strength validation
- 📝 Comprehensive logging and error handling
- 🎯 Multi-tenant support
- 🪝 Webhook support for password reset events

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- Poetry (for dependency management)
- Stytch account ([Sign up here](https://stytch.com))

### 2. Installation

```bash
# Clone or navigate to the project directory
cd metricszero-reset-pass

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### 3. Stytch Configuration

1. Go to your [Stytch Dashboard](https://stytch.com/dashboard)
2. Select your project or create a new one
3. Navigate to **Configuration → API Keys**
4. Copy your **Project ID** and **Secret Key**

### 4. Environment Setup

1. Edit the `.env` file in the project root
2. Replace the Stytch configuration values:

```env
# Stytch Configuration
STYTCH_PROJECT_ID=project-test-00000000-0000-0000-0000-000000000000
STYTCH_SECRET=secret-test-000000000000000000000000000=
STYTCH_PROJECT_ENV=test  # Use 'test' for development, 'live' for production
```

### 5. Database Setup

```bash
# Run migrations
poetry run python manage.py migrate
```

### 6. Test Configuration

```bash
# Test Stytch connectivity
poetry run python manage.py test_stytch

# Optional: Test with real email
poetry run python manage.py test_stytch --email your-email@example.com
```

### 7. Run the Server

```bash
poetry run python manage.py runserver
```

## Usage

### Password Reset Flow

1. **User clicks reset link from Stytch email**
   - URL format: `http://localhost:8000/reset_password/?token=<stytch_token>&stytch_token_type=multi_tenant_passwords`

2. **User sees password reset form**
   - Clean, responsive interface
   - Password confirmation validation
   - Client-side and server-side validation

3. **Password reset processing**
   - Token validation with Stytch
   - Password strength checking
   - Secure password update via Stytch API

### API Endpoints

- `GET/POST /reset_password/` - Main password reset form
- `POST /webhook/password-reset/` - Webhook for Stytch events

### Testing the Integration

You can test the password reset flow in several ways:

#### Method 1: Using Stytch Dashboard
1. Go to your Stytch Dashboard
2. Navigate to **Users** section
3. Create or select a user
4. Click "Send Password Reset Email"
5. Check your email and click the reset link

#### Method 2: Direct URL Testing
```
http://localhost:8000/reset_password/?token=your_test_token&stytch_token_type=multi_tenant_passwords
```

## Project Structure

```
metricszero-reset-pass/
├── manage.py
├── pyproject.toml
├── .env
├── reset_password/
│   ├── views.py                 # Main password reset logic
│   ├── stytch_service.py        # Stytch integration utilities
│   ├── urls.py                  # URL routing
│   ├── templates/
│   │   └── reset_password/
│   │       ├── reset_password.html  # Main reset form
│   │       └── error.html           # Error page
│   └── management/
│       └── commands/
│           └── test_stytch.py   # Stytch configuration tester
└── metricszero_reset_pass/
    ├── settings.py              # Django settings with Stytch config
    └── urls.py                  # Main URL configuration
```

## Security Features

- 🔐 Token-based authentication via Stytch
- 🕒 Token expiration (30 minutes default)
- 🔒 Password strength validation
- 🚫 CSRF protection
- 📝 Comprehensive logging
- 🔄 One-time use tokens

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STYTCH_PROJECT_ID` | Your Stytch Project ID | Required |
| `STYTCH_SECRET` | Your Stytch Secret Key | Required |
| `STYTCH_PROJECT_ENV` | Environment (test/live) | `test` |
| `DJANGO_DEBUG` | Django debug mode | `True` |
| `DJANGO_SECRET_KEY` | Django secret key | Auto-generated |

### Stytch Settings

- **Token Expiration**: 30 minutes (configurable in `stytch_service.py`)
- **Password Requirements**: Minimum 8 characters
- **Multi-tenant Support**: Enabled
- **Email Templates**: Configured in Stytch Dashboard

## Logging

Logs are written to:
- Console output (during development)
- `logs/password_reset.log` file

Log levels:
- `INFO`: Successful operations
- `ERROR`: Failed operations and exceptions
- `WARNING`: Potential issues

## Error Handling

The application handles various error scenarios:

- ❌ Invalid or expired tokens
- ❌ Missing Stytch configuration
- ❌ Password mismatch
- ❌ Weak passwords
- ❌ Network/API failures

## Webhook Integration

Optional webhook endpoint for handling Stytch events:

```python
# Configure in Stytch Dashboard
POST /webhook/password-reset/

# Supported events:
- password.reset_confirmed
```

## Development

### Running Tests

```bash
poetry run python manage.py test
```

### Code Formatting

```bash
poetry add --group dev black flake8
poetry run black .
poetry run flake8 .
```

## Production Deployment

1. Set environment to production in `.env`:
```env
STYTCH_PROJECT_ENV=live
DJANGO_DEBUG=False
```

2. Generate a new Django secret key
3. Configure your web server (nginx, Apache)
4. Set up SSL/TLS certificates
5. Configure Stytch production settings

## Troubleshooting

### Common Issues

**"Stytch credentials not configured"**
- Check your `.env` file has correct `STYTCH_PROJECT_ID` and `STYTCH_SECRET`
- Run `poetry run python manage.py test_stytch` to verify

**"Invalid or expired reset token"**
- Tokens expire after 30 minutes
- Each token can only be used once
- Ensure the token is copied correctly from the email

**Password reset email not received**
- Check spam/junk folder
- Verify email address exists in Stytch
- Check Stytch Dashboard for email logs

### Getting Help

1. Check the application logs in `logs/password_reset.log`
2. Run the Stytch configuration test: `poetry run python manage.py test_stytch`
3. Review Stytch Dashboard for API logs and errors

## License

This project is licensed under the MIT License.
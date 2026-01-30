"""
Web routes for Your Brief landing pages.
Handles public-facing pages like landing, signup, etc.
"""
from flask import Blueprint, render_template, redirect, url_for, session

# Create blueprint
web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def landing():
    """Landing page for Your Brief."""
    return render_template('web/landing.html')


@web_bp.route('/signup')
def signup():
    """Signup page."""
    return render_template('web/signup.html')


@web_bp.route('/auth-loading')
def auth_loading():
    """Loading page while OAuth is processing."""
    return render_template('web/auth_loading.html')


@web_bp.route('/success')
def success():
    """Success page after completing setup."""
    # Check if user is authenticated
    if 'user_email' not in session:
        return redirect(url_for('web.landing'))
    return render_template('web/success.html')


@web_bp.route('/error')
def error():
    """Error page."""
    error_message = session.get('error_message', 'An unknown error occurred')
    return render_template('web/error.html', error=error_message)

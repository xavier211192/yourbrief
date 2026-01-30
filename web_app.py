#!/usr/bin/env python3
"""
Your Brief - Flask Web Application

Multi-user web app for Your Brief with OAuth authentication.

Usage:
    python web_app.py
    or
    uv run python web_app.py
"""
import os
from flask import Flask, render_template, session
from flask_session import Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Configuration
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

# Initialize session
Session(app)

# Import and register blueprints
from app.api.web_routes import web_bp
from app.api.auth_routes import auth_bp
from app.api.user_routes import user_bp

app.register_blueprint(web_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('web/error.html', error='Page not found'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    session['error_message'] = 'An internal server error occurred'
    return render_template('web/error.html', error='Internal server error'), 500


# Health check endpoint
@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'healthy', 'service': 'Your Brief Web App'}, 200


if __name__ == '__main__':
    # Run in debug mode for development
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=5001, debug=debug)

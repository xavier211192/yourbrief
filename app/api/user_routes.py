"""
User preference routes for Your Brief.
Handles user settings like delivery time, timezone, etc.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify

# Create blueprint
user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/preferences')
def preferences():
    """User preferences page."""
    # Check if user is authenticated
    if 'user_email' not in session:
        return redirect(url_for('web.landing'))

    return render_template('web/preferences.html')


@user_bp.route('/preferences/save', methods=['POST'])
def save_preferences():
    """Save user preferences."""
    # Check if user is authenticated
    if 'user_email' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    # TODO: Save preferences to database
    delivery_time = request.form.get('delivery_time', '07:00')
    timezone = request.form.get('timezone', 'America/Los_Angeles')

    # Store in session for now (will move to database later)
    session['delivery_time'] = delivery_time
    session['timezone'] = timezone

    return redirect(url_for('web.success'))

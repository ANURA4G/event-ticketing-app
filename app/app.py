"""
Flask Application Entry Point
==============================

This is the main Flask application file.
"""

import os
import sys
from flask import Flask, render_template

# Add current directory to Python path for Vercel compatibility
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import blueprints
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp
from routes.scan import scan_bp

# Import security for secret key
from utils.security import SECRET_KEY

# Create Flask app
app = Flask(__name__)

# Configure app
app.secret_key = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(scan_bp)


@app.route('/')
def home():
    """Landing page route."""
    return render_template('landing.html')


@app.route('/admin')
def admin_shortcut():
    """Direct admin access route - requires login."""
    from flask import redirect, url_for, session
    if session.get('role') == 'admin':
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('auth.login'))


@app.route('/health')
def health():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    # Development server entry point
    app.run(debug=True)

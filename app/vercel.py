"""
Vercel Serverless Handler
==========================

This module adapts the Flask application for Vercel's serverless environment.
"""

import os
import sys
import traceback
from pathlib import Path

# Add the app directory to Python path for imports
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

try:
    # Import the Flask app - try multiple approaches for Vercel compatibility
    try:
        from app import app
    except ImportError:
        # If direct import fails, try importing as module
        import app as app_module
        app = app_module.app
    
    # Expose for Vercel's WSGI handler
    application = app
    handler = app
    
    # Debug route for testing
    @app.route('/vercel-test')
    def vercel_test():
        return {
            "status": "success", 
            "message": "Vercel deployment working",
            "path": app_dir,
            "sys_path": sys.path[:3]  # Show first 3 paths only
        }
        
except Exception as e:
    # Fallback error app for debugging
    from flask import Flask, jsonify
    
    error_app = Flask(__name__)
    
    @error_app.route('/')
    @error_app.route('/<path:path>')
    def error_handler(path=''):
        return jsonify({
            "error": "Import failed",
            "message": str(e),
            "traceback": traceback.format_exc()[-1000:],  # Last 1000 chars
            "working_dir": os.getcwd(),
            "app_dir": app_dir,
            "files_in_dir": os.listdir(app_dir),
            "python_path": sys.path[:5]
        }), 500
    
    application = error_app
    handler = error_app

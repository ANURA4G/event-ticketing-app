"""
Vercel Serverless Handler
==========================

This module adapts the Flask application for Vercel's serverless environment.

Responsibilities:
- Import the Flask app from app.py
- Expose the app as a WSGI-compatible handler for Vercel
- Handle serverless function invocation

Important Notes:
- Vercel uses ephemeral filesystem - JSON data resets on each deploy
- Cold starts may affect initial response times
- All routes are handled through this single serverless function

Usage:
- vercel.json points to this file as the handler
- No modifications needed for deployment
"""

from app import app

# Expose app for Vercel's WSGI handler
# Vercel will import this as the application handler
application = app

# For Vercel serverless functions
handler = app

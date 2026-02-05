"""
QR Scan Routes
===============

This module handles QR code scanning and ticket verification.

Features:
- Display QR scanner interface
- Verify scanned QR payloads
- Check signature integrity
- Mark attendance
- Prevent duplicate entries
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session

from utils.qr import decode_qr_payload
from utils.json_store import (
    get_ticket_by_id, mark_attendance, is_ticket_used,
    get_attendance_by_ticket
)

scan_bp = Blueprint('scan', __name__, url_prefix='/scan')


@scan_bp.route('/')
def index():
    """Display QR scanner page."""
    return render_template('scan.html')


@scan_bp.route('/camera')
def camera():
    """Camera-based QR scanner page."""
    return render_template('scan.html')


@scan_bp.route('/verify', methods=['POST'])
def verify():
    """
    API endpoint to verify a scanned QR payload.
    
    Accepts JSON with 'qr_data' containing the encrypted payload.
    
    Returns:
        JSON response with:
        - success: Boolean
        - status: VALID, USED, or INVALID
        - message: Human readable message
        - ticket: Ticket details (if valid)
    """
    data = request.get_json() or {}
    qr_data = data.get('qr_data', '').strip()
    
    if not qr_data:
        return jsonify({
            'success': False,
            'status': 'INVALID',
            'message': 'No QR data provided'
        })
    
    # Step 1: Decode and verify the QR payload
    decode_result = decode_qr_payload(qr_data)
    
    if not decode_result.get('valid'):
        return jsonify({
            'success': False,
            'status': 'INVALID',
            'message': decode_result.get('error', 'Invalid QR code')
        })
    
    # Extract ticket data from decoded payload
    payload_data = decode_result.get('data', {})
    ticket_id = payload_data.get('ticket_id')
    user_id = payload_data.get('user_id')
    team_name = payload_data.get('team_name')
    
    if not ticket_id:
        return jsonify({
            'success': False,
            'status': 'INVALID',
            'message': 'Invalid ticket data in QR code'
        })
    
    # Step 2: Verify ticket exists in database
    ticket = get_ticket_by_id(ticket_id)
    
    if not ticket:
        return jsonify({
            'success': False,
            'status': 'INVALID',
            'message': f'Ticket {ticket_id} not found in system'
        })
    
    # Step 3: Verify user_id matches (additional security)
    if ticket.get('user_id') != user_id:
        return jsonify({
            'success': False,
            'status': 'INVALID',
            'message': 'Ticket data mismatch - possible tampering'
        })
    
    # Step 4: Check if already used
    if is_ticket_used(ticket_id):
        existing = get_attendance_by_ticket(ticket_id)
        return jsonify({
            'success': False,
            'status': 'USED',
            'message': 'Ticket already used for entry',
            'scanned_at': existing.get('timestamp'),
            'ticket': {
                'ticket_id': ticket_id,
                'team_name': ticket.get('team_name'),
                'user_id': user_id
            }
        })
    
    # Step 5: Mark attendance
    scanned_by = session.get('username', 'scanner')
    result = mark_attendance(ticket_id, scanned_by)
    
    if result.get('success'):
        return jsonify({
            'success': True,
            'status': 'VALID',
            'message': '✅ Entry Allowed',
            'ticket': {
                'ticket_id': ticket_id,
                'team_name': ticket.get('team_name'),
                'user_id': user_id,
                'slot': ticket.get('slot'),
                'event_name': ticket.get('event_name')
            },
            'timestamp': result.get('timestamp')
        })
    else:
        return jsonify({
            'success': False,
            'status': result.get('status', 'INVALID'),
            'message': result.get('message', 'Failed to mark attendance')
        })


@scan_bp.route('/manual', methods=['GET', 'POST'])
def manual():
    """
    Manual ticket ID verification.
    
    For cases where QR scanner doesn't work.
    """
    if request.method == 'POST':
        ticket_id = request.form.get('ticket_id', '').strip().upper()
        
        if not ticket_id:
            flash('Please enter a ticket ID', 'error')
            return redirect(url_for('scan.manual'))
        
        # Check if ticket exists
        ticket = get_ticket_by_id(ticket_id)
        
        if not ticket:
            flash(f'Ticket {ticket_id} not found', 'error')
            return render_template('scan_result.html', result={
                'success': False,
                'status': 'INVALID',
                'message': f'Ticket {ticket_id} not found in system',
                'ticket_id': ticket_id
            })
        
        # Check if already used
        if is_ticket_used(ticket_id):
            existing = get_attendance_by_ticket(ticket_id)
            return render_template('scan_result.html', result={
                'success': False,
                'status': 'USED',
                'message': 'Ticket already used for entry',
                'ticket': ticket,
                'scanned_at': existing.get('timestamp')
            })
        
        # Mark attendance
        scanned_by = session.get('username', 'manual')
        result = mark_attendance(ticket_id, scanned_by)
        
        if result.get('success'):
            flash(f'✅ Entry allowed for {ticket.get("team_name")}', 'success')
            return render_template('scan_result.html', result={
                'success': True,
                'status': 'VALID',
                'message': 'Entry Allowed',
                'ticket': ticket,
                'timestamp': result.get('timestamp')
            })
        else:
            return render_template('scan_result.html', result=result)
    
    # GET - show manual entry form
    return render_template('scan.html')


@scan_bp.route('/result')
def result_page():
    """Display a scan result page."""
    return render_template('scan.html')


@scan_bp.route('/result/<ticket_id>')
def result(ticket_id):
    """Display scan result for a specific ticket."""
    ticket = get_ticket_by_id(ticket_id)
    attendance = get_attendance_by_ticket(ticket_id)
    
    if not ticket:
        result = {
            'success': False,
            'status': 'INVALID',
            'message': 'Ticket not found',
            'ticket_id': ticket_id
        }
    elif attendance:
        result = {
            'success': True,
            'status': 'CHECKED_IN',
            'message': 'Already checked in',
            'ticket': ticket,
            'scanned_at': attendance.get('timestamp')
        }
    else:
        result = {
            'success': True,
            'status': 'VALID',
            'message': 'Ticket is valid',
            'ticket': ticket
        }
    
    return render_template('scan_result.html', result=result)


# ============================================================
# API ENDPOINTS (for JavaScript scanner)
# ============================================================

@scan_bp.route('/api/check/<ticket_id>')
def api_check(ticket_id):
    """API to check ticket status without marking attendance."""
    ticket = get_ticket_by_id(ticket_id)
    
    if not ticket:
        return jsonify({
            'exists': False,
            'message': 'Ticket not found'
        })
    
    used = is_ticket_used(ticket_id)
    
    return jsonify({
        'exists': True,
        'used': used,
        'ticket': {
            'ticket_id': ticket_id,
            'team_name': ticket.get('team_name'),
            'user_id': ticket.get('user_id'),
            'slot': ticket.get('slot')
        }
    })

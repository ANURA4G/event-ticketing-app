"""
QR Code Generation Utilities
=============================

This module handles QR code generation for event tickets.

Security:
- Payload is encrypted before encoding in QR
- HMAC signature prevents tampering
- Contains ticket_id, user_id, timestamp, and signature
"""

import os
import json
import time

# Try to import qrcode, use placeholder if not available
try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

from utils.security import encrypt_data, decrypt_data, generate_signature, verify_signature

# Directory for storing QR code images
QR_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'qr')


def ensure_qr_dir():
    """Ensure the QR directory exists."""
    os.makedirs(QR_DIR, exist_ok=True)


def generate_qr_payload(ticket_id: str, user_id: str, team_name: str) -> str:
    """
    Generate an encrypted and signed QR payload.
    
    The payload contains:
    - ticket_id: Unique ticket identifier
    - user_id: User who owns the ticket
    - team_name: Team name for display
    - timestamp: When the QR was generated
    - signature: HMAC signature for verification
    
    Args:
        ticket_id: Unique ticket ID
        user_id: User ID associated with ticket
        team_name: Team name
    
    Returns:
        Encrypted payload string safe for QR encoding
    """
    # Create payload data
    payload_data = {
        'ticket_id': ticket_id,
        'user_id': user_id,
        'team_name': team_name,
        'timestamp': int(time.time())
    }
    
    # Convert to JSON string
    payload_json = json.dumps(payload_data, separators=(',', ':'))
    
    # Generate signature
    signature = generate_signature(payload_json)
    
    # Add signature to payload
    payload_data['signature'] = signature
    
    # Convert final payload to JSON
    final_payload = json.dumps(payload_data, separators=(',', ':'))
    
    # Encrypt the payload
    encrypted = encrypt_data(final_payload)
    
    return encrypted.decode('utf-8')


def decode_qr_payload(encrypted_payload: str) -> dict:
    """
    Decode and verify a QR payload.
    
    Args:
        encrypted_payload: The encrypted payload from QR scan
    
    Returns:
        Dictionary with:
        - valid: True if payload is valid and signature matches
        - data: The decoded ticket data
        - error: Error message if invalid
    """
    try:
        # Decrypt the payload
        decrypted = decrypt_data(encrypted_payload.encode('utf-8'))
        
        # Parse JSON
        payload_data = json.loads(decrypted)
        
        # Extract signature
        signature = payload_data.pop('signature', '')
        
        # Recreate the original payload for verification
        original_json = json.dumps(payload_data, separators=(',', ':'))
        
        # Verify signature
        if not verify_signature(original_json, signature):
            return {
                'valid': False,
                'error': 'Invalid signature - payload may be tampered'
            }
        
        return {
            'valid': True,
            'data': payload_data
        }
        
    except Exception as e:
        return {
            'valid': False,
            'error': f'Failed to decode payload: {str(e)}'
        }


def generate_qr_image(payload: str, ticket_id: str) -> str:
    """
    Generate a QR code image file.
    
    Args:
        payload: The encrypted payload to encode
        ticket_id: Ticket ID for filename
    
    Returns:
        Path to the generated QR image file
    """
    ensure_qr_dir()
    filepath = os.path.join(QR_DIR, f"{ticket_id}.png")
    
    if HAS_QRCODE:
        # Generate actual QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(payload)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filepath)
    else:
        # Fallback: Save payload as text file for debugging
        with open(filepath, 'w') as f:
            f.write(f"QR_PAYLOAD:{payload}")
    
    return filepath


def get_qr_path(ticket_id: str) -> str:
    """Get the file path for a ticket's QR code image."""
    return os.path.join(QR_DIR, f"{ticket_id}.png")


def get_qr_url(ticket_id: str) -> str:
    """Get the URL path for serving the QR image."""
    return f"/static/qr/{ticket_id}.png"

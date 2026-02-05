# Event Ticket & Entry Management System

A Flask-based web application for event ticketing with QR code-based entry verification.

## 🎫 Project Purpose

This system provides a complete solution for:
- **Event Ticketing**: Create and manage event tickets for attendees
- **QR Code Entry**: Generate QR codes for tickets that can be scanned at entry points
- **Attendance Tracking**: Record and track attendee check-ins in real-time
- **Role-Based Access**: Separate dashboards for administrators and users

## ⚠️ Important Warning

> **Data Persistence on Vercel**: This application uses JSON files for data storage. 
> On Vercel's serverless environment, the filesystem is **ephemeral**. 
> **All data (users, tickets, attendance) will reset on each deployment.**
> 
> For production use with persistent data, consider using an external storage solution.

## 📁 Folder Structure

```
event-ticketing-app/
│
├── app/                          # Main application package
│   ├── __init__.py               # App initialization and factory
│   ├── app.py                    # Flask app entry point
│   ├── vercel.py                 # Vercel serverless handler
│   │
│   ├── routes/                   # Route blueprints
│   │   ├── __init__.py           # Routes package init
│   │   ├── auth.py               # Authentication (login/logout)
│   │   ├── admin.py              # Admin dashboard & management
│   │   ├── user.py               # User dashboard & tickets
│   │   └── scan.py               # QR scanning & verification
│   │
│   ├── utils/                    # Utility modules
│   │   ├── __init__.py           # Utils package init
│   │   ├── security.py           # Encryption, hashing, secrets
│   │   ├── json_store.py         # Encrypted JSON read/write
│   │   ├── qr.py                 # QR code generation
│   │   └── pdf.py                # PDF ticket generation
│   │
│   ├── templates/                # Jinja2 HTML templates
│   │   ├── base.html             # Base template (extends all)
│   │   ├── landing.html          # Public landing page
│   │   ├── login_user.html       # User login page
│   │   ├── login_admin.html      # Admin login page
│   │   ├── dashboard_user.html   # User dashboard
│   │   ├── dashboard_admin.html  # Admin dashboard
│   │   └── scan.html             # QR scanner interface
│   │
│   ├── static/                   # Static assets
│   │   ├── css/                  # Stylesheets
│   │   ├── js/                   # JavaScript files
│   │   └── qr/                   # Generated QR code images
│   │
│   └── data/                     # JSON data storage
│       ├── users.json            # User accounts (encrypted)
│       ├── tickets.json          # Ticket records (encrypted)
│       └── attendance.json       # Check-in records (encrypted)
│
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── vercel.json                   # Vercel deployment config
```

## 🚀 How to Run Locally

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd event-ticketing-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the development server**
   ```bash
   cd app
   flask run
   # or
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## 🌐 Deploy to Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   vercel
   ```

3. **Follow the prompts** to configure your deployment

## 🔐 Security Notes

- All secrets are hardcoded in `app/utils/security.py` for simplicity
- Passwords are hashed using bcrypt
- JSON data is encrypted using Fernet symmetric encryption
- QR payloads are signed with HMAC for tamper detection
- **For production**: Consider moving secrets to a secure vault

## 📝 Features Overview

| Feature | Admin | User |
|---------|-------|------|
| Login/Logout | ✅ | ✅ |
| View Dashboard | ✅ | ✅ |
| Create Tickets | ✅ | ❌ |
| View Tickets | ✅ | ✅ (own only) |
| Download QR Code | ✅ | ✅ |
| Download PDF Ticket | ✅ | ✅ |
| Scan QR Codes | ✅ | ❌ |
| View Attendance | ✅ | ✅ (own only) |
| Manage Users | ✅ | ❌ |

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Storage**: Encrypted JSON files
- **Security**: bcrypt, Fernet (cryptography)
- **QR Codes**: qrcode, Pillow
- **PDF**: ReportLab
- **Deployment**: Vercel

---

*This project is structured for architecture clarity. Business logic implementation is pending.*

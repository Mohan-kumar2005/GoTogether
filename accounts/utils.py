
import logging
import json
import os

from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from django.utils.html import escape

logger = logging.getLogger(__name__)


def send_otp_email(user, otp):
    """
    Send an OTP verification email using the Brevo HTTPS API.

    Returns:
        (True, success_message) if accepted by Brevo.
        (False, error_message) if sending fails.
    """

    if not user.email:
        logger.warning(
            "OTP email not sent because user %s has no email address.",
            user.username,
        )
        return False, "No email address found for this account."

    api_key = os.environ.get("BREVO_API_KEY", "").strip()
    sender_email = os.environ.get("BREVO_SENDER_EMAIL", "").strip()

    if not api_key or not sender_email:
        logger.error("Brevo email environment variables are missing.")
        return False, "Email service is not configured."

    subject = f"GoTogether Verification Code: {otp}"

    display_name = escape(user.first_name or user.username)
    safe_otp = escape(str(otp))

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GoTogether Verification Code</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f8fafc;
                margin: 0;
                padding: 20px;
            }}
            .email-container {{
                max-width: 580px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 16px;
                overflow: hidden;
                border: 1px solid #e2e8f0;
            }}
            .email-header {{
                background: #e85a1d;
                padding: 30px 20px;
                text-align: center;
                color: white;
            }}
            .email-header h1 {{
                margin: 0;
                font-size: 26px;
                font-weight: 800;
            }}
            .email-header p {{
                margin: 8px 0 0;
                font-size: 13px;
            }}
            .email-body {{
                padding: 30px;
                color: #334155;
                line-height: 1.7;
            }}
            .otp-box {{
                background: #fff7ed;
                border: 2px dashed #ea580c;
                border-radius: 12px;
                padding: 20px;
                text-align: center;
                margin: 25px 0;
            }}
            .otp-code {{
                font-size: 36px;
                font-weight: bold;
                letter-spacing: 8px;
                color: #ea580c;
                font-family: monospace;
            }}
            .otp-expiry {{
                font-size: 12px;
                color: #64748b;
                margin-top: 8px;
            }}
            .safety-note {{
                background: #f1f5f9;
                border-left: 4px solid #0ea5e9;
                padding: 12px 16px;
                border-radius: 6px;
                font-size: 13px;
                color: #475569;
                margin: 20px 0;
            }}
            .email-footer {{
                background: #0f172a;
                padding: 20px;
                text-align: center;
                color: #cbd5e1;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <h1>GoTogether</h1>
                <p>Share Rides &bull; Share Costs &bull; Reach Home Safe</p>
            </div>
            <div class="email-body">
                <h2 style="color: #0f172a; margin-top: 0;">
                    Hello {display_name},
                </h2>
                <p>
                    Thank you for signing up on <strong>GoTogether</strong>.
                    Use the verification code below to verify your account.
                </p>
                <div class="otp-box">
                    <div class="otp-code">{safe_otp}</div>
                    <div class="otp-expiry">
                        Valid for the next 15 minutes.
                    </div>
                </div>
                <div class="safety-note">
                    <strong>Safety Reminder:</strong>
                    Never share this OTP with anyone.
                    Our team will never ask for your password or OTP.
                </div>
                <p style="font-size: 13px; color: #64748b;">
                    If you did not request this code, please disregard
                    this email.
                </p>
            </div>
            <div class="email-footer">
                &copy; 2026 GoTogether.
                Share rides and reach home safely.
            </div>
        </div>
    </body>
    </html>
    """

    plain_message = f"""
GoTogether - Verification Code

Hello {user.first_name or user.username},

Your verification OTP is: {otp}

This code is valid for 15 minutes.

Share Rides - Share Costs - Reach Home Safe

If you did not request this code, please disregard this email.
"""

    payload = {
        "sender": {
            "name": "GoTogether",
            "email": sender_email,
        },
        "to": [
            {"email": user.email}
        ],
        "subject": subject,
        "htmlContent": html_content,
        "textContent": plain_message,
    }

    request = Request(
        "https://api.brevo.com/v3/smtp/email",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=20) as response:
            if response.status in (200, 201, 202):
                logger.info(
                    "Brevo accepted OTP email for %s",
                    user.email,
                )
                return True, f"OTP sent to {user.email}"

            logger.error(
                "Brevo returned unexpected HTTP status %s",
                response.status,
            )
            return False, "Email could not be sent. Please try again."

    except HTTPError as exc:
        # Log the status, but never log the API key or OTP.
        logger.error("Brevo API returned HTTP status %s", exc.code)
        return False, "Email service rejected the request. Please try again."

    except (URLError, TimeoutError, OSError):
        logger.exception("Brevo email request failed.")
        return False, "Email service is unavailable. Please try again later."

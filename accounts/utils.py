import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

def send_otp_email(user, otp):
    """
    Sends a real-time OTP verification email to the user's Gmail / email address.
    Returns: (bool success, str message)
    """
    if not user.email:
        return False, "No email address found for this account."

    subject = f"🚗 GoTogether Verification Code: {otp}"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'GoTogether <noreply@gotogether.com>')
    to_email = [user.email]

    # HTML Email Template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f8fafc; margin: 0; padding: 20px; }}
            .email-container {{ max-width: 580px; margin: 0 auto; background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; }}
            .email-header {{ background: linear-gradient(135deg, #e85a1d 0%, #f47e20 100%); padding: 30px 20px; text-align: center; color: white; }}
            .email-header h1 {{ margin: 0; font-size: 24px; font-weight: 800; }}
            .email-header p {{ margin: 5px 0 0; opacity: 0.9; font-size: 13px; }}
            .email-body {{ padding: 35px 30px; color: #334155; line-height: 1.6; }}
            .otp-box {{ background: #fff7ed; border: 2px dashed #ea580c; border-radius: 12px; padding: 20px; text-align: center; margin: 25px 0; }}
            .otp-code {{ font-size: 38px; font-weight: 800; letter-spacing: 8px; color: #ea580c; display: inline-block; font-family: monospace; }}
            .otp-expiry {{ font-size: 12px; color: #64748b; margin-top: 8px; }}
            .festival-badge {{ display: inline-block; background: #fef3c7; color: #92400e; font-weight: bold; font-size: 11px; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; margin-bottom: 15px; }}
            .safety-note {{ background: #f1f5f9; border-left: 4px solid #0ea5e9; padding: 12px 16px; border-radius: 6px; font-size: 13px; color: #475569; margin: 20px 0; }}
            .email-footer {{ background: #0f172a; padding: 20px; text-align: center; color: #94a3b8; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <h1>GoTogether</h1>
                <p>Share Rides • Share Costs • Reach Home Safe</p>
            </div>
            <div class="email-body">
                
                <h2 style="color: #0f172a; margin-top: 0; font-size: 20px;">Hello {user.first_name or user.username},</h2>
                <p>Thank you for signing up on <strong>GoTogether</strong>. Use the 6-digit verification code below to verify your account and start sharing 2-wheeler & 4-wheeler festival rides:</p>
                
                <div class="otp-box">
                    <div class="otp-code">{otp}</div>
                    <div class="otp-expiry">⏳ Valid for the next 15 minutes</div>
                </div>

                <div class="safety-note">
                    <strong>🛡️ Safety Reminder:</strong> Never share this OTP with anyone. Our team will never ask for your password or verification code.
                </div>

                <p style="font-size: 13px; color: #64748b;">If you did not request this verification code, please disregard this email.</p>
            </div>
            <div class="email-footer">
                &copy; 2026 GoTogether. Helping commuters beat high festival bus fares with verified community rides.
            </div>
        </div>
    </body>
    </html>
    """

    plain_message = f"""
GoTogether - Verification Code

Hello {user.first_name or user.username},

Your verification OTP is: {otp}

This code is valid for 15 minutes. Enter it to verify your account on GoTogether.

Share Rides • Share Costs • Reach Home Safe
    """

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=from_email,
            to=to_email
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        logger.info(f"OTP email sent successfully to {user.email}")
        return True, f"OTP has been dispatched to your Gmail inbox: {user.email}"
    except Exception as e:
        logger.error(f"Failed to send email to {user.email}: {e}")
        return False, str(e)

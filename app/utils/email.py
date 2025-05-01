# # utils/email.py

# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# from pydantic import BaseModel, EmailStr
# import os

# conf = ConnectionConfig(
#     MAIL_USERNAME="your_email@example.com",
#     MAIL_PASSWORD="your_password",
#     MAIL_FROM="your_email@example.com",
#     MAIL_PORT=587,
#     MAIL_SERVER="smtp.gmail.com",  # or smtp.sendgrid.net
#     MAIL_TLS=True,
#     MAIL_SSL=False,
#     USE_CREDENTIALS=True
# )

# class EmailSchema(BaseModel):
#     email: EmailStr
#     subject: str
#     body: str
#     qr_base64: str

# async def send_email_with_qr(email_data: EmailSchema):
#     html = f"""
#     <p>{email_data.body}</p>
#     <img src="data:image/png;base64,{email_data.qr_base64}" />
#     """
#     message = MessageSchema(
#         subject=email_data.subject,
#         recipients=[email_data.email],
#         body=html,
#         subtype="html"
#     )
#     fm = FastMail(conf)
#     await fm.send_message(message)




import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "codingupta@gmail.com"  # your email
EMAIL_PASSWORD = "pkvd ssrv zwnz lvky"  # app password if using Gmail

def send_email_with_qr_code(to_email: str, qr_code_base64: str, registration_id: str):
    print("Sending email to:", to_email)
    print("QR Code Base64:", qr_code_base64)
    print("Registration ID:", registration_id)
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = "Your Event Registration QR Code"

    # Text content for the email
    body = f"Hello, \n\nThank you for registering. Please find your QR code for event registration below.\n\nRegistration ID: {registration_id}"
    msg.attach(MIMEText(body, 'plain'))

    # Convert base64 QR code into image
    img_data = base64.b64decode(qr_code_base64)
    img = MIMEImage(img_data, name=f"registration_{registration_id}.png")
    msg.attach(img)

    # Sending the email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_ADDRESS, to_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

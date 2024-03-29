import smtplib
from email.message import EmailMessage
import config.database as database
import os
from dotenv import load_dotenv

load_dotenv()


def email(remail: str,doctor:bool):

    if doctor:
      cursor = database.unverified_doc.find_one({"email": remail})
    else:
      cursor = database.unverified_user.find_one({"email": remail})
    if not cursor:
        return

    message = EmailMessage()
    # The mail addresses and password
    sender_address = os.getenv('EMAIL_ID')
    sender_pass = os.getenv('EMAIL_PASS')
    receiver_address = remail
    message['From'] = sender_address
    message['To'] = receiver_address
    # The subject line
    message['Subject'] = 'Well-Being Welcomes you to the family'

    # Setup the MIME

    message.set_content(
        f'''
    <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <title>Please verify your account.</title>
        <style>
          .wrapper {{
            padding: 20px;
            color: #444;
            font-size: 1.3em;
          }}
          a {{
            background: #592f80;
            text-decoration: none;
            padding: 8px 15px;
            border-radius: 5px;
            color: #fff;
          }}
        </style>
      </head>
      <body>
        <div class="wrapper">
          <p>Thank you for signing up on Well-Being. Please click on the link below to verify your account and stay healthy.</p>
          <br>
          <a href="https://hackathoniitp.herokuapp.com/users/email_verification/{cursor["email_token"]}" style="text-decoration : none;color:white; ">Verify Email!</a>
        </div>
      </body>
      </html>
        ''',
        subtype="html")

    # The body and the attachments for the mail
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    print('Mail Sent')
    session.quit()

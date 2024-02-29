import traceback
from flask import Flask, jsonify, request
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

load_dotenv();

class mailUtility:

    @staticmethod
    def sendMail(mailObj, email):
        try:
            mail_obj = mailObj
            # mail_dict = dict(mail_obj)

            # Set up 
            mail_server = smtplib.SMTP('smtp.gmail.com', 587)
            mail_server.starttls()

            # Log in to the email server
            mail_server.login(os.getenv('SMTP_EMAILID'), os.getenv('SMTP_PASSWORD'))

            message = MIMEMultipart()
            message['From'] = 'gitlatnip91@gmail.com'
            message['To'] = email
            message['Subject'] = mail_obj['subject']
            message.attach(MIMEText(mail_obj['description'], 'html'))
            print("M A I L : ",message)

            mail_server.sendmail('gitlatnip91@gmail.com', email, message.as_string())

            mail_server.quit()

            # return jsonify({'message': 'Email sent successfully', 'success': True}), 200

        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            # return jsonify({'message': 'Error occurred while sending email', 'success': False}), 500
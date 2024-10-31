
from email_validator import validate_email, EmailNotValidError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib
import random

        
class Email():
    def __init__(self, customer_email: str) -> None:
        self.customer_email = customer_email   
        self.send_email = None
    
    def send_email(self, subject: str, email_body: str):
        """This method won't be used for now, but it's here for future use."""
        if not self.is_valid_email(self.customer_email):
            return False, "Invalid email address"
        
        email = MIMEMultipart()
        email["From"] = self.bank_email
        email["To"] = self.customer_email
        email["Subject"] = subject
        
        email.attach(MIMEText(email_body, "plain"))

        context = ssl.create_default_context()
        
        
        """This part is also not compatible with the current project,
        but it's here for future use and modification."""
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(self.sender_email, self.password)
                smtp.sendmail(self.send_email, self.customer_email, email.as_string())
                return True, "Email sent successfully"
        except smtplib.SMTPAuthenticationError as e:
            return False, "Failed to authenticate with the SMTP server:", e
        except smtplib.SMTPRecipientsRefused as e:
            return False, "All recipient addresses were refused:", e
        except smtplib.SMTPSenderRefused as e:
            return False, "The sender address was refused:", e
        except smtplib.SMTPDataError as e:
            return False, "The SMTP server replied with an unexpected error code:", e
        except smtplib.SMTPConnectError as e:
            return False, "Failed to connect to the SMTP server:", e
        except smtplib.SMTPHeloError as e:
            return False, "The server refused our HELO message:", e
        except smtplib.SMTPNotSupportedError as e:
            return False, "The SMTP server does not support the STARTTLS extension:", e
        except smtplib.SMTPException as e:
            return False, "An error occurred during the SMTP transaction:", e
        except Exception as e:
            return False, "An unexpected error occurred:", e
    
    @staticmethod
    def get_verification_code() -> str:
        return str(random.randint(100000, 999999))
    
    def is_valid_email(email: str) -> bool:
        try:
            valid = validate_email(email)
            email = valid.email
            return True
        except EmailNotValidError:
            return False
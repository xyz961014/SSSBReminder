import os
import smtplib
import email
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import argparse
import ipdb

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mail_to", type=str, nargs="+", required=True,
                        help="Receiver email address")
    parser.add_argument("--title", type=str, default="SSSB Update!",
                        help="Mail title")
    parser.add_argument("--content", type=str, default="SSSB Update content!",
                        help="Mail content")

    args = parser.parse_args()
    return args


# Username, email address created via the console
username = os.environ["MAIL_USERNAME"]
# Password, SMTP password created via the console
password = os.environ["MAIL_PASSWORD"]
# Custom reply-to address, unrelated to the console settings. 
# The email sender address does not receive mail, and any replies will be redirected to this reply-to address.
mail_from = os.environ["MAIL_FROM"]
#replyto = None


def main(args):
    # Displayed To recipient address
    rcptto = args.mail_to
    # Displayed Cc recipient address
    rcptcc = []
    # Bcc recipient address, Bcc recipients will not be displayed on the email but will receive the email
    rcptbcc = []
    # All recipient addresses, including Cc addresses. No more than 60 recipients in a single send.
    receivers = rcptto

    msg = build_message(rcptto, args.title, args.content, 
                        rcptcc=rcptcc, rcptbcc=rcptbcc)
    send_mail(receivers, msg)

def build_message(rcptto, title, content, rcptcc=[], rcptbcc=[]):
    
    # Construct an alternative structure
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(title)
    msg['From'] = formataddr(["SSSB Reminder", mail_from])  # Nickname + sender address (or alias)
    # Convert list to string
    msg['To'] = ",".join(rcptto)
    msg['Cc'] = ",".join(rcptcc)
    #msg['Reply-to'] = replyto
    msg['Message-id'] = email.utils.make_msgid()
    msg['Date'] = email.utils.formatdate()
    
    # If you need to enable email tracking services, please use the following code to set the tracking link header.
    # First, the domain needs to be registered, and the correct CNAME configuration must be set; second, you need to tag the email, 
    # this tag has been created and exists on the console. The tag can be used 10 minutes after creation.
    # Set tracking link header
    # tagName = 'xxxxxxx'
    #
    # # OpenTrace corresponds to the string '1', fixed
    # trace = {
    #     "OpenTrace": '1',  # Enable email open tracking
    #     "LinkTrace": '1',  # Track clicks on URLs within the email
    #     "TagName": tagName  # Tag name created on the console
    # }
    # jsonTrace = json.dumps(trace)
    # base64Trace = str(base64.b64encode(jsonTrace.encode('utf-8')), 'utf-8')
    # # print(base64Trace)
    # msg.add_header("X-AliDM-Trace", base64Trace)
    
    
    # Construct the text/plain part of the alternative
    # textplain = MIMEText('Custom TEXT plain text part', _subtype='plain', _charset='UTF-8')
    # msg.attach(textplain)
    
    # Construct the text/html part of the alternative
    texthtml = MIMEText(content, _subtype='html', _charset='UTF-8')
    msg.attach(texthtml)
    
    # Attachments
    # files = [r'C:\Users\Downloads\test1.jpg', r'C:\Users\Downloads\test2.jpg']
    # for t in files:
    #     part_attach1 = MIMEApplication(open(t, 'rb').read())  # Open attachment
    #     part_attach1.add_header('Content-Disposition', 'attachment', filename=t.rsplit('\\', 1)[1])  # Name the attachment
    #     msg.attach(part_attach1)  # Add attachment

    return msg


def send_mail(receivers, msg):
    try:
        # If you need to use SSL for encryption, you can create a client like this
        client = smtplib.SMTP('smtp.eu.mailgun.org', 587)
        # Enable DEBUG mode
        client.set_debuglevel(0)
        # The sender and authentication address must match
        client.login(username, password)
        # Note: If you want to get the return value of the DATA command, 
        # you can refer to the sendmail method of smtplib:
        # Use SMTP.mail/SMTP.rcpt/SMTP.data methods
        # print(receivers)
        client.sendmail(username, receivers, msg.as_string())  # Supports multiple recipients, up to 60
        client.quit()
        print('Email sent successfully!')
    except smtplib.SMTPConnectError as e:
        print('Email sending failed, connection failed:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPAuthenticationError as e:
        print('Email sending failed, authentication error:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPSenderRefused as e:
        print('Email sending failed, sender refused:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPRecipientsRefused as e:
        print('Email sending failed, recipient refused:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPDataError as e:
        print('Email sending failed, data reception refused:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPException as e:
        print('Email sending failed,', str(e))
    except Exception as e:
        print('Email sending exception,', str(e))


if __name__ == "__main__":
    args = parse_args()
    main(args)

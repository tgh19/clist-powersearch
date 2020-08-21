import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

PASSWORD = ''
SRC_EMAIL = ''
DEST_EMAIL = ''

def send_email(post_title, post_url):
    mail_content = f"""{post_title} {post_url}"""

    #The mail addresses and password
    sender_address = SRC_EMAIL
    sender_pass = PASSWORD
    receiver_address = DEST_EMAIL

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = ''
    message.attach(MIMEText(mail_content, 'plain'))

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) # Use gmail with port
    session.starttls() # Enable security
    session.login(sender_address, sender_pass) # Login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('post sent')
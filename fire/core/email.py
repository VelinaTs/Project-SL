import smtplib
from email.mime.text import MIMEText

# sydyrjanie Email 
def send_email(barber, chas):
    subject = "Removed chas"
    body = f"Часът на {chas.firstname} {chas.lastname} за {chas.date} в {chas.time} е бил премахнат. Моля, проверете вашия профил за повече информация."
    sender_email = "project.test.email.sl@gmail.com"
    receiver_email = barber.username
    password = "YnNh768j"
    
    # syobshtenie
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    # Connect to the Gmail SMTP server and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)

    print("Email sent!")
    
    
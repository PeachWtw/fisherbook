from flask import current_app, render_template
from flask_mail import Message
from threading import Thread
from app import mail

def send_async_email(app,msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass
def send_mail(to, subject, template, **kwargs):
    msg = Message(subject='[鱼书]'+' '+ subject,recipients=[to],
                  sender=current_app.config['MAIL_USERNAME'])
    msg.html = render_template(template,**kwargs)
    # mail.send(msg)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
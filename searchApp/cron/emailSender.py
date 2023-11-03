import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import logging

providers = [
    {
        'sender': 'cata.briscan@gmail.com',
        'smtp_user': 'catalin.briscan@feedcheck.co',
        'smtp_password': 'feedback12#',
        'smtp_endpoint': 'smtp.mailjet.com',  # https://app.mailjet.com/account/setup?_ga=2.98234139.568521340.1655818924-1911686189.1650629369&_gac=1.24974664.1653995756.Cj0KCQjw-daUBhCIARIsALbkjSZx9JYq8_u8fY8VXxwQHacNSDSf4kmIL_nDBx_9hjre7zo0AtTOm_YaAgA3EALw_wcB
        'smtp_port': 587
    },
]


def sendEmail(to, subject, text, sendFrom='', files=[], fromField='', cc=[], replyTo=[]):
    """
    To parameter may have multiple email addresses separated by comma
    """
    provider = providers[0]
    msg = MIMEMultipart()
    # ATTENTION: make DNS setup for every domain at whitelabel
    # https://app.mailjet.com/account/sender
    msg['From'] = fromField or 'FastCompete <{}>'.format(sendFrom or provider['sender'])
    msg['To'] = to
    if cc:
        msg['CC'] = ",".join(cc)
    if replyTo:
        msg['Reply-To'] = ",".join(replyTo)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text, 'html'))

    # add attachments
    for file in files:
        with open(file, "rb") as f:
            part = MIMEApplication(
                f.read(),
                Name=basename(file)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(file))
        msg.attach(part)

    smtp = smtplib.SMTP(provider['smtp_endpoint'], provider['smtp_port'])
    smtp.ehlo()
    smtp.starttls()
    smtp.login(provider['smtp_user'], provider['smtp_password'])
    try:
        """
        Here we need to add all addresses in to field:
        https://stackoverflow.com/a/1546435/769677
        """
        to_address = to.split(',') + cc
        smtp.sendmail(msg['From'], to_address, msg.as_string())
    except Exception as e:
        logging.exception("Send mail exception")
    finally:
        smtp.close()


if __name__ == '__main__':
    sendEmail("cata.briscan@gmail.com", "Email test: I love Dora!", "This is a <b>test</b> mail!",
              replyTo=['catalin.briscan@feedcheck.co', 'cata.briscan@gmail.com'])

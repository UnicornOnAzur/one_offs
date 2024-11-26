"""
@author: UnicornOnAzur

This module provides functionality to create and send emails with optional
attachments. It supports both SSL and TLS protocols for secure email
transmission.
"""
# Standard library
import email.message
import smtplib
import typing


class Attachment:
    """Class to represent an email attachment."""
    TYPES: dict = {"csv": ("text", "csv"),
                   "doc": ("application", "msword"),
                   "gif": ("image", "gif"),
                   "html": ("text", "html"),
                   "jpg": ("image", "jpeg"),
                   "json": ("application", "json"),
                   "mp3": ("audio", "mpeg"),
                   "mp4": ("video", "mp4"),
                   "pdf": ("application", "pdf"),
                   "png": ("image", "png"),
                   "ppt": ("application", "vnd.ms-powerpoint"),
                   "txt": ("text", "plain"),
                   "xlm": ("application", "vnd.ms-excel"),
                   "xls": ("application", "vnd.ms-excel"),
                   "xlsx": (
                    "application",
                    "vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                   "xml": ("application", "xml"),
                   "zip": ("application", "zip")}

    def __init__(self, file: bytes, filename):
        self.data = file
        self.filename = filename
        # determine the maintype and subtype
        self.maintype, self.subtype = self._get_mime_type()

    def _get_mime_type(self) -> typing.Tuple[str, str]:
        """Retrieve the MIME type based on the file extension."""
        return Attachment.TYPES.get(self.filename.split(".")[-1],
                                    ("application", "octet-stream"))


def create_message(subject: str,
                   sender: str,
                   recipients: list,
                   content: str,
                   attachments: typing.Optional[typing.List] = None
                   ) -> email.message.EmailMessage:
    """
    Create an email message with optional attachments.

    Parameters
    ----------
    subject : str
        The subject of the email.
    sender : str
        The sender's email address.
    recipients : list
        A list of recipient email addresses.
    content : str
        The body content of the email.
    attachments : Optional[List[Attachment]]
        A list of Attachment objects to include in the email.

    Returns
    -------
    email.message.EmailMessage
        The constructed email message.
    """
    msg = email.message.EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg.set_content(content)
    if attachments:
        for attachment in attachments:
            msg.add_attachment(attachment.data,
                               maintype=attachment.maintype,
                               subtype=attachment.subtype,
                               filename=attachment.filename)
    return msg


def send_mail_ssl(host: str,
                  port: int,
                  user: str,
                  password: str,
                  message: email.message.EmailMessage) -> bool:
    """
    Send an email using SSL.

    Parameters
    ----------
    host : str
        The SMTP server host.
    port : int
        The port to connect to the SMTP server.
    user : str
        The username for authentication.
    password : str
        The password for authentication.
    message : email.message.EmailMessage
        The email message to be sent.

    Returns
    -------
    bool
        True if the email was sent successfully, False otherwise.
    """
    with smtplib.SMTP_SSL(host=host, port=port) as smtp_server:
        response_code, response_line = smtp_server.login(user=user,
                                                         password=password)
        print(response_code, response_line.decode("utf-8"))
        failed_recipients: dict = smtp_server.send_message(msg=message)
    return not failed_recipients


def send_mail_tls(host: str,
                  port: int,
                  user: str,
                  password: str,
                  message: email.message.EmailMessage) -> bool:
    """
    Send an email using TLS.

    Parameters
    ----------
    host : str
        The SMTP server host.
    port : int
        The port to connect to the SMTP server.
    user : str
        The username for authentication.
    password : str
        The password for authentication.
    message : email.message.EmailMessage
        The email message to be sent.

    Returns
    -------
    bool
        True if the email was sent successfully, False otherwise.
    """
    with smtplib.SMTP(host=host, port=port) as smtp_server:
        smtp_server.starttls()
        response_code, response_line = smtp_server.login(user=user,
                                                         password=password)
        print(response_code, response_line.decode("utf-8"))
        failed_recipients: dict = smtp_server.send_message(msg=message)
    return not failed_recipients


def demo():
    """Demonstrate sending an email with an attachment."""
    # Standard library
    import io
    import os
    # Third party
    import dotenv

    dotenv.load_dotenv()
    username = os.getenv("GOOGLE_USERNAME")
    password = os.getenv("GOOGLE_APP_PASSWORD")
    file = Attachment(io.BytesIO(b'This is a test file.').read(), "test.txt")
    message = create_message("test...",
                             username,
                             [username],
                             "mail mail mail",
                             [file])
    send_mail_tls("smtp.gmail.com",
                  587,
                  username,
                  password,
                  message)


if __name__ == "__main__":
    demo()

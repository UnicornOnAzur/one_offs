import base64
from email.base64mime import body_encode as encode_base64
import email.message
import email.utils
import re
import smtplib
import socket
import ssl
#
MAXLINE: int = 8192


def step_1(
        host: str, port: int, user: str, password: str, title: str, body: str):
    """
    Sends an email using the SMTP protocol with a context manager and the high
    level send_message function.

    Parameters:
    - host: SMTP server address
    - port: SMTP server port
    - user: Sender's email address
    - password: Sender's email password
    - title: Subject of the email
    - body: Body content of the email
    """
    message = email.message.EmailMessage()
    message["Subject"] = f"{title} 1"
    message["From"] = user
    message["To"] = user
    message.set_content(body)

    # Connect
    with smtplib.SMTP(host=host, port=port) as smtp_server:
        # Start TLS
        smtp_server.starttls()
        # Login
        smtp_server.login(user=user, password=password)
        # Send mail
        smtp_server.send_message(message)
    # Close


def step_2(
        host: str, port: int, user: str, password: str, title: str, body: str):
    """
    Remove the context manager. Unpack the login function and replace the
    send_message to sendmail.

    Parameters: (no change)
    """
    message = "\r\n".join([f"Subject: {title} 2",
                           f"From: {user}", f"To: {user}",
                           'Content-Type: text/plain; charset="utf-8"',
                           "Content-Transfer-Encoding: 7bit",
                           "MIME-Version: 1.0\r\n",
                           body, ""]).encode("utf-8")
    smtp_server = smtplib.SMTP()
    # Connect
    smtp_server.connect(host=host, port=port)
    # Start TLS
    smtp_server.starttls()
    # Login
    smtp_server.ehlo_or_helo_if_needed()
    authmethod = "plain"
    smtp_server.user, smtp_server.password = user, password
    method_name = "auth_" + authmethod.lower().replace("-", "_")
    smtp_server.auth(authmethod, getattr(smtp_server, method_name), initial_response_ok=True)
    # Send mail
    smtp_server.sendmail(user, user, message)
    # Close
    smtp_server.quit()


def step_3(
        host: str, port: int, user: str, password: str, title: str, body: str):
    """
    Unwrap up until the docmd methods

    Parameters: (no change)
    """
    message = "\r\n".join([f"Subject: {title} 3",
                           f"From: {user}", f"To: {user}",
                           'Content-Type: text/plain; charset="utf-8"',
                           "Content-Transfer-Encoding: 7bit",
                           "MIME-Version: 1.0\r\n",
                           body, ""]).encode("utf-8")
    smtp_server = smtplib.SMTP()
    # Connect
    smtp_server.connect(host=host, port=port)
    # Start TLS
    smtp_server.ehlo_or_helo_if_needed()
    (resp, _) = smtp_server.docmd("STARTTLS")
    if resp == 220:
        context = ssl._create_stdlib_context()
    smtp_server.sock = context.wrap_socket(smtp_server.sock,
                                           server_hostname=smtp_server._host)
    smtp_server.file = None
    smtp_server.ehlo_resp = None
    # Login
    smtp_server.ehlo_or_helo_if_needed()
    authmethod = "PLAIN"
    smtp_server.user, smtp_server.password = user, password
    method_name = "auth_" + authmethod.lower().replace("-", "_")
    authobject = getattr(smtp_server, method_name)
    initial_response = authobject()
    response = encode_base64(initial_response.encode(smtp_server.command_encoding), eol='')
    _ = smtp_server.docmd("AUTH", authmethod + " " + response)
    # Send mail
    smtp_server.ehlo_or_helo_if_needed()
    smtp_server.mail(user)
    smtp_server.rcpt(user)
    smtp_server.data(message)
    # Close
    smtp_server.docmd("quit")
    smtp_server.close()


def step_4(
        host: str, port: int, user: str, password: str, title: str, body: str):
    """
    Unwrap the docmd to putcmd and getreply

    Parameters: (no change)
    """
    message = "\r\n".join([f"Subject: {title} 4",
                           f"From: {user}", f"To: {user}",
                           'Content-Type: text/plain; charset="utf-8"',
                           "Content-Transfer-Encoding: 7bit",
                           "MIME-Version: 1.0\r\n",
                           body, ""]).encode("utf-8")
    smtp_server = smtplib.SMTP()
    # Connect
    smtp_server.connect(host=host, port=port)
    # Start TLS
    smtp_server.putcmd(smtp_server.ehlo_msg, smtp_server.local_hostname)
    (_, msg) = smtp_server.getreply()
    smtp_server.ehlo_resp = msg
    smtp_server.putcmd("STARTTLS")
    (resp, _) = smtp_server.getreply()
    if resp == 220:
        context = ssl._create_stdlib_context()
    smtp_server.sock = context.wrap_socket(smtp_server.sock,
                                           server_hostname=smtp_server._host)
    smtp_server.file = None
    smtp_server.ehlo_resp = None
    # Login
    smtp_server.putcmd(smtp_server.ehlo_msg, smtp_server.local_hostname)
    smtp_server.getreply()
    authmethod = "plain"
    smtp_server.user, smtp_server.password = user, password
    method_name = "auth_" + authmethod.lower().replace("-", "_")
    authobject = getattr(smtp_server, method_name)
    initial_response = authobject()
    response = encode_base64(initial_response.encode(smtp_server.command_encoding), eol='')
    smtp_server.putcmd("AUTH", authmethod + " " + response)
    smtp_server.getreply()
    # Send mail
    smtp_server.putcmd(smtp_server.ehlo_msg, smtp_server.local_hostname)
    smtp_server.getreply()
    _, addr = email.utils.parseaddr(user)
    smtp_server.putcmd("mail", f"from:<{addr}>")
    smtp_server.getreply()
    smtp_server.putcmd("rcpt", f"to:<{addr}>")
    smtp_server.getreply()
    smtp_server.putcmd("data")
    smtp_server.getreply()
    message_bytes = re.sub(br"(?m)^\.", b"..", message)
    if message_bytes[-2:] != smtplib.bCRLF:
        message_bytes = message_bytes + smtplib.bCRLF
    message_bytes = message_bytes + b"." + smtplib.bCRLF
    smtp_server.send(message_bytes)
    smtp_server.getreply()
    # Close
    smtp_server.putcmd("quit")
    smtp_server.close()


def step_5(
        host: str, port: int, user: str, password: str, title: str, body: str):
    """
    Unwrap the putcmd to send

    Parameters: (no change)
    """
    message = "\r\n".join([f"Subject: {title} 5",
                           f"From: {user}", f"To: {user}",
                           'Content-Type: text/plain; charset="utf-8"',
                           "Content-Transfer-Encoding: 7bit",
                           "MIME-Version: 1.0\r\n",
                           body, ""]).encode("utf-8")
    smtp_server = smtplib.SMTP()
    # Connect
    smtp_server.connect(host=host, port=port)
    # Start TLS
    smtp_server.send(f"{smtp_server.ehlo_msg} {smtp_server.local_hostname} {smtplib.CRLF}".encode("utf-8"))
    (_, msg) = smtp_server.getreply()
    smtp_server.ehlo_resp = msg
    smtp_server.send(f"STARTTLS {smtplib.CRLF}".encode("utf-8"))
    (resp, _) = smtp_server.getreply()
    if resp == 220:
        context = ssl._create_stdlib_context()
    smtp_server.sock = context.wrap_socket(smtp_server.sock,
                                           server_hostname=smtp_server._host)
    smtp_server.file = None
    smtp_server.ehlo_resp = None
    # Login
    smtp_server.send(f"{smtp_server.ehlo_msg} {smtp_server.local_hostname} {smtplib.CRLF}".encode("utf-8"))
    smtp_server.getreply()
    authmethod = "plain"
    smtp_server.user, smtp_server.password = user, password
    method_name = "auth_" + authmethod.lower().replace("-", "_")
    authobject = getattr(smtp_server, method_name)
    initial_response = authobject()
    response = encode_base64(initial_response.encode(smtp_server.command_encoding), eol='')
    smtp_server.send(f"AUTH {authmethod} {response}{smtplib.CRLF}".encode("utf-8"))
    smtp_server.getreply()
    # Send mail
    smtp_server.send(f"{smtp_server.ehlo_msg} {smtp_server.local_hostname} {smtplib.CRLF}".encode("utf-8"))
    smtp_server.getreply()
    _, addr = email.utils.parseaddr(user)
    smtp_server.send(f"mail from:<{addr}> {smtplib.CRLF}".encode("utf-8"))
    smtp_server.getreply()
    smtp_server.send(f"rcpt to:<{addr}> {smtplib.CRLF}".encode("utf-8"))
    smtp_server.getreply()
    smtp_server.send(f"data {smtplib.CRLF}".encode("utf-8"))
    smtp_server.getreply()
    message_bytes = re.sub(br"(?m)^\.", b"..", message)
    if message_bytes[-2:] != smtplib.bCRLF:
        message_bytes = message_bytes + smtplib.bCRLF
    message_bytes = message_bytes + b"." + smtplib.bCRLF
    smtp_server.sock.sendall(message_bytes)
    smtp_server.getreply()
    # Close
    smtp_server.send(f"quit {smtplib.CRLF}".encode("utf-8"))
    smtp_server.close()


def step_6(
        host: str, port: int, user: str, password: str, title: str, body: str):
    """
    Unwrap the send to sock.sendall() and getreply to sock.makefile.

    Parameters: (no change)
    """
    message = "\r\n".join([f"Subject: {title} 6",
                           f"From: {user}", f"To: {user}",
                           'Content-Type: text/plain; charset="utf-8"',
                           "Content-Transfer-Encoding: 7bit",
                           "MIME-Version: 1.0\r\n",
                           body, ""]).encode("utf-8")
    smtp_server = smtplib.SMTP()
    # Connect
    smtp_server.sock = smtp_server._get_socket(host, port, smtp_server.timeout)
    smtp_server._host = host
    smtp_server.sock.makefile("rb").readline(MAXLINE)
    # Start TLS
    smtp_server.sock.sendall(f"{smtp_server.ehlo_msg} {smtp_server.local_hostname} {smtplib.CRLF}".encode("utf-8"))
    msg = smtp_server.sock.makefile("rb").readline(MAXLINE)[4:]
    smtp_server.ehlo_resp = msg
    smtp_server.sock.sendall(f"STARTTLS {smtplib.CRLF}".encode("utf-8"))
    lines = smtp_server.sock.makefile("rb").readline(MAXLINE)
    resp = int(lines[:3])
    if resp == 220:
        context = ssl._create_stdlib_context()
    smtp_server.sock = context.wrap_socket(smtp_server.sock,
                                           server_hostname=smtp_server._host)
    smtp_server.ehlo_resp = None
    # Login
    smtp_server.sock.sendall(f"{smtp_server.ehlo_msg} {smtp_server.local_hostname} {smtplib.CRLF}".encode("utf-8"))
    smtp_server.sock.makefile("rb").readline(MAXLINE)
    authmethod = "plain"
    smtp_server.user, smtp_server.password = user, password
    method_name = "auth_" + authmethod.lower().replace("-", "_")
    authobject = getattr(smtp_server, method_name)
    initial_response = authobject()
    response = encode_base64(initial_response.encode(smtp_server.command_encoding), eol='')
    smtp_server.sock.sendall(f"AUTH {authmethod} {response}{smtplib.CRLF}".encode("utf-8"))
    smtp_server.sock.makefile("rb").readline(MAXLINE)
    # Send mail
    smtp_server.sock.sendall(f"{smtp_server.ehlo_msg} {smtp_server.local_hostname} {smtplib.CRLF}".encode("utf-8"))
    smtp_server.sock.makefile("rb").readline(MAXLINE)
    _, addr = email.utils.parseaddr(user)
    smtp_server.sock.sendall(f"mail from:<{addr}> {smtplib.CRLF}".encode("utf-8"))
    smtp_server.sock.makefile("rb").readline(MAXLINE)
    smtp_server.sock.sendall(f"rcpt to:<{addr}> {smtplib.CRLF}".encode("utf-8"))
    smtp_server.sock.makefile("rb").readline(MAXLINE)
    smtp_server.sock.sendall(f"data {smtplib.CRLF}".encode("utf-8"))
    smtp_server.sock.makefile("rb").readline(MAXLINE)
    message_bytes = re.sub(br"(?m)^\.", b"..", message)
    if message_bytes[-2:] != smtplib.bCRLF:
        message_bytes = message_bytes + smtplib.bCRLF
    message_bytes = message_bytes + b"." + smtplib.bCRLF
    smtp_server.sock.sendall(message_bytes)
    smtp_server.sock.makefile("rb").readline(MAXLINE)
    # Close
    smtp_server.sock.sendall(f"quit {smtplib.CRLF}".encode("utf-8"))
    smtp_server.sock.close()


def step_7(
        host: str, port: int, user: str, password: str, title: str, body: str):
    """
    Remove every last part of the SMTP object.

    Parameters: (no change)
    """
    message = "\r\n".join([f"Subject: {title} 7",
                           f"From: {user}",
                           f"To: {user}",
                           'Content-Type: text/plain; charset="utf-8"',
                           "Content-Transfer-Encoding: 7bit",
                           "MIME-Version: 1.0\r\n",
                           body, ""]).encode("utf-8")
    ehlo_msg = "ehlo"
    local_hostname = socket.getfqdn()
    # Connect
    socket_ = socket.create_connection((host, port))
    socket_.makefile("rb").readline(MAXLINE)
    # Start TLS
    socket_.sendall(f"{ehlo_msg} {local_hostname} {smtplib.CRLF}".encode("utf-8"))
    socket_.makefile("rb").readline(MAXLINE)
    socket_.sendall(f"STARTTLS {smtplib.CRLF}".encode("utf-8"))
    lines = socket_.makefile("rb").readline(MAXLINE)
    resp = int(lines[:3])
    if resp == 220:
        context = ssl._create_stdlib_context()
    socket_ = context.wrap_socket(socket_, server_hostname=host)
    # Login
    socket_.sendall(f"{ehlo_msg} {local_hostname} {smtplib.CRLF}".encode("utf-8"))
    socket_.makefile("rb").readline(MAXLINE)
    authmethod = "plain"
    authobject = lambda: "\0%s\0%s" % (user, password)
    initial_response = authobject()
    response = encode_base64(initial_response.encode('ascii'), eol='')
    socket_.sendall(f"AUTH {authmethod} {response}{smtplib.CRLF}".encode("utf-8"))
    socket_.makefile("rb").readline(MAXLINE)
    # Send mail
    socket_.sendall(f"{ehlo_msg} {local_hostname} {smtplib.CRLF}".encode("utf-8"))
    socket_.makefile("rb").readline(MAXLINE)
    _, addr = email.utils.parseaddr(user)
    socket_.sendall(f"mail from:<{addr}> {smtplib.CRLF}".encode("utf-8"))
    socket_.makefile("rb").readline(MAXLINE)
    socket_.sendall(f"rcpt to:<{addr}> {smtplib.CRLF}".encode("utf-8"))
    socket_.makefile("rb").readline(MAXLINE)
    socket_.sendall(f"data {smtplib.CRLF}".encode("utf-8"))
    socket_.makefile("rb").readline(MAXLINE)
    message_bytes = re.sub(br"(?m)^\.", b"..", message)
    if message_bytes[-2:] != smtplib.bCRLF:
        message_bytes = message_bytes + smtplib.bCRLF
    message_bytes = message_bytes + b"." + smtplib.bCRLF
    socket_.sendall(message_bytes)
    socket_.makefile("rb").readline(MAXLINE)
    # Close
    socket_.sendall(f"quit {smtplib.CRLF}".encode("utf-8"))
    socket_.close()


def demo():
    import os
    import dotenv

    dotenv.load_dotenv()
    username: str = os.getenv("GOOGLE_USERNAME", "")
    password: str = os.getenv("GOOGLE_APP_PASSWORD", "")
    host: str = "smtp.gmail.com"
    port: int = 587
    title: str = "title"
    body: str = "body"

    for step in [step_1, step_2, step_3, step_4, step_5, step_6, step_7]:
        try:
            print(step.__name__)
            step(host, port, username, password, title, body)
        except Exception as e:
            print(step.__name__, e)


if __name__ == "__main__":
    demo()

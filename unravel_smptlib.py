import email.message
import email.utils
import re
import smtplib
import socket
import ssl
#
TITLE: str = "title"
BODY: str = "body"
UTF8: str = "utf-8"


def step_1(host, port, user, password):
    message = email.message.EmailMessage()
    message["Subject"] = f"{TITLE} {1}"
    message["From"] = user
    message["To"] = user
    message.set_content(BODY)

    with smtplib.SMTP(host=host, port=port) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(user=user, password=password)
        smtp_server.send_message(message)


def step_2(host, port, user, password):
    message = "\r\n".join([f"Subject: {TITLE} {2}",
                           f"From: {user}",
                           f"To: {user}",
                           'Content-Type: text/plain; charset="utf-8"',
                           'Content-Transfer-Encoding: 7bit',
                           'MIME-Version: 1.0\r\n',
                           BODY, ""]).encode(UTF8)
    smtp_server = smtplib.SMTP()
    # Connect
    smtp_server.connect(host=host, port=port)
    # Start TLS
    smtp_server.starttls()
    # Login
    smtp_server.login(user=user, password=password)
    # Send mail
    smtp_server.sendmail(user, user, message)
    # Close
    smtp_server.quit()


def step_3(host, port, user, password):
    message = "\r\n".join([f"Subject: {TITLE} {3}",
                           f"From: {user}",
                           f"To: {user}",
                           'Content-Type: text/plain; charset="utf-8"',
                           'Content-Transfer-Encoding: 7bit',
                           'MIME-Version: 1.0\r\n',
                           BODY, ""]).encode(UTF8)
    smtp_server = smtplib.SMTP()
    # Connect
    smtp_server.connect(host=host, port=port)
    # Start TLS
    smtp_server.starttls()
    # Login
    smtp_server.login(user=user, password=password)
    # Send mail
    smtp_server.ehlo_or_helo_if_needed()
    smtp_server.mail(user)
    smtp_server.rcpt(user)
    smtp_server.data(message)
    # Close
    smtp_server.docmd("quit")
    smtp_server.close()


def step_4(host, port, user, password):
    message = "\r\n".join([f"Subject: {TITLE} {4}",
                           f"From: {user}",
                           f"To: {user}",
                           'Content-Type: text/plain; charset="utf-8"',
                           'Content-Transfer-Encoding: 7bit',
                           'MIME-Version: 1.0\r\n',
                           BODY, ""]).encode(UTF8)
    smtp_server = smtplib.SMTP()
    # Connect
    smtp_server.connect(host=host, port=port)
    # Start TLS
    smtp_server.starttls()
    # Login
    smtp_server.login(user=user, password=password)
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
    message_bytes = re.sub(br'(?m)^\.', b'..', message)
    if message_bytes[-2:] != smtplib.bCRLF:
        message_bytes = message_bytes + smtplib.bCRLF
    message_bytes = message_bytes + b"." + smtplib.bCRLF
    smtp_server.send(message_bytes)
    smtp_server.getreply()
    # Close
    smtp_server.putcmd("quit")
    smtp_server.close()


def step_5(host, port, user, password):
    message = "\r\n".join([f"Subject: {TITLE} {5}",
                           f"From: {user}",
                           f"To: {user}",
                           'Content-Type: text/plain; charset="utf-8"',
                           'Content-Transfer-Encoding: 7bit',
                           'MIME-Version: 1.0\r\n',
                           BODY, ""]).encode(UTF8)
    smtp_server = smtplib.SMTP()
    # Connect
    smtp_server.connect(host=host, port=port)
    # Start TLS
    smtp_server.starttls()
    # Login
    smtp_server.login(user=user, password=password)
    # Send mail
    smtp_server.send(f"{smtp_server.ehlo_msg} {smtp_server.local_hostname} {smtplib.CRLF}".encode(UTF8))
    smtp_server.getreply()
    _, addr = email.utils.parseaddr(user)
    smtp_server.send(f"mail from:<{addr}> {smtplib.CRLF}".encode(UTF8))
    smtp_server.getreply()
    smtp_server.send(f"rcpt to:<{addr}> {smtplib.CRLF}".encode(UTF8))
    smtp_server.getreply()
    smtp_server.send(f"data {smtplib.CRLF}".encode(UTF8))
    smtp_server.getreply()
    message_bytes = re.sub(br'(?m)^\.', b'..', message)
    if message_bytes[-2:] != smtplib.bCRLF:
        message_bytes = message_bytes + smtplib.bCRLF
    message_bytes = message_bytes + b"." + smtplib.bCRLF
    smtp_server.sock.sendall(message_bytes)
    smtp_server.getreply()
    # Close
    smtp_server.send(f"quit {smtplib.CRLF}".encode(UTF8))
    smtp_server.close()


def step_6(host, port, user, password):
    # up until sock.sendall() and getreply()
    message = "\r\n".join([f"Subject: {TITLE} {6}",
                           f"From: {user}",
                           f"To: {user}",
                           'Content-Type: text/plain; charset="utf-8"',
                           'Content-Transfer-Encoding: 7bit',
                           'MIME-Version: 1.0\r\n',
                           BODY, ""]).encode(UTF8)
    smtp_server = smtplib.SMTP()
    # Connect
    smtp_server.sock = smtp_server._get_socket(host, port, smtp_server.timeout)
    smtp_server._host = host
    smtp_server.getreply()
    # Start TLS
    smtp_server.starttls()
    # Login
    smtp_server.login(user=user, password=password) # TODO: unwrap this
    # Send mail
    smtp_server.ehlo_or_helo_if_needed()
    _, addr = email.utils.parseaddr(user)
    smtp_server.sock.sendall(f"mail from:<{addr}> {smtplib.CRLF}".encode(UTF8))
    smtp_server.getreply()
    smtp_server.sock.sendall(f"rcpt to:<{addr}> {smtplib.CRLF}".encode(UTF8))
    smtp_server.getreply()
    smtp_server.sock.sendall(f"data {smtplib.CRLF}".encode(UTF8))
    smtp_server.getreply()
    message_bytes = re.sub(br'(?m)^\.', b'..', message)
    if message_bytes[-2:] != smtplib.bCRLF:
        message_bytes = message_bytes + smtplib.bCRLF
    message_bytes = message_bytes + b"." + smtplib.bCRLF
    smtp_server.sock.sendall(message_bytes)
    smtp_server.getreply()
    # Close
    smtp_server.sock.sendall(f"quit {smtplib.CRLF}".encode(UTF8))
    smtp_server.sock.close()


def step_7(host, port, user, password):
    message = "\r\n".join([f"Subject: {TITLE} {7}",
                           f"From: {user}",
                           f"To: {user}",
                           'Content-Type: text/plain; charset="utf-8"',
                           'Content-Transfer-Encoding: 7bit',
                           'MIME-Version: 1.0\r\n',
                           BODY, ""]).encode(UTF8)
    smtp_server = smtplib.SMTP()
    # Connect
    socket_ = socket.create_connection((host, port))
    socket_.makefile("rb")
    smtp_server._host = host
    smtp_server.sock = socket_
    # Start TLS
    smtp_server.ehlo_or_helo_if_needed()
    print(smtp_server.esmtp_features)
    smtp_server.starttls()
    # smtp_server.ehlo_or_helo_if_needed()
    # socket_.sendall(b"STARTTLS" + smtplib.bCRLF)
    # context = ssl._create_stdlib_context()
    # socket_ = context.wrap_socket(socket_, server_hostname=host)
    # Login
    smtp_server.login(user=user, password=password)
    # Send mail
    smtp_server.ehlo_or_helo_if_needed()
    _, addr = email.utils.parseaddr(user)
    socket_.sendall(f"mail from:<{addr}> {smtplib.CRLF}".encode(UTF8))
    socket_.makefile("rb")
    socket_.sendall(f"rcpt to:<{addr}> {smtplib.CRLF}".encode(UTF8))
    socket_.makefile("rb")
    socket_.sendall(f"data {smtplib.CRLF}".encode(UTF8))
    socket_.makefile("rb")
    message_bytes = re.sub(br'(?m)^\.', b'..', message)
    if message_bytes[-2:] != smtplib.bCRLF:
        message_bytes = message_bytes + smtplib.bCRLF
    message_bytes = message_bytes + b"." + smtplib.bCRLF
    socket_.sendall(message_bytes)
    socket_.makefile("rb")
    # Close
    socket_.sendall(f"quit {smtplib.CRLF}".encode(UTF8))
    socket_.close()


def demo():
    import os
    import dotenv

    dotenv.load_dotenv()
    username = os.getenv("GOOGLE_USERNAME", "")
    password = os.getenv("GOOGLE_APP_PASSWORD", "")
    host = "smtp.gmail.com"
    port = 587

    for step in [step_1, step_2, step_3, step_4, step_5, step_6, ]:
        step(host, port, username, password)


if __name__ == "__main__":
    demo()

import aiosmtplib
from email.message import EmailMessage
from config import settings
from jinja2 import Environment, FileSystemLoader


env = Environment(
  loader=FileSystemLoader("templates")
)

template = env.get_template(
  "email_reset.html"
  )


async def send_reset_email(user_email, username, token):

  message = EmailMessage()
  message["Subject"] = "RESET PASSWORD"
  message["From"] = settings.email_address
  message["To"] = user_email

  reset_link = (
      f"{settings.frontend_url}"
      f"/reset_password"
      f"?token={token}"
    )

  html_content = template.render(
    reset_link=reset_link,
    username=username
  )

  message.add_alternative(html_content, subtype="html")

  import socket

  print("HOST:", settings.email_host)
  print("PORT:", settings.email_port)

  try:
      print(socket.getaddrinfo(settings.email_host, settings.email_port))
  except Exception as e:
      print("DNS ERROR:", e)

  await aiosmtplib.send(
    message,
    hostname=settings.email_host,
    port=settings.email_port,
    username=settings.email_address,
    password=settings.email_password,
    use_tls=True
  )








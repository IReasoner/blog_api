import aiosmtplib
from email.message import EmailMessage
from config import settings
from jinja2 import Environment, FileSystemLoader
import logging

logger = logging.getLogger(__name__)


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

  logger.info("=== Starting send_reset_email ===")
  logger.info(f"HOST: {settings.email_host}")
  logger.info(f"PORT: {settings.email_port}")
  logger.info(f"EMAIL: {settings.email_address}")

  import socket

  try:
      result = socket.getaddrinfo(settings.email_host, settings.email_port)
      logger.info(f"DNS RESULT: {result}")
  except Exception:
      logger.exception("DNS lookup failed")

  # await aiosmtplib.send(
  #   message,
  #   hostname=settings.email_host,
  #   port=settings.email_port,
  #   username=settings.email_address,
  #   password=settings.email_password,
  #   use_tls=True
  # )

  smtp = aiosmtplib.SMTP(
    hostname=settings.email_host,
    port=settings.email_port,
    use_tls=True,
    timeout=30,
)

  logger.info("About to connect")

  await smtp.connect()

  logger.info("Connected!")

  await smtp.quit()

    






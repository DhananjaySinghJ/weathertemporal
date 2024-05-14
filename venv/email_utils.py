from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(sender_email, recipient_email, subject, content, sendgrid_api_key):
    """
    Sends an email using the SendGrid API.

    Args:
        sender_email (str): The email address of the sender.
        recipient_email (str): The email address of the recipient.
        subject (str): The subject of the email.
        content (str): The content of the email.
        sendgrid_api_key (str): The API key for the SendGrid service.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    # Create a Mail object with sender, recipient, subject, and content
    message = Mail(
        from_email=sender_email,
        to_emails=recipient_email,
        subject=subject,
        plain_text_content=content
    )

    try:
        # Create a SendGrid client with the provided API key
        sg = SendGridAPIClient(sendgrid_api_key)
        # Send the email
        response = sg.send(message)
        # Check if the email was sent successfully (status code 202)
        return response.status_code == 202
    except Exception as e:
        # If an error occurs during sending, print the error message
        print("Error sending email:", str(e))
        return False

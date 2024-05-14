import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

weather_api_key = os.getenv('WEATHER_API_KEY')
sendgrid_api_key = os.getenv('SENDGRID_API_KEY')

# Base URL variable to store URL
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Prompt the user to enter the city name
city_name = input("Enter city name: ")
email_id = input("Enter email id: ")

# Complete URL variable to store complete URL address
complete_url = base_url + "appid=" + weather_api_key + "&q=" + city_name

# Get method of requests module
# Return response object
response = requests.get(complete_url)

# Convert JSON format data into Python format data
data = response.json()

# Check if the city is found
if data["cod"] != "404":
    # Extract temperature in Kelvin
    temperature_kelvin = data["main"]["temp"]

    # Convert temperature from Kelvin to Celsius
    temperature_celsius = temperature_kelvin - 273.15

    # Extract other weather information
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    weather_description = data["weather"][0]["description"]

    # Prepare email content
    email_content = f"The current weather in {city_name}:\n" \
                    f"Temperature: {temperature_celsius:.2f} °C\n" \
                    f"Atmospheric Pressure: {pressure} hPa\n" \
                    f"Humidity: {humidity} %\n" \
                    f"Description: {weather_description}"

    # Create SendGrid email message
    message = Mail(
        from_email='dhananjay.singh552@gmail.com',
        to_emails=email_id,
        subject=f"Weather Update for {city_name}",
        plain_text_content=email_content
    )

    # Send email using SendGrid
    # Send email using SendGrid
    try:
        sg = SendGridAPIClient(sendgrid_api_key)  # Use sendgrid_api_key variable instead of 'SENDGRID_API_KEY'
        response = sg.send(message)
        if response.status_code == 202:
            print("Email sent successfully!")
        else:
            print("Failed to send email.")
    except Exception as e:
        print("Error sending email:", str(e))


else:
    print("City Not Found")

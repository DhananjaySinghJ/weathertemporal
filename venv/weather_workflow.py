import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import psycopg2
import logging
from temporal.workflow import workflow_method, WorkflowClient
from temporal.activity_method import activity_method

class WeatherWorkflow:
    @workflow_method
    async def execute_workflow(cls, city_name: str, email_id: str):
        # Retrieve weather data
        weather_data = await cls.get_weather(city_name)
        if weather_data.get("cod") != "404":
            # Construct email content with weather information
            email_content = cls.construct_email_content(city_name, weather_data)
            # Send email
            await cls.send_email('your_email_id', email_id, f"Weather Update for {city_name}", email_content)
            # Insert into database
            await cls.insert_into_database(email_id, city_name)
            return "Workflow completed successfully!"
        else:
            return "City Not Found"

    @activity_method
    async def get_weather(cls, city_name: str):
        # Retrieve weather data from OpenWeatherMap API
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={city_name}&appid={weather_api_key}"
        response = requests.get(complete_url)
        data = response.json()
        return data

    @activity_method
    async def send_email(cls, sender_email: str, recipient_email: str, subject: str, content: str):
        # Send email using SendGrid
        message = Mail(
            from_email=sender_email,
            to_emails=recipient_email,
            subject=subject,
            plain_text_content=content
        )
        try:
            sg = SendGridAPIClient(sendgrid_api_key)
            response = sg.send(message)
            return response.status_code == 202
        except Exception as e:
            logging.error("Error sending email:", str(e))
            return False

    @activity_method
    async def insert_into_database(cls, email: str, city: str):
        # Insert user details into database
        conn = psycopg2.connect(db_string)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, city) VALUES (%s, %s)", (email, city))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def construct_email_content(city_name: str, weather_data: dict):
        # Construct email content with weather information
        temperature_celsius = weather_data["main"]["temp"] - 273.15
        pressure = weather_data["main"]["pressure"]
        humidity = weather_data["main"]["humidity"]
        weather_description = weather_data["weather"][0]["description"]
        email_content = f"The current weather in {city_name}:\n" \
                        f"Temperature: {temperature_celsius:.2f} °C\n" \
                        f"Atmospheric Pressure: {pressure} hPa\n" \
                        f"Humidity: {humidity} %\n" \
                        f"Description: {weather_description}"
        return email_content

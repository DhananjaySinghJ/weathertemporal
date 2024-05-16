import httpx
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import psycopg2
import logging
from temporalio.activity import activity_method
from temporalio.workflow import workflow_method, Workflow


class WeatherWorkflowImpl:
    @staticmethod
    @activity_method
    async def get_weather(city_name: str):
        try:
            # Retrieve weather data from OpenWeatherMap API
            weather_api_key = os.environ.get("WEATHER_API_KEY")
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            async with httpx.AsyncClient() as client:
                response = await client.get(base_url, params={"q": city_name, "appid": weather_api_key})
                response.raise_for_status()  # Raise an exception for non-200 status codes
                data = response.json()
                return data
        except Exception as e:
            logging.error(f"Error retrieving weather data: {str(e)}")
            return None

    @staticmethod
    @activity_method
    async def send_email(sender_email: str, recipient_email: str, subject: str, content: str):
        try:
            # Send email using SendGrid
            sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
            message = Mail(
                from_email=sender_email,
                to_emails=recipient_email,
                subject=subject,
                plain_text_content=content
            )
            sg = SendGridAPIClient(sendgrid_api_key)
            response = await sg.send(message)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            return True
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            return False

    @staticmethod
    @activity_method
    async def insert_into_database(email: str, city: str):
        try:
            # Insert user details into database
            db_string = os.environ.get("DB_CONNECTION_STRING")
            conn = psycopg2.connect(db_string)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (email, city) VALUES (%s, %s)", (email, city))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            logging.error(f"Error inserting into database: {str(e)}")
            return False


class WeatherWorkflow(Workflow):
    @staticmethod
    @workflow_method
    async def execute_workflow(city_name: str, email_id: str):
        try:
            # Retrieve weather data
            weather_data = await WeatherWorkflowImpl.get_weather(city_name)
            if weather_data and weather_data.get("cod") != "404":
                # Construct email content with weather information
                email_content = WeatherWorkflow.construct_email_content(city_name, weather_data)
                # Send email
                email_sent = await WeatherWorkflowImpl.send_email('your_email_id', email_id, f"Weather Update for {city_name}", email_content)
                # Insert into database if email was sent successfully
                if email_sent:
                    await WeatherWorkflowImpl.insert_into_database(email_id, city_name)
                    return "Workflow completed successfully!"
                else:
                    return "Failed to send email"
            else:
                return "City Not Found"
        except Exception as e:
            logging.error(f"Error executing workflow: {str(e)}")
            return "Error executing workflow"

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

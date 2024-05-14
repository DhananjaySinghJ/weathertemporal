from dotenv import load_dotenv
import os
import weather
import email_utils
import database

def main():
    # Load environment variables from .env file
    load_dotenv()
    # Retrieve API keys and database connection string from environment variables
    weather_api_key = os.getenv('WEATHER_API_KEY')
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    db_string = os.getenv('DB_CONNECTION_STRING')

    # Prompt user to enter city name and email address
    city_name = input("Enter city name: ")
    email_id = input("Enter email id: ")

    # Get weather data for the specified city using the OpenWeatherMap API
    weather_data = weather.get_weather(city_name, weather_api_key)
    
    # Check if the city is found
    if weather_data.get("cod") != "404":
        # Extract weather information from the response data
        temperature_celsius = weather_data["main"]["temp"] - 273.15
        pressure = weather_data["main"]["pressure"]
        humidity = weather_data["main"]["humidity"]
        weather_description = weather_data["weather"][0]["description"]

        # Construct email content with weather information
        email_content = f"The current weather in {city_name}:\n" \
                        f"Temperature: {temperature_celsius:.2f} °C\n" \
                        f"Atmospheric Pressure: {pressure} hPa\n" \
                        f"Humidity: {humidity} %\n" \
                        f"Description: {weather_description}"

        # Send the weather update email using SendGrid
        if email_utils.send_email('your_email_id', email_id, f"Weather Update for {city_name}", email_content, sendgrid_api_key):
            # If email is sent successfully, insert user details into the database
            print("Email sent successfully!")
            database.insert_into_database(email_id, city_name, db_string)
        else:
            print("Failed to send email.")
    else:
        print("City Not Found")

if __name__ == "__main__":
    main()

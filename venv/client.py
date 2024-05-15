import os
from temporal.workflow import WorkflowClient

# Import workflow class
from weather_workflow import WeatherWorkflow

# Set environment variables
os.environ["TEMPORAL_HOST_PORT"] = "localhost:7233"
os.environ["WEATHER_API_KEY"] = "your_weather_api_key"
os.environ["SENDGRID_API_KEY"] = "your_sendgrid_api_key"
os.environ["DB_CONNECTION_STRING"] = "your_database_connection_string"

def main():
    # Create a Temporal client
    client = WorkflowClient.new_client(namespace="default")
    # Create a workflow stub
    workflow = client.new_workflow_stub(WeatherWorkflow)
    # Prompt user for city name and email ID
    city_name = input("Enter city name: ")
    email_id = input("Enter email id: ")
    # Execute the workflow
    result = workflow.execute_workflow(city_name, email_id)
    print(result)

if __name__ == "__main__":
    main()

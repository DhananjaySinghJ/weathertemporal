import os
from temporalio.workerfactory import WorkerFactory
from weather_workflow import WeatherWorkflow, WeatherWorkflowImpl


def register_workflow(worker_factory):
    # Register the WeatherWorkflow class as a workflow
    worker_factory.register_workflow_implementation(WeatherWorkflow)


def register_activities(worker_factory):
    # Register the WeatherWorkflowImpl class as activities implementation
    worker_factory.register_activities_implementation(WeatherWorkflowImpl)


def main():
    # Set environment variables
    os.environ["TEMPORAL_HOST_PORT"] = "localhost:7233"
    os.environ["WEATHER_API_KEY"] = "your_weather_api_key"
    os.environ["SENDGRID_API_KEY"] = "your_sendgrid_api_key"
    os.environ["DB_CONNECTION_STRING"] = "your_database_connection_string"

    # Create a Temporal client
    client = WorkerFactory.new_client()
    factory = WorkerFactory(client)
    # Register the workflow and activities
    register_workflow(factory)
    register_activities(factory)
    # Create and run the worker
    worker = factory.new_worker()
    worker.run()


if __name__ == "__main__":
    main()

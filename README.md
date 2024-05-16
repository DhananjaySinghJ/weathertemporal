# Weather Temporal Project

Welcome to the Weather Project! This project aims to fetch weather data from a public API, store it in a PostgreSQL database, and send weather updates to specified users via email. It utilizes Temporal for workflow orchestration to manage the execution of tasks asynchronously.

## Introduction

Weather information is vital for various industries and individuals, from agriculture to transportation, event planning to daily routines. The Weather Project provides a seamless solution for fetching real-time weather data, storing it for future reference, and delivering updates directly to users' inboxes.

### Key Features

- **Weather Data Retrieval**: Fetches weather information from a public API based on user-specified locations.
- **Database Storage**: Stores weather data in a PostgreSQL database for historical tracking and analysis.
- **Email Notifications**: Sends weather updates to specified users via email, providing timely information on current conditions.
- **Asynchronous Workflow**: Utilizes Temporal for workflow orchestration, allowing for efficient and scalable execution of weather-related tasks.

## Installation

1. Clone the repository:
2. Navigate to the project directory:
3. Create a virtual environment:
4. Activate the virtual environment:
5. Install dependencies:
6. Install and configure PostgreSQL:
- Install PostgreSQL using your package manager (e.g., Homebrew on macOS).
- Create a new PostgreSQL database and user:

## Configuration

1. Create a .env file for:
- API keys for the weather API and SendGrid
- PostgreSQL database connection details
- Temporal host port

## Usage

1. Start the PostgreSQL server:
Note: Replace `brew` with the appropriate package manager command if you're not using Homebrew.

2. Execute the main Python script to run the weather workflow:


## Project Structure

- `venv/`: Virtual environment directory
- `workflows/`: Directory containing Temporal workflow and activity implementations
- `weatherdatabase.py`: Python script for database operations
- `weather_email.py`: Python script for sending weather emails
- `config.py`: Configuration file for API keys, email settings, etc.
- `README.md`: Project documentation (you're reading it!)
  
## TO RUN THE PROJECT WITHOUT TEMPORAL JUST RUN MAIN.py

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Create a new pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.





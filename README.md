# 🤹‍♂️Fellas: BC Weather Station Dashboard

## Project Overview

This web-based application offers a  solution for accessing daily and historical weather data from over 200 automated weather stations across British Columbia. Our goal is to provide a user-friendly experience with a feature-rich dashboard useful to both common users and administrators.

## Project Description

### High-Level Overview

The BC Weather Station Dashboard provides a comprehensive web-based application for users to access daily and historical weather data from the BC Wildfire Service's automated weather stations. The dashboard features an intuitive interface, data visualizations, and customizable user preferences.

### Key Features

1. **Data Visualizations:** Explore real-time and historical weather data through interactive visualizations.
2. **Data Filtering:** Customize your data view by filtering based on day, month, year, or season.
3. **Weather Station Exploration:** Utilize the map widget to discover the locations of BC wildfire weather stations.
4. **Alert System:** Receive alerts for extreme weather events based on researched criteria.
5. **Secure Login/Registration:** Create an account to personalize your experience and set up alerts.

## Functional Requirements

### Providing Feedback

Users can submit feedback, which will be reviewed and addressed by the admin team.

### Viewing Data Visualizations

Explore a variety of visualizations, including temperature, humidity, precipitation, wind speed, and wind direction.

### Filtering Data

Customize your data view by applying filters based on day, month, year, or season.

### Viewing Weather Stations

Use the map widget to visualize the locations of BC wildfire weather stations and access detailed weather information.

### Receiving/Set Alerts

Users can receive global alerts for extreme weather conditions, while admins can configure and manage alerts.

### Login/Registration System

A secure system allowing users to create accounts, personalize preferences, and set up alerts.

### Uploading Data

Admins can perform bulk data uploads from BC weather stations, ensuring data accuracy and completeness.

### Database Management

Efficiently store, retrieve, update, and delete user and product data in the system's database.

## Use Cases

![Use Case Diagram](Project_Use_Case_Diagram.pdf)

Explore various use cases such as user feedback submission, data visualization viewing, data filtering, weather station exploration, receiving alerts, and admin functionalities like data uploads and alert configurations.

## User Stories

### Wildfire Weather Station Dashboard User Stories

1. **Firefighter - Account Creation**
   - As a firefighter, I want to create an account to access personalized data.

2. **Firefighter - Real-time and Historical Data**
   - As a firefighter, I want to see real-time and historical weather data from nearby stations to assess wildfire risk.

3. **BC Citizen - Stay Informed**
   - As a citizen, I want to stay informed about current wildfire risks near me and learn about the weather around me to stay informed.

4. **Insurance Company - Historical Data Analysis**
   - As an insurance company, we want to analyze historical weather data to identify areas in BC that are at risk for extreme events like wildfires.

5. **Admin - Platform Management**
   - As an administrator, I want to manage users, configure alerts, customize visualizations, and analyze data to ensure the platform functions effectively and securely.


## Cloning and Setup Instructions

### Clone the Repository

1. Open a terminal or command prompt.

2. Navigate to the directory where you want to clone the project:

    ```bash
    cd path/to/your/directory
    ```

3. Clone the repository:

    ```bash
    git clone https://github.com/carsondrobe/Fellas.git
    ```

### Set up Virtual Environment

1. Change into the project directory:

    ```bash
    cd Fellas
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On Unix or MacOS:

        ```bash
        source venv/bin/activate
        ```

### Install Dependencies

1. Ensure that your virtual environment is activated.

2. Install project dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

### Apply Database Migrations

1. Run Django migrations to apply the database schema:

    ```bash
    python manage.py migrate
    ```

### Run the Development Server

1. Start the Django development server:
    ```bash
    cd Site/bc_weather_station_dashboard 
    ```

    ```bash
    python manage.py runserver
    ```

   The development server should be accessible at `http://127.0.0.1:8000/` by default.

2. Open a web browser and navigate to the provided URL to see the application.



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



# To run the application, you would use: uvicorn Simulator:app --host 0.0.0.0 --port 8080 --reload

# FastAPI and Web Development
from fastapi import FastAPI, HTTPException #  For building the web application, For handling HTTP exceptions
# Database Connectivity
import psycopg2 # PostgreSQL database adapter for Python
from urllib.parse import urlparse # For parsing database connection URLs
# Email Sending
from App import sendmail # Importing the sendmail function from the App module (not a standard library)
# Scheduling and Threading
import schedule # For scheduling tasks
import time # For working with time and sleep functions
import threading # For running tasks in separate threads
# Miscellaneous
from datetime import datetime # For working with dates and times
import logging # For logging events and errors
import os # For interacting with the operating system
import random # For generating random numbers


# Set up logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Database connection function
def get_db_connection():
    
    try:
        # Your connection URL
        DATABASE_URL = os.getenv('DATABASE_URL')

        # Parse the URL
        result = urlparse(DATABASE_URL)

        # Extract the components
        username = result.username
        password = result.password
        database = result.path[1:]  # remove the leading '/'
        hostname = result.hostname
        port = result.port

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
        
        return conn
    except psycopg2.OperationalError as e:
        logging.info(f"Error: {e}")

# Initialize energy produced to 0: For first runs
energy_produced = 0

def simulate():
    """
    The simulate() function simulates the energy usage of various appliances in a home, updates their conditions, and sends email notifications when necessary.
    Parameters:
        None
    Returns:
        None
    Functionality:
        1. Retrieves all appliances from the database.
        2. Loops through each appliance and:
            - Checks if the current temperature falls outside the threshold range.
            - Updates the appliance condition if necessary.
            - Sends an email notification if the condition changes.
            - Generates random energy consumed and current output values based on the appliance type.
            - Calculates the energy produced. (Not Needed)
            - Inserts a new observation into the energy usage table.
        3. Commits the changes and closes the database connection.
    Appliance Conditions:
        If the appliance is on:
            - Freezer: Energy consumed between 0.6 and 0.8 kWh, current output increases by 2.0-4.7°C.
            - Refrigerator: Energy consumed between 0.02 and 0.04 kWh, current output increases by 5.0-6.0°C.
            - Air Conditioner: Energy consumed between 0.0007 and 0.001 kWh, current output increases by 4.0-5.7°C.
        If the appliance is off:
            - Freezer: Energy consumed is 0 kWh, current output decreases by 2.0-4.7°C.
            - Refrigerator: Energy consumed is 0 kWh, current output decreases by 5.0-6.0°C.
            - Air Conditioner: Energy consumed is 0 kWh, current output decreases by 4.0-5.7°C.
    Email Notifications:
        Sent when an appliance's condition changes.
        Contains the appliance name, old condition, and new condition.
    Database Interactions:
        Retrieves appliances from the Appliances table.
        Updates the ApplianceCondition column in the Appliances table.
        Inserts new observations into the EnergyUsage table.
    Notes:
        The energy_produced variable is a global variable that accumulates the energy produced by all appliances.
            But this is flawed since we are not actually dealing with energy producing appliances
        The sendmail() function is used to send email notifications.
        The get_db_connection() function is used to establish a database connection
    """
    
    global energy_produced # Access the global energy_produced variable
    
    # Establish a connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve all appliances from the database
    cursor.execute('''
        SELECT Appliances.ApplianceID, Appliances.HomeID, Appliances.ApplianceName, Appliances.ApplianceCondition, 
            Appliances.StartValue, Appliances.StopValue, Homes.Email
        FROM Appliances
        JOIN Homes ON Appliances.HomeID = Homes.HomeID
    ''')
    appliances = cursor.fetchall() # Fetch all the rows from the query result

    # Loop through each appliance
    for appliance in appliances:
        # Unpack the appliance data
        appliance_id, home_id, appliance_name, appliance_condition, start_value, stop_value, email = appliance
        
        # Convert the appliance condition from string to boolean
        str_to_bool = {"True": True, "False": False}
        appliance_condition = str_to_bool.get(appliance_condition, False)

        # Get the last observation from the energy usage table
        cursor.execute(f'''
            SELECT *
            FROM EnergyUsage
            WHERE HomeID = {home_id} AND ApplianceID = {appliance_id}
            ORDER BY DateTime DESC
            LIMIT 1;
        ''')
        last_observation = cursor.fetchone()
        try:
            # Get the current temperature from the last observation
            current_temperature = last_observation['CurrentOutput']
        except TypeError:
            # If the appliance is new, set the current temperature to 0.0
            current_temperature = 0.0

        # ==== Auto On/Off ======
        # Check if the current temperature falls outside the threshold range
        if (current_temperature < stop_value and not appliance_condition) or (current_temperature > start_value and appliance_condition):
            # Update the appliance condition
            new_condition = not appliance_condition
            
            # Update the appliance condition in the database
            cursor.execute(f'''
                UPDATE Appliances
                SET ApplianceCondition = '{str(new_condition)}'
                WHERE HomeID = {home_id} AND ApplianceID = {appliance_id}
            ''')

            # Define a function to convert the condition to a string
            def condition_to_string(condition):
                return "ON" if condition else "OFF"
            
            # Get the old and new conditions as strings
            old = condition_to_string(appliance_condition)
            new = condition_to_string(new_condition)

            # Send an email notification
            sendmail(type="appliance condition",mail=email,appliance_name=appliance_name,old_condition=old, new_condition=new)
        
        # If the appliance is on
        if appliance_condition:
            # Generate random energy consumed and current output values based on the appliance type
            if appliance_id == 1:  # Freezer
                energy_consumed = random.uniform(0.6, 0.8)
                current_output = current_temperature + random.uniform(2.0, 4.7)
            elif appliance_id == 2:  # Refrigerator
                energy_consumed = random.uniform(0.02, 0.04)
                current_output = current_temperature + random.uniform(5.0, 6.0)
            elif appliance_id == 3:  # Air Conditioner
                energy_consumed = random.uniform(0.0007, 0.001)
                current_output = current_temperature + random.uniform(4.0, 5.7)

        # If the appliance is off
        else:
            # Generate random energy consumed and current output values based on the appliance type
            if appliance_id == 1:  # Freezer
                energy_consumed = random.uniform(0, 0)
                current_output = current_temperature - random.uniform(2.0, 4.7)
            elif appliance_id == 2:  # Refrigerator
                energy_consumed = random.uniform(0, 0)
                current_output = current_temperature - random.uniform(5.0, 6.0)
            elif appliance_id == 3:  # Air Conditioner
                energy_consumed = random.uniform(0, 0)
                current_output = current_temperature - random.uniform(4.0, 5.7)

        # Calculate the energy produced
        energy_produced += energy_consumed
        # Get the current date and time
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Insert a new observation into the energy usage table
        cursor.execute(f'''
            INSERT INTO EnergyUsage (HomeID, ApplianceID, DateTime, EnergyConsumed, EnergyProduced, CurrentOutput)
            VALUES ({home_id}, {appliance_id}, '{now}', {energy_consumed}, {energy_produced}, {current_output});
        ''')
    
    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

def run_scheduler():
    """
    Runs the scheduler to execute tasks at specified intervals.

    In this case, the simulate function is scheduled to run every hour.
    """
    schedule.every(1).hours.do(simulate) # Schedule the simulate function to run every hour
    # Infinite loop to continuously check for pending tasks
    while True:
        # Run any pending tasks (functions scheduled to run at their designated time)
        schedule.run_pending()
        # Sleep for 1 second to avoid consuming excessive CPU resources
        time.sleep(1)

# Start the scheduler in a background thread
threading.Thread(target=run_scheduler, daemon=True).start()

@app.get("/simulate")
def simulate_endpoint():
    """
    Simulate endpoint to trigger the simulation.

    Returns a success message if the simulation runs successfully, 
    otherwise raises an HTTPException with a 500 status code and the error message.
    """
    try:
        # Call the simulate function to run the simulation
        simulate()
        # Return a success message
        return {"message": "Simulation ran successfully"}
    except Exception as e:
        # Catch any exceptions raised during the simulation
        # Raise an HTTPException with a 500 status code and the error message
        raise HTTPException(status_code=500, detail=str(e))
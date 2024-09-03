# To run the application, you would use: uvicorn Simulator:app --host 0.0.0.0 --port 8080 --reload

from fastapi import FastAPI, HTTPException
import psycopg2
import os
from urllib.parse import urlparse
import random
from datetime import datetime
import schedule
import time
import threading
import logging

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
        logging.info("DB connected")
        return conn
    except psycopg2.OperationalError as e:
        logging.info(f"Error: {e}")

# Initialize energy produced to 0: For first runs
energy_produced = 0

def simulate():
    global energy_produced
    conn = get_db_connection()
    cursor = conn.cursor()

    logging.info("Running simulate function")
    # Get all appliances
    cursor.execute('''
        SELECT ApplianceID, HomeID, ApplianceCondition, StartValue, StopValue
        FROM Appliances
    ''')
    appliances = cursor.fetchall()

    logging.info(f"Fetched {len(appliances)} appliances")

    # Loop through each appliance
    for appliance in appliances:
        appliance_id, home_id, appliance_condition, start_value, stop_value = appliance

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
            current_temperature = last_observation['CurrentOutput']
        except TypeError:
            current_temperature = 0.0 # If the appliance is new

        # ==== Auto On/Off ======
        # Check if the current temperature falls outside the threshold range
        if (current_temperature < stop_value and not appliance_condition) or (current_temperature > start_value and appliance_condition):
            # Update the appliance condition
            new_condition = not appliance_condition
            
            cursor.execute(f'''
                UPDATE Appliances
                SET ApplianceCondition = {str(new_condition)}
                WHERE HomeID = {home_id} AND ApplianceID = {appliance_id}
            ''')
        
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

        # Insert a new observation into the energy usage table
        cursor.execute(f'''
            INSERT INTO EnergyUsage (HomeID, ApplianceID, DateTime, EnergyConsumed, EnergyProduced, CurrentOutput)
            VALUES ({home_id}, {appliance_id}, {datetime.now()}, {energy_consumed}, {energy_produced}, {current_output});
        ''')
        logging.info(f"Inserted new observation for ApplianceID {appliance_id} in HomeID {home_id}")

    conn.commit()
    conn.close()
    logging.info("Simulation completed and database updated.")

def run_scheduler():
    schedule.every(1).minutes.do(simulate)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler in a background thread
threading.Thread(target=run_scheduler, daemon=True).start()

@app.get("/simulate")
def simulate_endpoint():
    try:
        simulate()
        return {"message": "Simulation ran successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
import requests
from uagents import Agent, Context, Bureau, Model

class TemperatureAlert(Model):
    location: str
    min_temperature: float
    max_temperature: float
    
WEATHER_API_KEY = 'b522b5ef009540ff2b942076593fb43f'  
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=b522b5ef009540ff2b942076593fb43f'

# Create a function to check temperature and send alerts
async def check_temperature(ctx: Context, alert):
    location = alert['location']  # Use square brackets to access the 'location' key
    params = {
        'q': location,
        'appid': WEATHER_API_KEY,
        'units': 'metric'  # Use Celsius for temperature
    }

    try:
        response = requests.get(WEATHER_API_URL, params=params)
        data = response.json()
        current_temperature = data['main']['temp']

        if current_temperature < alert['min_temperature']:
            ctx.logger.info(f"Alert: Temperature in {location} is below {alert['min_temperature']}°C.")
        elif current_temperature > alert['max_temperature']:
            ctx.logger.info(f"Alert: Temperature in {location} is above {alert['max_temperature']}°C.")
    except Exception as e:
        ctx.logger.error(f"Error fetching weather data for {location}: {e}")

# Create the agent
temperature_agent = Agent(name="TemperatureAlertAgent",endpoint=['http://api.openweathermap.org/'])

# Define temperature alerts as a list of dictionaries
temperature_alerts = [
    {"location": "london", "min_temperature": 15.0, "max_temperature": 25.0},
    {"location": "ghaziabad", "min_temperature": 0.00, "max_temperature": 3.00},
    # Add more locations and temperature thresholds as needed
]
# Schedule the temperature check function for each alert at regular intervals (e.g., every 30 minutes)
for alert in temperature_alerts:#make it t
    @temperature_agent.on_interval(period=2)  # 1800 seconds = 30 minutes
    async def schedule_temperature_check(ctx: Context, alert=alert):
        await check_temperature(ctx, alert)

# Create a Bureau and add the agent to it
# bureau = Bureau()
# bureau.add(temperature_agent)

# if __name__ == "__main__":
#     bureau.run()
#if the 
temperature_agent.run()
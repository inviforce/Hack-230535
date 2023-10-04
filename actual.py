import requests
from uagents import Agent, Context, Bureau, Model
from uagents.setup import fund_agent_if_low
city_name=input("enter the city name= ")
min_temp=int(input("enter the min temp= "))
max_temp=int(input("enter the max temp= "))
#defines a TemperatureAlert class as a model. 
#It represents the data structure for temperature alerts, specifying attributes like location, min_temperature, and max_temperature. 
#This class will be used to store temperature alert information.
class TemperatureAlert(Model):
    location: str
    min_temperature: float
    max_temperature: float
WEATHER_API_KEY = 'b522b5ef009540ff2b942076593fb43f'  
WEATHER_API_URL = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}'
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
        print(city_name,"current temprature is = ",current_temperature)
        if current_temperature < alert['min_temperature']:
            ctx.logger.info(f"Alert: Temperature in {location} is below {alert['min_temperature']}°C.")
        elif current_temperature > alert['max_temperature']:
            ctx.logger.info(f"Alert: Temperature in {location} is above {alert['max_temperature']}°C.")
    except Exception as e:
        ctx.logger.error(f"Error fetching weather data for {location}: {e}")

# Create the agent
temperature_agent = Agent(name="TemperatureAlertAgent",endpoint=['https://api.openweathermap.org'])
fund_agent_if_low(temperature_agent.wallet.address())
# Define temperature alerts as a list of dictionaries
temperature_alerts = [
    {"location": city_name, "min_temperature": min_temp, "max_temperature": max_temp},
    
    # Add more locations and temperature thresholds as needed
]
# Schedule the temperature check function for each alert at regular intervals (e.g., every 30 minutes)
for alert in temperature_alerts:
    @temperature_agent.on_interval(period=2)  # 1800 seconds = 30 minutes
    async def schedule_temperature_check(ctx: Context, alert=alert):
        await check_temperature(ctx, alert)

#Create a Bureau and add the agent to it
bureau = Bureau()
bureau.add(temperature_agent)

if __name__== "__main__":    
    bureau.run()

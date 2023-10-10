import requests
import os
import storage
from colorama import Fore
from dotenv import load_dotenv
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
#-------FIRST STEP IS TO GET INFORMATION FROM CLIENT----------
city_name=storage.Location
min_temp=float(storage.min_temp)
max_temp=float(storage.max_temp)
#-------SECOND STEP IS TO GET INFORMATION FROM OPEN WEATHER API--------
load_dotenv()
weather_api_key=os.getenv('weather_api_key')
weather_api=f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_api_key}'
params={"units":"metric"}
#-------------CHECKING FOR THE CORRECT TEMPERATURE RANGE------------
async def alert_temperature(ctx:Context,alert):
    try:
        response_api=requests.get(weather_api,params=params)
        content = response_api.json()
        if content["main"]["temp"]>alert['max_temperature']: #------CHECKING FOR MAXIMUM TEMPERATURE---------
            ctx.logger.info(Fore.RED+f"Alert: Temperature in {alert['location']} is above {alert['max_temperature']}")
        elif content["main"]["temp"]<alert['min_temperature']:#-------CHECKING FOR MINIMUM TEMPERATURE--------
            ctx.logger.info(Fore.RED+f"Alert: Temperature in  {alert['location']} is below {alert['min_temperature']}")
    except Exception:#--------IN CASE OF SOME ERROR IN EXTRACTING INFORMATION----------
        ctx.logger.info(Fore.MAGENTA+f"Error fetching data for {alert['location']},check the spelling or the given city doesn't exist in our data base")
#----------CREATING AN AGENT------------
temp_alert=Agent(name="Temperature_Alert_Agent",seed="Alert recovery phase",endpoint=['https://api.openweathermap.org'])
fund_agent_if_low(temp_alert.wallet.address())
temperature_alerts = [
    {"location": city_name, "min_temperature": min_temp, "max_temperature": max_temp}]
for alert in temperature_alerts:
    @temp_alert.on_interval(period=1800)  #-------1800 seconds = 30 minutes-------
    async def schedule_temperature_check(ctx: Context, alert=alert):
        await alert_temperature(ctx, alert)
temp_alert.run()#-------RUNNNING AGENT-------
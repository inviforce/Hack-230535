import requests
from uagents import Agent, Context, Bureau, Model
from uagents.setup import fund_agent_if_low
#first step is to get information from the client
city_name=input("Enter city name: ")
min_temp=int(input("Enter the minimum temperature in degree Celsius: "))
max_temp=int(input("Enter the maximum temperature in degree Celsius: "))
#second step is to acess information from the api
weather_api_key='b522b5ef009540ff2b942076593fb43f'
weather_api=f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_api_key}'
params={"units":"metric"}
response_api=requests.get(weather_api,params=params)
async def alert_temperature(ctx:Context,alert):
    try:
        # Access the content of the response and check for the condition of temperature
        content = response_api.json()
        if content["main"]["temp"]>max_temp:
            ctx.logger.info(f"Alert:Temperature in city {city_name} is exceeding maximum temperature, Current temperature is {content['main']['temp']}")
        elif content["main"]["temp"]<min_temp:
            ctx.logger.info(f"Alert:Temperature in city {city_name} is below minimum temperature, Current temperature is {content['main']['temp']}")
    except Exception as e:
        ctx.logger.info(f"Error fetching data for{city_name},check the spelling or the given city doesn't exist in our data base")
#to create an agent
temp_alert=Agent(name="Alert",seed="Alert recovery phase",endpoint=['https://api.openweathermap.org'])
fund_agent_if_low(temp_alert.wallet.address())
temperature_alerts = [
    {"location": city_name, "min_temperature": min_temp, "max_temperature": max_temp},
    
]
for alert in temperature_alerts:
    @temp_alert.on_interval(period=2)  # 1800 seconds = 30 minutes
    async def schedule_temperature_check(ctx: Context, alert=alert):
        await alert_temperature(ctx, alert)
temp_alert.run()
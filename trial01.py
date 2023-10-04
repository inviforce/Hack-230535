import requests
city_name=input()


params = { 
        'units': 'metric'}

# Send a GET request to a URL
response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q=London&appid=b522b5ef009540ff2b942076593fb43f",params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Access the content of the response
    content = response.json()
    
    print(content['main']['temp'])
    
else:
    print("Request failed with status code:", response.status_code)
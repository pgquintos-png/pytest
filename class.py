import requests

response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=35.6764&lon=139.6500&appid=1e76a73bdf58b1ef4826d87695cd27b4")

print(response.json())
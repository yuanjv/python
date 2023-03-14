#!/bin/python3
from datetime import date
import json
import requests
import os
from chatgpt_wrapper import ChatGPT

current_time=os.popen("date").read().strip('\n')

def getDict(link:str)->dict:
    return json.loads(requests.get(link).text)

#get location from ip
ip_info=getDict("http://ip-api.com/json")
lat=ip_info["lat"]
lon=ip_info["lon"]

#NWS uses weather grids to identify the weather in a specific location
#get current weather grid info
weather_grid_info=getDict(f"https://api.weather.gov/points/{lat},{lon}")

#get the current weather data as a python dict
forecast=getDict(weather_grid_info["properties"]["forecast"])["properties"]

#construct the chatgpt prompt
prompt=f'''
Today is {current_time}. Please make an oral weather report based on the data on the following json:
{json.dumps(forecast)}
'''

#loop to make sure chatgpt doesnt return a json
bot=ChatGPT()
ans='{"'
while ans!=ans.replace('{"',''):
    ans=bot.ask(prompt)
    #translate units
    ans=bot.ask("Please rewrite the weather report by changing all F and mph data to Celsius and meters per second accordingly.")
    bot.delete_conversation()
    ans=ans.split('\n')
    del ans[0]
    ans='\n'.join(ans)

print(ans)

os._exit(0)

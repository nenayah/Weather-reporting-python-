# Code to perform web scraping for weather data of current region
# using requests-html library
from bs4 import *
from requests_html import HTMLSession
import requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"


# Function that given a URL by extracting all useful weather information and return it in a dictionary
def get_weather_data(url):
    session = HTMLSession()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE

    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Getting current region, weather, temperature, and actual day and hour.
    # store all results on this dictionary
    result = {}
    result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
    # extract temperature now
    result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
    # get the day and hour now
    result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
    # get the actual weather
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text

    # get the precipitation
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    # get the % of humidity
    result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
    # extract the wind
    result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text

    # get next few days' weather
    next_days = []
    days = soup.find("div", attrs={"id": "wob_dp"})
    for day in days.findAll("div", attrs={"class": "wob_df"}):
        # extract the name of the day
        day_name = day.findAll("div")[0].attrs['aria-label']
        # get weather status for that day
        weather = day.find("img").attrs["alt"]
        temp = day.findAll("span", {"class": "wob_t"})
        # maximum temparature in Celsius, use temp[1].text if you want fahrenheit
        max_temp = temp[0].text
        # minimum temparature in Celsius, use temp[3].text if you want fahrenheit
        min_temp = temp[2].text
        next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})

    # append to result
    result['next_days'] = next_days
    return result


# finish up the script by parsing command-line arguments
if __name__ == "__main__":
    URL = "https://www.google.com/search?q=weather&sxsrf=AOaemvKHG3CukxUHhL7rjD8MTxxnyKGr7g%3A1634891839837&ei=P3hyYYfFMoq5gweSya-4DA&ved=0ahUKEwjH4O_azt3zAhWK3OAKHZLkC8cQ4dUDCA4&uact=5&oq=weather&gs_lcp=Cgdnd3Mtd2l6EANKBAhBGABQ-ugZWProGWCN6xloAHACeACAAQCIAQCSAQCYAQCgAQHAAQE&sclient=gws-wiz"

    #To check for internet connection
    timeout = 5
    try:
        request = requests.get(URL, timeout=timeout)
        Internet = True
        print("Connected to the Internet")
    except (requests.ConnectionError, requests.Timeout) as exception:
        Internet = False
        print("No internet connection.")

    #To retrieve weather data
    import argparse

    parser = argparse.ArgumentParser(description="Quick Script for Extracting Weather data using Google Weather")
    parser.add_argument("region", nargs="?", help="""Region to get weather for, must be available region.
                                        Default is your current location determined by your IP Address""", default="")
    # parse arguments
    args = parser.parse_args()
    region = args.region
    URL += region
    # get data
    data = get_weather_data(URL)

    if Internet is True:
        print("Weather for:", data["region"])
        print("Now:", data["dayhour"])
        print(f"Temperature now: {data['temp_now']}°C")
        print("Description:", data['weather_now'])
        print("Precipitation:", data["precipitation"])
        print("Humidity:", data["humidity"])
        print("Wind:", data["wind"])

        print(" ")
        print("Each day for the next week:")

        if "Monday" in data["dayhour"]:
            i = 0
        elif "Tuesday" in data["dayhour"]:
            i = 1
        elif "Wednesday" in data["dayhour"]:
            i = 2
        elif "Thursday" in data["dayhour"]:
            i = 3
        elif "Friday" in data["dayhour"]:
            i = 4
        elif "Saturday" in data["dayhour"]:
            i = 5
        elif "Sunday" in data["dayhour"]:
            i = 6

        week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        safe = i
        while i < 7:
            next_url = "https://www.google.com/search?q=" + week[i] + "+weather&sxsrf=AOaemvKHG3CukxUHhL7rjD8MTxxnyKGr7g%3A1634891839837&ei=P3hyYYfFMoq5gweSya-4DA&ved=0ahUKEwjH4O_azt3zAhWK3OAKHZLkC8cQ4dUDCA4&uact=5&oq=weather&gs_lcp=Cgdnd3Mtd2l6EANKBAhBGABQ-ugZWProGWCN6xloAHACeACAAQCIAQCSAQCYAQCgAQHAAQE&sclient=gws-wiz"
            next_data = get_weather_data(next_url)
            weather_next_dict = {
                "region": next_data["region"],
                "day_hour": next_data["dayhour"],
                "weather_description": next_data['weather_now'],
                "precipitation": next_data["precipitation"],
                "humidity": next_data["humidity"],
                "wind": next_data["wind"]
            }
            print(weather_next_dict)
            i += 1
        i = 0
        while i < safe:
            next_url = "https://www.google.com/search?q=" + week[i] + "+weather&sxsrf=AOaemvKHG3CukxUHhL7rjD8MTxxnyKGr7g%3A1634891839837&ei=P3hyYYfFMoq5gweSya-4DA&ved=0ahUKEwjH4O_azt3zAhWK3OAKHZLkC8cQ4dUDCA4&uact=5&oq=weather&gs_lcp=Cgdnd3Mtd2l6EANKBAhBGABQ-ugZWProGWCN6xloAHACeACAAQCIAQCSAQCYAQCgAQHAAQE&sclient=gws-wiz"
            next_data = get_weather_data(next_url)
            weather_next_dict = {
                "region": next_data["region"],
                "day_hour": next_data["dayhour"],
                "weather_description": next_data['weather_now'],
                "precipitation": next_data["precipitation"],
                "humidity": next_data["humidity"],
                "wind": next_data["wind"]
            }
            print(weather_next_dict)
            i += 1

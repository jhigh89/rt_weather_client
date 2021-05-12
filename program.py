import collections
import config
import requests

Location = collections.namedtuple('Location', 'city state country')
Weather = collections.namedtuple('Weather', 'location units temp condition')

def main():
    show_header()

    # Get the location request
    location_text = input("Which city's weather would you like to check? (e.g. San Francisco, CA, US) \n")
    print(f"You selected {location_text}")
    
    Loc = convert_plaintext_location(location_text)
    if not Loc:
        print(f"Could not find any info about {location_text}.")
        return
    
    # Get report from the API
    data = call_weather_api(Loc)
    if not data:
        print(f"Could not get the weather for {location_text} from the API!")

    # Report the weather
    location_name = get_location_name(Loc)
    if data.units == 'imperial':
        scale = "F"
    else:
        scale = "C"
    print(f"The weather in {location_name} is {data.temp} {scale} and {data.condition}.")

def show_header():
    print('--------------------------------')
    print('---------Weather Client---------')
    print('--------------------------------')
    print('')

def convert_plaintext_location(location_text):
    if not location_text or not location_text.strip():
        return None

    location_text = location_text.lower().strip()
    parts = location_text.split(',')

    city = ""
    state = ""
    country = "US"

    if len(parts) == 1:
        city = parts[0].strip()
    elif len(parts) == 2:
        city = parts[0].strip()
        state = parts[1].strip()
    elif len(parts) == 3:
        city = parts[0].strip()
        state = parts[1].strip()
        country = parts[2].strip()
    else:
        return None

    return Location(city, state, country)

def call_weather_api(Loc,Units="imperial"):
    """
    Calls weather api with Loc tuple with specified temp unit

    :Param Loc: requires a tuple with a city, state, and two letter country code (eg USA should be US)
    :Param Unit: requires either Imperial or Metric to determine temp units
    """
    url = config.url

    Units = Units.lower().strip()

    if Loc.city:
        url += f"&city={Loc.city}"
    if Loc.state:
        url += f"&state={Loc.state}"
    if Loc.country:
        url += f"&country={Loc.country}"
    if Units == "imperial":
        url += f"&units=imperial"
    elif Units == "metric":
        url += f"&units=metric"

    response = requests.get(url)

    if response.status_code in {400, 404, 500}:
        print(f"Error: {response.text}")
        return None

    data = response.json()

    return convert_api_to_weather(data, Loc)

def convert_api_to_weather(data, Loc):
    temp = data.get('forecast').get('temp')
    wjson = data.get('weather')
    condition = f"{wjson.get('category')}: {wjson.get('description').capitalize()}"

    weather = Weather(Loc, data.get('units'), temp, condition)

    return weather

def get_location_name(location):
    if not location.state:
        return f"{location.city.capitalize()}, {location.country.upper()}"
    else:
        return f"{location.city.capitalize()}, {location.state.upper()}, {location.country.upper()}"

if __name__ == "__main__":
    main()

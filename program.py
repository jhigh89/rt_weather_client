import collections
import config

Location = collections.namedtuple('Location', 'city state country')

def main():
    # Show the header
    show_header()

    # Get the location request
    location_text = input("Which city's weather would you like to check? (e.g. San Francisco, CA, US) \n")
    print(f"You selected {location_text}")
    # Convert plaintext over to data we can use
    Loc = convert_plaintext_location(location_text)

    # Get report from the API
    data = call_weather_api(Loc)
    # Report the weather

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
    country = "USA"

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

def call_weather_api(Loc,Unit="imperial"):
    """
    Calls weather api with Loc tuple with specified temp unit

    :Param Loc: requires a tuple with a city, state, and two letter country code (eg USA should be US)
    :Param Unit: requires either Imperial or Metric to determine temp units
    """
    url = config.url

    Unit = Unit.lower().strip()

    if Loc.city:
        url += f"&city={Loc.city}"
    if Loc.state:
        url += f"&state={Loc.state}"
    if Loc.country:
        url += f"&country={Loc.country}"
    if Unit == "imperial":
        url += f"&units=imperial"
    elif Unit == "metric":
        url += f"&units=metric"

    print(f"Would call {url}")

if __name__ == "__main__":
    main()


def main():
    # Show the header
    show_header()

    # Get the location request
    location_text = input("Which city's weather would you like to check? (e.g. San Francisco, CA, USA) \n")
    print(f"You selected {location_text}")
    # Convert plaintext over to data we can use
    # Get report from the API
    # Report the weather

def show_header():
    print('--------------------------------')
    print('---------Weather Client---------')
    print('--------------------------------')
    print('')

if __name__ == "__main__":
    main()

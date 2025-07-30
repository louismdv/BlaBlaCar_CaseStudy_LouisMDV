import folium  # used to draw route on map
from folium import Marker, PolyLine

from selenium import webdriver  # used to generate map screenshot from html file
from selenium.webdriver.chrome.options import Options

from openrouteservice import Client  # used to connect to openrouteservice API
from openrouteservice.exceptions import ApiError

import readline  # used to avoid keystroke perturbations
import time
import os
from dotenv import load_dotenv  # to use the API key stored in a .env file

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('ORS_API_KEY')

client = Client(key=api_key)


# collect user input, verify valid longitude and latitude coordinates and store in stations list
def get_user_input():

    print("Enter bus stations (name, lat, lon). Type 'done' when finished.\n")
    output_file_name = ""
    stations = []
    while True:
        user_input = input("Station name:   ")
        if user_input.lower() == 'done':
            break
        try:
            name, lat, lon = map(str.strip, user_input.split(","))
            lat, lon = float(lat), float(lon)

            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValueError("Error: Coordinates out of range")
            elif stations and lat == stations[-1]['lat'] and lon == stations[-1]['lon']:
                raise ValueError("Error: Same coordinates as last station")

            stations.append({"name": name, "lat": lat, "lon": lon})
            output_file_name += f"{name.split(' -')[0]}->"
        except Exception as e:
            print(f"Error: Invalid input: {e}")

    print('\n')
    output_file_name = output_file_name.rstrip('-> ')
    return stations, output_file_name


def get_route_geometry(coords):

    try:
        route = client.directions(
            coordinates=coords,
            profile='driving-car',
            format='geojson'
        )
        return route['features'][0]['geometry']['coordinates']
    except Exception as e:
        error_str = str(e)
        if '400' in error_str and '2000.0 meters' in error_str:
            print(
                "❌ Error: Route distance too long (max 2000 km). Please choose closer stations.")
            return
        elif '400' in error_str:
            print("❌ Error: Invalid route request. Please check your coordinates.")
            return
        else:
            print(f"❌ Error fetching route: {e}")
            return


def create_maps(stations, output_file_name):

    if len(stations) < 2:
        print("Error: At least 2 stations are required.")
        return

    # Initiate map m
    m = folium.Map(location=[stations[0]['lat'],
                   stations[0]['lon']], zoom_start=6)

    # Add markers for each station
    for station in stations:
        # Create a permanent label using DivIcon with offset
        folium.map.Marker(
            # Small offset to move label away from route + 0.0
            [station['lat'] + 0.01, station['lon'] + 0.01],
            icon=folium.DivIcon(
                html=f'<div style="background-color: white; border: 2px solid black; padding: 5px; border-radius: 5px; font-weight: bold; color: black;">{station["name"]}</div>',
                icon_size=(150, 50),
                icon_anchor=(0, 0)  # Anchor at top-left for better positioning
            )
        ).add_to(m)

        # Also add a regular marker for the clickable point
        folium.Marker(
            [station['lat'], station['lon']],
            popup=station['name'],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    # Prepare coordinates for routing
    coords = [[station['lon'], station['lat']] for station in stations]

    route_coords = get_route_geometry(coords)
    if route_coords:
        # Convert (lon, lat) to (lat, lon) for folium
        latlon = [(pt[1], pt[0]) for pt in route_coords]
        PolyLine(latlon, color="blue", weight=4, opacity=0.8).add_to(m)
    elif route_coords == None:
        return

    os.makedirs('html_routes', exist_ok=True)
    html_result = output_file_name + '.html'
    output_dir = os.path.join("html_routes", html_result)

    m.save(output_dir)
    print(f"✓ Map saved to {output_dir}")
    generate_jpg_map(output_file_name)


def generate_jpg_map(output_file_name):

    try:
        # Create png_routes directory
        os.makedirs('png_routes', exist_ok=True)

        # Create the HTML and JPG file paths
        html_path = os.path.join("html_routes", f"{output_file_name}.html")
        png_path = os.path.join("png_routes", f"{output_file_name}.png")

        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        # Initialize driver
        driver = webdriver.Chrome(options=chrome_options)

        # Load the HTML file
        driver.get(f"file://{os.path.abspath(html_path)}")
        time.sleep(2)  # Wait for map to load

        # Take screenshot
        driver.save_screenshot(png_path)
        driver.quit()

        print(f"✓ PNG saved to: {png_path}")
        return png_path

    except Exception as e:
        print(f"Error generating JPG: {e}")
        return None


def main():

    print('''\nℹ️  If you are in a lack of inspiration here are some coordinate examples:

    Bruxelles - Gare du Midi, 50.834966, 4.333064
    Lille - Europe train station, 50.638638, 3.076491
    Paris - Bercy seine bus station, 48.83568689, 2.380160747
    Angers - Gare Routiere Esplanade, 47.464769, -0.557731
    Lyon - Perrache bus station, 45.749711, 4.826788
    Bordeaux - Belcier bus stop, 44.82271757, -0.5546906559
    Marseille - Saint-Charles bus station, 43.304179, 5.379868
    Barcelone - Gare Routiere Nord, 41.394968, 2.183275''')

    print(f'\n{"=" * 70}\n')

    print("👋 Welcome to the BlaBlaBus Route Planner:\n")

    while True:
        stations, output_file_name = get_user_input()
        create_maps(stations, output_file_name)

        user_input = input("\nWould you like to plan another route? y/n\n")
        if user_input.lower() == 'n':
            break


if __name__ == "__main__":
    main()

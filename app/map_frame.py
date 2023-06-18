import tkinter as tk
from tkinter import ttk
import googlemaps
from datetime import datetime
from urllib.request import urlopen
from io import BytesIO
from tkinterhtml import HtmlFrame
from PIL import Image, ImageTk
import ssl

class MapFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__()
        locations = [
            (50.0541492, 19.9353576), # Starting location
            (50.056999772, 19.935662924), # Ending location
            (50.064192, 19.920094), # Additional location 1
            (50.051994, 19.938195) # Additional location 2
        ]

        self.canvas = tk.Canvas(self, width=600, height=400)
        self.update_map(locations)
        self.chosen_day = 0

    def create_routes(self, locations):
        self.locations = locations
        self.update_map(locations[0:5])

    def change_day(self, day):
        self.update_map(self.locations[day*5:day*5+5])


    def update_map(self, locations):
        # if locations is None:
        #     locations = [(50.064192, 19.920094), (50.051994, 19.938195)]
        self.canvas.delete('all')
        gmaps = googlemaps.Client(key='')


        # Get the directions from Google Maps API
        now = datetime.now()
        waypoints = [f'{lat},{lng}' for lat, lng in locations]
        directions_result = gmaps.directions(
            origin=waypoints[0],
            destination=waypoints[1],
            mode="walking",
            departure_time=now,
            waypoints=waypoints[2:],
            optimize_waypoints=True # Optimize the order of the waypoints for the most optimal route
        )

        # Get the route coordinates
        route = directions_result[0]['overview_polyline']['points']
        decoded_route = googlemaps.convert.decode_polyline(route)

        # Get the duration of the route
        duration = sum(leg['duration']['value'] for leg in directions_result[0]['legs'])

        # Define the map image
        map_zoom = 12
        map_size = "600x400"
        map_type = "roadmap"
        markers = '&'.join([f'markers=color:red%7Clabel:{label}%7C{lat},{lng}' for label, (lat, lng) in zip(['S', 'E'] + list('ABCD'), locations)])
        map_image_url = "https://maps.googleapis.com/maps/api/staticmap?" \
            f"size={map_size}&maptype={map_type}&{markers}&" \
            f"path=weight:5%7Ccolor:blue%7Cenc:{route}&key="

        # Disable certificate verification
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Fetch map image
        map_image_file = urlopen(map_image_url, context=ssl_context)

        # Create a Tkinter window and embed the map image in a canvas
        self.map_image = Image.open(BytesIO(map_image_file.read()))
        self.map_photo = ImageTk.PhotoImage(self.map_image)
        self.canvas.create_image(0, 0, image=self.map_photo, anchor=tk.NW)

        # Draw the route on the canvas
        for i in range(len(decoded_route)-1):
            x1 = decoded_route[i]['lat']
            y1 = decoded_route[i]['lng']
            x2 = decoded_route[i+1]['lat']
            y2 = decoded_route[i+1]['lng']
            self.canvas.create_line(float(x1), float(y1), float(x2), float(y2), fill='red', width=5)

        self.canvas.pack()

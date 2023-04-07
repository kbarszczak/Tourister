import tkinter as tk
import googlemaps
from datetime import datetime
from urllib.request import urlopen
from io import BytesIO
from tkinterhtml import HtmlFrame
from PIL import Image, ImageTk
import ssl

# Replace with your own Google Maps API key
gmaps = googlemaps.Client(key='')

# Define the starting and ending locations as latitude and longitude coordinates
start_location = (50.0541492, 19.9353576)
end_location = (50.056999772, 19.935662924)

# Get the directions from Google Maps API
now = datetime.now()
directions_result = gmaps.directions(start_location, end_location, mode="driving", departure_time=now)

# Get the route coordinates
route = directions_result[0]['overview_polyline']['points']
decoded_route = googlemaps.convert.decode_polyline(route)

# Define the map image
map_zoom = 7
map_size = "600x400"
map_type = "roadmap"
map_image_url = "https://maps.googleapis.com/maps/api/staticmap?" \
    "size={0}&maptype={1}&markers=color:red%7Clabel:S%7C{2},{3}&" \
    "markers=color:red%7Clabel:E%7C{4},{5}&path=weight:5%7Ccolor:blue%7Cenc:{6}&key={7}".format(
        map_size, map_type, start_location[0], start_location[1], end_location[0], end_location[1], route, 'AIzaSyCEXtjl_G_dtv0FBRs6qifX-ZULgDPDI_E')



# Disable certificate verification
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Fetch map image
map_image_file = urlopen(map_image_url, context=ssl_context)



# Create a Tkinter window and embed the map image in a canvas
root = tk.Tk()
# map_image_file = urlopen(map_image_url)
map_image = Image.open(BytesIO(map_image_file.read()))
map_photo = ImageTk.PhotoImage(map_image)
canvas = tk.Canvas(root, width=map_image.width, height=map_image.height)
canvas.create_image(0, 0, image=map_photo, anchor=tk.NW)
print(decoded_route)
# Draw the route on the canvas
for i in range(len(decoded_route)-1):
    x1 = decoded_route[i]['lat']
    y1 = decoded_route[i]['lng']
    x2 = decoded_route[i+1]['lat']
    y2 = decoded_route[i+1]['lng']
    print(x1)
    canvas.create_line(float(x1), float(y1), float(x2), float(y2), fill='red', width=5)

canvas.pack()

# Run the Tkinter event loop
root.mainloop()

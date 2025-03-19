import os
import time
import threading
from flask import Flask, render_template
from dotenv import load_dotenv
from pixoo import Pixoo
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Pixoo
pixoo_host = os.environ.get('PIXOO_HOST', '10.108.32.240')  # Replace with your Pixoo IP
pixoo = Pixoo(pixoo_host)

app = Flask(__name__)

# Function to load pixel sprite from an image
def load_pixel_sprite(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((10, 10))  # Ensure sprite is 10x10

    pixels = []
    for y in range(img.height):
        row = []
        for x in range(img.width):
            row.append(img.getpixel((x, y)))
        pixels.append(row)
    
    return pixels

# Load animation frames
frame_paths = [
    "static/animations/pixil-layer-0.png",
    "static/animations/pixil-layer-1.png",
    "static/animations/pixil-layer-2.png",
    "static/animations/pixil-layer-3.png"
]
animation_frames = [load_pixel_sprite(path) for path in frame_paths]

# Inventory data
computers_count = 5  
total_area = "500 sqm"

# Global flag to control animation loop
running_animation = True

def draw_static_ui():
    """ Draws the static UI (background, text, and box borders) on the Pixoo. """
    # Draw white background
    for y in range(64):
        for x in range(64):
            pixoo.draw_pixel_at_location_rgb(x, y, 255, 255, 255)  # White background

    # Draw Text Labels
    pixoo.draw_text("PCS:", (15, 10), (0, 0, 0))
    pixoo.draw_text(f"{computers_count}", (50, 10), (0, 0, 0))

    pixoo.draw_text("FLOOR:", (15, 35), (0, 0, 0))
    pixoo.draw_text(f"{total_area}", (50, 35), (0, 0, 0))

    # Draw Boxes
    box_positions = [(5, 5), (5, 30), (5, 55)]
    for x, y in box_positions:
        for i in range(10):
            pixoo.draw_pixel_at_location_rgb(x + i, y, 0, 0, 0)  
            pixoo.draw_pixel_at_location_rgb(x + i, y + 10, 0, 0, 0)  
            pixoo.draw_pixel_at_location_rgb(x, y + i, 0, 0, 0)  
            pixoo.draw_pixel_at_location_rgb(x + 10, y + i, 0, 0, 0)  

    pixoo.push()  # Send to Pixoo

def animate_sprite():
    """ Continuously animates the sprite inside the first box without erasing UI. """
    sprite_x, sprite_y = 6, 6  # Position inside the first box

    while running_animation:
        for frame in animation_frames:
            # Clear only the sprite area (not the entire screen)
            for y in range(10):
                for x in range(10):
                    pixoo.draw_pixel_at_location_rgb(sprite_x + x, sprite_y + y, 255, 255, 255)  # White (background)

            # Draw the new frame
            for y in range(len(frame)):
                for x in range(len(frame[y])):
                    r, g, b = frame[y][x]
                    pixoo.draw_pixel_at_location_rgb(sprite_x + x, sprite_y + y, r, g, b)
            
            pixoo.push()  # Send to Pixoo
            time.sleep(1)  # Adjust speed for animation

# Start UI and Animation in separate threads
threading.Thread(target=draw_static_ui, daemon=True).start()
threading.Thread(target=animate_sprite, daemon=True).start()

@app.route('/')
def home():
    return 'Pixoo Inventory Dashboard'

@app.route('/inventory')
def inventory():
    return render_template('inventory.html', computers_count=computers_count, total_area=total_area)

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        running_animation = False  # Stop animation when exiting

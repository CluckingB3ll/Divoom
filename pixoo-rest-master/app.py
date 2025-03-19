import os
from flask import Flask, render_template
from dotenv import load_dotenv
from flasgger import Swagger
from pixoo import Pixoo

# Load environment variables
load_dotenv()

# Configure Pixoo
pixoo_host = os.environ.get('PIXOO_HOST', '10.108.32.240')  # Replace with your Pixoo IP
pixoo = Pixoo(pixoo_host)

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/')
def home():
    return 'Pixoo Inventory Dashboard'

@app.route('/inventory')
def inventory():
    computers_count = 5  # Example count
    total_area = "500 sqm"

    # Set background to white
    for y in range(64):
        for x in range(64):
            pixoo.draw_pixel_at_location_rgb(x, y, 255, 255, 255)  # White background

    # Draw Text at (10,10) pixels
    pixoo.draw_text("PCs:", (10, 10), (0, 0, 0))  # Black text
    pixoo.draw_text(f"{computers_count}", (50, 10), (0, 0, 0))  # Right-aligned number

    # Draw a Horizontal Line
    for x in range(10, 54):  # Draw a line across the width
        pixoo.draw_pixel_at_location_rgb(x, 25, 0, 0, 0)  # Black line at y=25

    # Draw second row of text at (10,35)
    pixoo.draw_text("FLOOR:", (10, 35), (0, 0, 0))  
    pixoo.draw_text(f"{total_area}", (50, 35), (0, 0, 0))  

    pixoo.push()  # Send update to Pixoo

    return render_template('inventory.html', computers_count=computers_count, total_area=total_area)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

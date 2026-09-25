from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Route to serve the main map HTML file
@app.route('/')
def index():
    """
    Renders the main map2.html template.
    """
    return render_template('map3.html')

# Route to serve static files, specifically india_states.json
@app.route('/static/<path:filename>')
def static_files(filename):
    """
    Serves static files from the 'static' directory.
    This is used to provide the india_states.json file to the frontend.
    """
    # Ensure the static folder exists
    static_folder = os.path.join(app.root_path, 'static')
    if not os.path.exists(static_folder):
        print(f"Warning: Static folder not found at {static_folder}")
        # You might want to create it or handle this error more gracefully
        os.makedirs(static_folder, exist_ok=True)

    return send_from_directory(static_folder, filename)

if __name__ == '__main__':
    # Ensure a 'templates' directory exists for map2.html
    templates_path = os.path.join(app.root_path, 'templates')
    if not os.path.exists(templates_path):
        os.makedirs(templates_path)
        print(f"Created 'templates' directory at: {templates_path}")

    # Ensure a 'static' directory exists for india_states.json
    static_path = os.path.join(app.root_path, 'static')
    if not os.path.exists(static_path):
        os.makedirs(static_path)
        print(f"Created 'static' directory at: {static_path}")
        print("Please download 'india_states.json' and place it inside the 'static' folder.")
        print("You can download it from: https://raw.githubusercontent.com/datameet/india-maps/master/States/india_states.geojson")

    # Run the Flask application in debug mode
    app.run(debug=True)
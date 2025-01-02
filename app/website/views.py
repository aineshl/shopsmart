from flask import Blueprint, render_template, request, redirect, url_for
from .process import scrape_and_summarize
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url1 = request.form.get('url1')
        url2 = request.form.get('url2')
        urls = [url1, url2]  # Store user URLs in a list

        # Call the scraping function
        results = scrape_and_summarize(urls)
        
        # Render comparison.html with the results
        return render_template("comparison.html", results=results)
    return render_template("input.html")

def success():
    # Get the results passed from the POST request after scraping
    results = request.args.get('results')

    # If results are passed as a query parameter, decode and process them (e.g., from JSON or another format)
    if results:
        results = json.loads(results)  # Assuming 'results' is being passed as JSON string

    # Display the submitted URLs along with the results on the comparison page
    return render_template("comparison.html", results=results)

@views.route('/test')
def test():
    return "Test page working!"
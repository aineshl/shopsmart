from flask import Blueprint, render_template, request, redirect, url_for
from .process import scrape_and_summarize
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url1 = request.form.get('url1')
        url2 = request.form.get('url2')
        urls = [url1, url2]  

        results = scrape_and_summarize(urls)
        
        return render_template("comparison.html", results=results)
    return render_template("input.html")

def success():
    results = request.args.get('results')

    if results:
        results = json.loads(results) 

    return render_template("comparison.html", results=results)

@views.route('/test')
def test():
    return "Test page working!"
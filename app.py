# Import dependencies
# Import Flask to render template, redirect to another URL, and create a URL
# Import PyMongo to interact with our Mongo database
# Import scraping code to convert from Jupyter notebook to Python
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping


# Initialize Flask app
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection to mars_app database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Homepage route
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)


# Scrape route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)


# Tell Flask to run
if __name__ == "__main__":
   app.run()
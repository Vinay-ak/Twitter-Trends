from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
import subprocess
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client.twitter_trends
collection = db.trending_topics

def home(request):
    return render(request, 'trends/index.html')

def run_script(request):
    try:
        # Run the Selenium script
        subprocess.run(["python", "selenium_script.py"], check=True)


        # Fetch the latest record from MongoDB
        latest_record = collection.find_one(sort=[("date_time_obj", -1)])

        if not latest_record:
            print("No records found in MongoDB.")
            return JsonResponse({"error": "No records found in MongoDB."})


        # Prepare the response
        response = {
            "trends": [
                latest_record.get("trend1", ""),
                latest_record.get("trend2", ""),
                latest_record.get("trend3", ""),
                latest_record.get("trend4", ""),
                latest_record.get("trend5", "")
            ],
            "dateTime": latest_record.get("script_end_time"),
            "ipAddress": latest_record.get("ip_address"),
            "record": latest_record
        }
        return JsonResponse(response)

    except Exception as e:
        print(f"Error: {str(e)}")  
        return JsonResponse({"error": str(e)})


import time
import random
import uuid
import zipfile
import socket
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
from dotenv import load_dotenv
import os


#Load enviornment Variables
load_dotenv()


#Enviorment Variables
MONGO_URI = os.getenv("MONGO_URI")
PROXY_LIST = os.getenv("HOSTS").split(",")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")



#Proxy Authentication Plugin
def proxy_auth_plugin(PROXY):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
    background_js = f"""
    var config = {{
        mode: "fixed_servers",
        rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{PROXY}",
                port: parseInt({PORT})
            }},
            bypassList: ["localhost"]
        }}
    }};
    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    function callbackFn(details) {{
        return {{
            authCredentials: {{
                username: "{USERNAME}",
                password: "{PASSWORD}"
            }}
        }};
    }}
    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {{urls: ["<all_urls>"]}},
        ['blocking']
    );
    """
    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return pluginfile



#IP Address Resolution from Hostname
def resolve_proxy_ip(PROXY):
    """Resolve the proxy hostname to an IP address."""
    try:
        proxy_ip = socket.gethostbyname(PROXY)  # Extract the hostname from the proxy (e.g., in.proxymesh.com)
        print(f"Proxy IP address: {proxy_ip}")
        return proxy_ip
    except socket.gaierror as e:
        print(f"Error resolving proxy IP: {e}")
        return "Unknown IP"



#MongoDB Configuration
def configure_mongo():
    """Connect to MongoDB and return the collection. """
    client = MongoClient(MONGO_URI)
    db = client["twitter_trends"]
    return db["trending_topics"]


#Selenium Configuration
def configure_selenium(pluginfile):
    """Set up the Selenium web driver with the a proxy. """
    options = webdriver.ChromeOptions()
    options.add_extension(pluginfile)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


#Random Proxy Selection
def get_random_proxy():
    """Return a random proxy from the list. """
    return random.choice(PROXY_LIST)    


#User Login
def wait_for_user_login(driver):
    """Pause the script until the user logs in. """
    try:
        driver.get("http://twitter.com/")
        time.sleep(10) #Wait for the page to load
    except Exception as e:
        print(f"Proxy connection failed: {e}")
    #Load the login page
    print("Please log in to Twitter.")
    while True:
        if "home" in driver.current_url: #Check if the user has logged in
            print("Login successful. Proceeding with the scraping...")
            break
        time.sleep(2) #Wait for 2 seconds before checking again


#Trending Topics Fetching
def fetch_trending_topics(driver):
    """Scrape 'What's Happening' section from trending topics. """
    driver.get("https://twitter.com/home") #Ensure the homepage is loaded
    time.sleep(5) #Wait for the page to load

    #Locate the 'What's Happening' section
    trending_elements = driver.find_elements(By.CSS_SELECTOR, "div[aria-label='Timeline: Trending now'] div.r-a023e6.r-rjixqe.r-b88u0q span")
    print(f"Found {len(trending_elements)} trending topics.")
    trends = []
    for trend in trending_elements:
        text = trend.text.strip()  # Safely get text and remove extra whitespace
        if text and text not in trends:  # Ensure text is not empty and unique
            trends.append(text)
        if len(trends) >= 5:  # Stop after collecting 5 unique trends
            break
    print(f"Trending topics: {trends}")
    return trends


#Saving to MongoDB
def save_to_mongo(trends, proxy_ip):
    """Save trending topics to MongoDB. """
    collection = configure_mongo()
    record = {
        "_id": str(uuid.uuid4()), #For unique id
        "trend1": trends[0] if len(trends) > 0 else None,
        "trend2": trends[1] if len(trends) > 1 else None,
        "trend3": trends[2] if len(trends) > 2 else None,
        "trend4": trends[3] if len(trends) > 3 else None,
        "trend5": trends[4] if len(trends) > 4 else None,
        "end_time": datetime.now(),
        "ip_address": proxy_ip
    }
    collection.insert_one(record)
    print("Results saved to MongoDB.")    


#Main Function
def main():
    """Main function to run the script. """
    try:
        #Get a random proxy
        PROXY = get_random_proxy()
        print(f"Using proxy: {PROXY}")

        #Resolve the proxy IP address
        proxy_ip = resolve_proxy_ip(PROXY)

        #Create the proxy authentication plugin
        pluginfile = proxy_auth_plugin(PROXY)

        #Configure Selenium driver with the selected proxy
        driver = configure_selenium(pluginfile)

        #Wait for the user to log in
        wait_for_user_login(driver)

        #Fetch the trending topics
        trends = fetch_trending_topics(driver)

        #Save the results to MongoDB
        save_to_mongo(trends, proxy_ip)

        print("Treanding topics sucessfully fetched and saved to MongoDB.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
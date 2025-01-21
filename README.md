# Twitter-Trends

This project scrapes the top 5 trending topics from Twitter's homepage and stores the results in a MongoDB database. It uses Selenium for web scraping and ProxyMesh for rotating IPs. A simple Django web interface is provided to trigger the scraping process, display the results, and fetch the latest trends from the database.


## Features
- **Selenium Script**: Scrapes Twitter's homepage and fetches the top 5 trending topics under the "What's Happening" section.
- **Proxy Rotation**: Utilizes ProxyMesh to rotate IP addresses for each request, ensuring that the scraper doesn't get blocked.
- **MongoDB**: Stores the results in a MongoDB database, with the name of trends, IP address used, and the date and time of scraping.
- **Django Web Interface**: A simple web page that allows you to trigger the scraping process with a button and view the results in real-time.

## How to use

- **Instal packages**: For running the selenium script and ProxyMesh :

    ```bash
    pip install selenium webdriver-manager pymongo python-dotenv
    ```
- **Enviornment Variables**: Create a .env file in the root directory of the project with the following variables:
    ```bash
    #MongoDB URI
    MONGO_URI=your_mongodb_url

    #Proxymesh Credentials
    USERNAME="your_proxymesh_username"
    PASSWORD="your_proxymesh_password"
    PORT="your_proxymesh_port"
    USE_PROXY='FALSE' or 'TRUE'
    HOSTS="your_proxymesh_hostnames" 
    '(if you have multiple hosts then enter them sperated with a comma)'
    ```
    refer to .env.example for better understanding.

- **Run Django App**: After setting up everything else run the django app using:
    ```bash
    python manage.py runserver
    ```
    make sure you are in the right directory to run this command. 

## Requirements

- **Google Chrome**: You can run the webapp in any browser but Google Chrome must be installed in your system for logging into twitter/X. 

- **ProxyMesh Account**: You need a ProxyMesh account for proxy rotation or you can still run this app without proxy rotation by setting 'USE_PROXY' enviornmnet variable to 'FALSE'. 

- **MongoDB URL**: For storing and fetching the scraped values. 

- **Twitter/X Account**: For log in into twitter/X. 

## To-Do

- Add more browsers support

- Automate twitter/X log-in

- Improve frontend of the django app
# Simple URL Shortener

This repository contains a simple URL shortener service written in Python using Flask and Redis. It's designed to demonstrate the basics of URL shortening and redirection. Please note that this project is intended for educational purposes and is not optimized for state-of-the-art (SOTA) performance or production use.

## Overview

The URL shortener service provides an API to shorten URLs and redirect shortened URLs back to the original URLs. The project uses base62 encoding to convert unique numeric identifiers into a shortened path, which makes up the short URL. 

Redis is used as a datastore to keep the mappings between the shortened paths and the original URLs. This allows for quick lookups and minimal latency during redirection. However, the current implementation is simplistic and does not include features you would expect in a production-ready URL shortener, such as analytics, user authentication, high availability, or advanced security features.

Approach used to shorten a URL is Base62 encoding approach. A UID (only numeric) is converted to its Base62 form, and that is used as the short postfix for the Shortened URL.
Ideally a UID generator is ued in distributed systems, like Twitter Snowflake, but for simplicity purposes we are using a global counter here.

## Getting Started

### Prerequisites

- Python 3.9+
- Flask
- Redis server

### Installation

1. Clone the repository:
   
```
git clone https://github.com/your-username/simple-url-shortener.git
```

Navigate to the project directory:
```
cd simple-url-shortener
```

Install the dependencies:
```
pip install -r requirements.txt
```

Start the Redis server on your local machine:
```
redis-server --port [REDIS-PORT]
```

## Usage
To start the Flask application, run:
```
python server.py
```
Your Flask server should be on `HOST` and `PORT` provided in `config.py`.

To shorten a URL, send a POST request to `/shorten` with the original URL. To access a shortened URL, simply navigate to `http://localhost:6969/<shortened_path>`, and you will be redirected to the original URL, if `<shortened_path>` exists.

## API Endpoints
POST /shorten - Shortens a given URL.
GET /longify - Returns the Long URL of a short URL, if it exists in DB.
GET /<short_id> - Redirects to the original URL based on the short ID, if it exists in DB.

## Disclaimer
This project is for educational purposes only. It is not recommended to use this service as-is for any critical or production-level applications.

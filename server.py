from flask import Flask, request, jsonify, redirect, abort

from datastore import DataStore
from logic import URLShortener


redis_datastore = DataStore()
url_shortener = URLShortener()

app = Flask(__name__)


## THIS PART IS JUST FOR SIMPLICITY PURPOSES, CHECK README FOR MORE INFO
counter = 1000000
def generate_uid():
    global counter
    counter += 1
    return counter
######

@app.route('/shorten', methods = ['POST'])
def shorten():
    # Get the long URL from the POST data
    data = request.json
    
    long_url = data.get('long_url')
    expire = None
    if "expire" in data:
        expire = data.get('expire')

    # Check if the long URL is already in the datastore
    prehash_check = redis_datastore.get(long_url, db_id = 1)
    # If it is, return the existing short URL
    if prehash_check:
        short_url, base62_hash, uid = prehash_check
        return jsonify({
                    'short_url': short_url,
                    'long_url': long_url,
                    'preexisting': True
                })
    
    uid = generate_uid()
    base62_hash = url_shortener.encode_id(uid)
    short_url = "http://localhost:6969/" + base62_hash

    # If it isn't, add it to the datastore
    redis_datastore.set(base62_hash, [short_url, long_url, uid], db_id = 0, expire = expire)
    redis_datastore.set(long_url, [short_url, base62_hash, uid], db_id = 1, expire = expire)

    return jsonify({
                'short_url': short_url,
                'long_url': long_url,
            })


@app.route('/longify', methods = ['GET'])
def longify():
    # Get the short URL from the GET data
    data = request.json
    short_url = data.get('short_url')

    base62_hash = short_url.split('/')[-1]

    # Check if the short URL is in the datastore
    prehash_check = redis_datastore.get(base62_hash, db_id = 0)
    # If it is, return the existing long URL
    if prehash_check:
        short_url, long_url, uid = prehash_check
        return jsonify({
                    'short_url': short_url,
                    'long_url': long_url,
                })
    else:
        return jsonify({
                    'error': 'Short URL not found.'
                })
    

@app.route('/<short_id>')
def redirect_to_long_url(short_id):
    # Attempt to fetch the long URL from Redis
    prehash_check = redis_datastore.get(short_id, db_id = 0)
    
    # If the long URL exists, redirect to it
    if prehash_check:
        short_url, long_url, uid = prehash_check
        return redirect(long_url, code = 302)

    # If the short_id is not found, return a 404 error
    abort(404)


if __name__ == '__main__':
    app.run(debug = True, port = 6969)

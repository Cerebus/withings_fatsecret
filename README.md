# El Cheapo Withings/Nokia Body integration with FatSecret

This is a cheap web function that accepts a weight measurement from a
Withings/Nokia Health Body scale and stuffs it into a predefined
profile in FatSecret.  The web function accepts JSON over POST in the
following form.

```json
{ "weightkg" : 80.0 }
```

The function connects to the FatSecret API and records the value in
the configured user's weight log.

The web function is triggered from [IFTTT](https://ifttt.com).

# Motivation

- Because I'm lazy and I don't want to update my FatSecret log every
  day;
- Because I'm annoyed that FatSecret hasn't provided any Withings integration;
- Because modern APIs make this trivial to accomplish, so there's no
  excuse why FatSecret hasn't done this themselves;
- Because it was an excuse to learn a few new things.

# Installation
## Prerequisites

- FatSecret user account
- IFTTT user account
- FatSecret Platform API account (free account works)
- A place to run a Flask app under Python3

## Dependencies

See `requirements.txt`:
- (Flask)[http://flask.pocoo.org/] to run the server
- (pyfatsecret)[https://github.com/walexnelson/pyfatsecret] to
  interact with the FatSecret Platform API
- (PyYAML)[https://github.com/yaml/pyyaml] to manage configuration data

## Store API keys and user tokens

> **Note:** These values permit access to both the API and your
> personal user data.  Do not put them somewhere where an
> unauthenticated user may view them.  If you're running this web
> function on a cloud service, security is your problem.  By default
> the web function will look in the working directory for the
> credential file, so if that's not a good place to keep it you should
> modify the `flask_listener.py` file appropriately.

### Via script

- Obtain your FatSecret API key and secret from
  [here](https://platform.fatsecret.com/api/Default.aspx?screen=myc)
- Copy the REST API consumer key and REST API shared secret
- Run `store_keys.py` with your API keys as arguments
- Follow the link the script prints
- Authorize the app
- Enter the PIN

```
usage: store_keys.py [-h] [--file FILE] consumer_key consumer_secret

Authorize and store FatSecret user token

positional arguments:
  consumer_key     FatSecret API Consumer Key
  consumer_secret  FatSecret REST API Shared Secret

optional arguments:
  -h, --help       show this help message and exit
  --file FILE      credential storage file
```

### Manually

You'll have to figure out how to get a user token and secret on your
own.  The `store_keys.py` script shows one way to do it.

- Copy the file `sample_fs_credentials.yml` to `fs_credentials.yml`
- Edit `fs_credentials.yml` and add your keys as indicated

## Configuring web hook

Log in to IFTTT and create a new applet
- "If" trigger is "Body Scale - New measurement" from the Withings
  service
  - Authorize IFTTT to receive measurements from Withings/Nokia Health
  
- "Then" action is "Make a web request" from the Web Hooks service
  - URL: wherever you're hosting the Flask app
  - Method: POST
  - Content Type: application/json
  - Body:

```json
{ "weightkg" : {{WeightKg}} }
```

# Run the server
## Testing

You can run the Flask dev server for testing:

```
FLASK_APP=flask_listener.py flask run --host 0.0.0.0
```

By default this listens on port 5000.  Refer to the (Flask
docs)[http://flask.pocoo.org/docs/1.0/server/] for more.

## Production

Consult your hosting environment documentation.

# Limitations & Considerations

- Single user is hard-coded
- POSTs are not authenticated
- No other security, really.  Use at your own risk.
- What error checking?
- FatSecret API free tier is limited to 5000 calls/day (not really a
  problem for a single-user deployment :)

# Future Work

- Deploy to AWS Lambda (probably via Zappa)
- Enable multi-user support
- Remove dependency on IFTTT 
  - Or build an actual IFTTT service
  
# Contributing
    
Feel free to fork this repo and send me pull requests.

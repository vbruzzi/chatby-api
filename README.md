# API Behaviour and Endpoints
This is the expectected behaviour for the Chatby API.

## Setup
To setup this API, run `pip install` inside the folder to download all of the required packages. After that, you should then change the `mongoURI` variable to your MongoDB URI in able to connect to it. Then run `python app.py`. `flask run` will not work due to limitations with Flask-SocketIO, but functionality will remain the same.

 ## Creating a new user
Send a POST request to `/uper` with a JSON payload in the following format: 
```
{
	"username": "vitoRRr",
	"password": "12345"
}
```

 ## Logging in
 Send a GET reqeuest with the username and password in the same format as above. Will return a 200 OK status code with a JSON payload with the stylized username (for display) and the standardized username.
 ```
 {
    "stylizedUsername": "vitoRRr",
    "username": "vitorrr"
}

 ```

## Posting a message
Send a POST request with the message in the following JSON format:
```
{
    "message": "Hello world!",
    "username": "vitorrr"  
}

```
## GET
Gets all the messages. Returns it in JSON in this format:

```
[
    {
        "message": "Hello world!",
        "username": "vitorrr"    
    },
    [...]
]
```
import os

# use `docker inspect` to get the alias of the database container
# it's also the container name or the service name
URL_API = f"http://server:{os.environ['SERVER_PORT']}"
HEADERS = {
    'Authorization': f"Bearer {os.environ['SERVER_JWT_TOKEN']}",
    'Content-Type': "application/json",
    }

# access code whitelist
ACCESS_CODE_WHITELIST = [
    "bananahammock"
    ]
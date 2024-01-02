# Website for Scrolling LED Sign
frontend/backend app to control my DIY scrolling LED sign

# Goals
* users can submit text to scroll

# Quickstart
* `docker-compose up -d --build`
    * app should be available at `${DOMAIN}` (via Traefik)

# Highlights
* Streamlit frontend
    * access code verification
    * paginated tables
* PostgREST backend
    * in `postgrest-py`, expose `QueryParams` to filter data
    * Swagger docs
* reverse proxy and load balancer via Traefik
* pytest

# Resources
* requests between containers<br>https://stackoverflow.com/questions/50040023/containers-communication-with-python-requests
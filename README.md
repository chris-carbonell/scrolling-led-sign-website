# Website for Scrolling LED Sign
frontend/backend app to control my DIY scrolling LED sign

# Goals
* users can submit text to scroll

# Quickstart
* `docker-compose up -d`
    * app should be available at `localhost:8000`

# Highlights
* fastui frontend with fastapi backend
* pytest
* jinja templates for SQL data pulls (incl. conditonal logic)
* overwrite fastapi title casing in endpoint names
* for fun, inherit psycopg connection to assume DSN from environment variables by default

# Resources
* fastui tutorial with form<br>https://www.youtube.com/watch?v=eBWrnSyN2iw
* organizing bigger fastapi projects<br>https://stackoverflow.com/questions/70118412/keeping-endpoint-function-declarations-in-separate-modules-with-fastapi
* tutorial with better base image<br>https://testdriven.io/blog/fastapi-docker-traefik/
* fastapi CORS issues<br>https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/7759
    * but there are dependency conflicts due to `fastui` and `pydantic`
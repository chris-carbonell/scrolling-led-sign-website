# Website for Scrolling LED Sign
frontend/backend app to control my DIY scrolling LED sign

# Goals
* users can submit text to scroll

# Quickstart
* `docker-compose up -d --build`
    * app should be available at `localhost:8000`

# Highlights
* streamlit frontend with fastapi backend
* pytest
* jinja templates for SQL data pulls (incl. conditonal logic)
* overwrite fastapi title casing in endpoint names
* for fun, inherit psycopg connection to assume DSN from environment variables by default

# Resources
* organizing bigger fastapi projects<br>https://stackoverflow.com/questions/70118412/keeping-endpoint-function-declarations-in-separate-modules-with-fastapi
* more details in logging<br>https://gist.github.com/liviaerxin/d320e33cbcddcc5df76dd92948e5be3b
* streamlit + fastapi tutorial<br>https://medium.com/codex/streamlit-fastapi-%EF%B8%8F-the-ingredients-you-need-for-your-next-data-science-recipe-ffbeb5f76a92
* streamlit + traefik repo<br>https://github.com/joeychrys/streamlit_deployment
* requests between containers<br>https://stackoverflow.com/questions/50040023/containers-communication-with-python-requests
* SQLAlchemy with postgres and FastAPI repo<br>https://github.com/AmishaChordia/FastAPI-PostgreSQL-Docker
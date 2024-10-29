
FROM python:3.12.7

# Update and install necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1945 infotek && useradd -u 1945 -g infotek -s /bin/sh infotek

# RUN mkdir -p /data

RUN mkdir -p /code

WORKDIR /code


# COPY ./src/requirements.txt /code/requirements.txt
COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./src/app /code/app

RUN chown -R infotek.infotek /code/app
USER infotek

EXPOSE 8080

# CMD ["fastapi", "run", "app/main.py", "--port", "8080"]
# Command to run the FastAPI application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
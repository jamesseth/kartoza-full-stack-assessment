FROM python:3.8-slim-buster
ARG WORKDIR=/app
ENV PROJECT_NAME kartoza

# Set number of gunicorn workers .
ENV NUMBER_OF_GUNICORN_WORKERS=2
# Prevent Python io buffering.
ENV PYTHONUNBUFFERED=1
# Stop Python from creating *.pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    locales \
    gnupg2 \
    wget \
    ca-certificates \
    rpl \
    pwgen \
    software-properties-common \
    iputils-ping \
    apt-transport-https \
    curl \
    gettext \
    libxml2-dev \
    zlib1g-dev \
    netcat \
    gdal-bin

RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal
COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN rm -f requirements.txt

# Create non root user and django group
RUN groupadd -r django && useradd -r -s /bin/false -g django django



WORKDIR $WORKDIR
COPY . .
RUN chown -R django:django /app

# Kick-off Gunicorn
# CMD exec gunicorn --bind :8000 --workers $NUMBER_OF_GUNICORN_WORKERS ${PROJECT_NAME}.wsgi:application
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]

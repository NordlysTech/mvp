# Base image
FROM python:3.10-slim


# Install build dependencies for numpy
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    clang \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

#-------------------------------------------------
COPY ./requirements.txt /app/requirements.txt

# Create a working directory in the image
WORKDIR /app 

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD [ "python", "-u","-m"  , "flask", "run", "--host=0.0.0.0"]
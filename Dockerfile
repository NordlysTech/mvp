# Base image
FROM python:3-slim

# Update and upgrade packages
RUN apt-get update && \
    apt-get install -y ffmpeg


# -----------------------------------------------
# Install required dependencies
RUN apt-get update \
    && apt-get install -y build-essential libssl-dev ca-certificates libasound2 wget \
    && rm -rf /var/lib/apt/lists/*

# Download and install OpenSSL
WORKDIR /usr/src
RUN wget -O - https://www.openssl.org/source/openssl-1.1.1u.tar.gz | tar zxf - \
    && cd openssl-1.1.1u \
    && ./config --prefix=/usr/local \
    && make -j $(nproc) \
    && make install_sw install_ssldirs \
    && ldconfig -v

# Set SSL_CERT_DIR environment variable
ENV SSL_CERT_DIR=/etc/ssl/certs

# Set LD_LIBRARY_PATH environment variable
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
 
#-------------------------------------------------
COPY ./requirements.txt /app/requirements.txt

# Create a working directory in the image
WORKDIR /app 

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD [ "python", "-u","-m"  , "flask", "run", "--host=0.0.0.0"]
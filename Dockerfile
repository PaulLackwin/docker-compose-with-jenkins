FROM apache/nifi

USER root

# Install Python and pip
RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip
# Set the working directory inside the container
WORKDIR /opt/nifi/nifi-current

# Install Python libraries using pip
COPY requirements.txt /opt/nifi/nifi-current
RUN python3 -m pip install --no-cache-dir -r requirements.txt

USER nifi

# Start NiFi
CMD ["bin/nifi.sh", "run"]

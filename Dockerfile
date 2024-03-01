FROM nikolaik/python-nodejs:python3.10-nodejs18

# Update package lists, upgrade existing packages, and install necessary packages
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg neofetch \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the local directory contents into the container at /app/
COPY . /app/

# Set the working directory to /app/
WORKDIR /app/

# Install Python dependencies from requirements.txt
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt

# Specify the default command to run on container start
CMD ["python3", "-m", "main.py"]

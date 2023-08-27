# Set base image (host OS)
FROM python:3.8-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies\
RUN apk add --no-cache bash
RUN apk add make automake gcc g++ subversion python3-dev
RUN apk update
RUN apk add apache2
RUN apk add apache2-dev
RUN apk add apache2-utils 
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app.py .

# Specify the command to run on container start
CMD [ "python", "./app.py" ]

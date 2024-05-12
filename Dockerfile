# Use the official Python 3.10 image from Docker Hub as the base image
FROM python:3.10

# Set maintainer information
MAINTAINER Morteza Mogharrab <morteza.mgb@gmail.com>

# Add the current directory (.) to the /src directory in the Docker image
ADD . /src

# Set the working directory inside the Docker image to /src
WORKDIR /src

# Run pip install commands to install Flask and Gunicorn Python packages
RUN pip install --upgrade pip \
    && pip install flask gunicorn

# Copy the entrypoint.sh script from the host machine to the root directory (/) of the Docker image
COPY entrypoint.sh /

# Change the permissions of the entrypoint.sh script to make it executable
RUN chmod +x /entrypoint.sh

# Create a volume named /src/db in the Docker image
VOLUME /src/db

# Expose port 5040 on the Docker container
EXPOSE 5040

# Specify the default command to run when the Docker container starts, which is to run the entrypoint.sh script
CMD ["/entrypoint.sh"]

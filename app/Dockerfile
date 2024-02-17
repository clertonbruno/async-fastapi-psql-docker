# Use Python 3.10 slim image as the base image for the builder stage
FROM python:3.10-slim AS builder

# Copy the requirements.txt and requirements-dev.txt files into the image
COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt

# Upgrade pip and install dependencies listed in requirements.txt without caching to reduce image size
RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# Use an argument to allow customization of the environment (e.g., development, test, production)
ARG ENV

# Conditionally install additional development dependencies if the environment is set to test
RUN if [ "$ENV" = "test" ]; then \
    pip install --user --no-cache-dir -r requirements-dev.txt; \
    fi;

# Start a new stage for the production image to keep it clean and secure
FROM python:3.10-slim AS production

# Prevent Python from creating .pyc files and ensure immediate output of print statements and logs.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

# Copy installed packages from the builder stage to the production image
COPY --from=builder /root/.local /root/.local

# Update PATH environment variable to include the directory where the packages were installed
ENV PATH=/root/.local/bin:$PATH

# Set the working directory to /app
WORKDIR /app

# Copy the application source code to the working directory in the image
COPY . /app

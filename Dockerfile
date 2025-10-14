# Dockerfile

# Step 1: Start from a secure, minimal Python base image.
# 'slim' images are smaller and have a reduced attack surface, a best practice for production.
FROM python:3.11-slim

# Step 2: Set the working directory inside the container.
# All subsequent commands (like COPY, RUN) will be relative to this path.
WORKDIR /app

# Step 3: Copy only the requirements file first to leverage Docker's layer caching.
# This is a key optimization: if requirements.txt doesn't change, Docker won't
# re-install all the dependencies on subsequent builds, making them much faster.
COPY requirements.txt .

# Step 4: Install dependencies in a clean, non-cached way.
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the .env file with our secrets.
# This is a simple method for local testing. In a real cloud deployment, secrets
# would be injected securely using a service like AWS Secrets Manager or GCP Secret Manager.
COPY .env .

# Step 6: Copy the rest of the application source code and configuration.
COPY . .

# Step 7: Build the data artifact (the vectorstore) INSIDE the container.
# This ensures our knowledge base is part of the final, self-contained image,
# making it truly portable and solving the "it works on my machine" problem.
RUN python 04_create_vectorstore.py

# Step 8: Expose the port that Chainlit runs on.
# This tells Docker which port the application *inside* the container will listen on.
EXPOSE 8000

# Step 9: Define the command to run when the container starts.
# The host '0.0.0.0' is essential for making the app accessible from outside the container.
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]

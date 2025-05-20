FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . .

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]

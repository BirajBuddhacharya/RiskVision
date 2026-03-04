# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /RiskVision

# Copy the current directory contents into the container at /RiskVision
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the Flask app when the container launches
CMD ["python3", "app.py"]

# Step 1: Use an official Python runtime as the base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /work_files_db_1
			

# Step 3: Copy all (.) into your Python app to the container
COPY . /work_files_db_1

# Step 3: Copy the requirements.txt (or any dependency file)
COPY requirements.txt .

# Step 4: Install dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for Python
ENV PYTHONUNBUFFERED 1

# Step 6: Specify the command to run your Python app
CMD ["python", "simple_sql_app.py"]
# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (required for Cloud Run)
ENV PORT=8080
EXPOSE 8080

# Start the bot
CMD ["python", "bot.py"]

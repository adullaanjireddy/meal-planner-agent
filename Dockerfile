FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . .

# Create memory directory
RUN mkdir -p /app/memory/profiles

# Expose ports
# Expose only Streamlit port
EXPOSE 8501

CMD sh -c "python backend/server.py & streamlit run app.py --server.port=8501 --server.address=0.0.0.0"
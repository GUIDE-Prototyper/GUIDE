# Comprehensive Installation Guide for Running the Backend on a Server

This guide will walk you through the process of setting up and running the backend application on your server. The application is a Quart app running with Gunicorn and connected to Nginx. Follow the steps below to ensure a successful installation and deployment.

## Prerequisites

Before you begin, ensure you have the following:

- A server with a Unix-based operating system (e.g., Ubuntu).
- Access to the server with sudo privileges.
- Python 3.7 or later installed.
- Git installed on your server.
- Nginx installed and running.
- OpenAI API key and organization ID.

## Step-by-Step Installation

### 1. Clone the Repository

1. **Create a directory for the project:**

   ```bash
   sudo mkdir -p /data/GUIDE
   sudo chown $USER:$USER /data/GUIDE
   ```

2. **Clone the repository:**

   ```bash
   git clone github-repo-url /data/GUIDE
   ```

### 2. Set Up a Python Virtual Environment

1. **Install `virtualenv` if not already installed:**

   ```bash
   sudo apt-get update
   sudo apt-get install python3-venv
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv /data/venv-guide
   ```

3. **Activate the virtual environment:**

   ```bash
   source /data/venv-guide/bin/activate
   ```

### 3. Install Dependencies

1. **Navigate to the project directory:**

   ```bash
   cd /data/GUIDE
   ```

2. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

### 4. Configure OpenAI API

1. **Locate the `openai_conf` file in the quartapp directory.**

2. **Edit the file to include your OpenAI API key and organization ID:**

   ```plaintext
   api_key=your_openai_api_key
   organization=your_openai_org_id
   ```

### 5. Configure Gunicorn

1. **Ensure the Gunicorn configuration file is correctly set up:**

   The `gunicorn.conf.py` file should be located in `/data/GUIDE/`. Ensure it is configured to use 24 workers.

### 6. Set Up Nginx

1. **Create an Nginx configuration file for your app:**

   ```bash
   sudo nano /etc/nginx/sites-available/yourapp
   ```

2. **Add the following configuration:**

   ```nginx
   server {
       listen 80;
       server_name your_domain_or_IP;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Enable the configuration:**

   ```bash
   sudo ln -s /etc/nginx/sites-available/yourapp /etc/nginx/sites-enabled
   ```

4. **Test and restart Nginx:**

   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### 7. Deploy the Application

1. **Create a deploy script:**

   Use the `deploy.sh` script found under "scripts" directory to deploy quartapp to gunicorn server:

   ```bash
   #!/bin/bash

   # Define variables
   REPO_URL="github-repo-url"
   REPO_DIR="/data/GUIDE/"
   VENV_DIR="/data/venv-guide/"
   GUNICORN_CONFIG="/data/GUIDE/gunicorn.conf.py"

   # Function to handle errors
   function error_exit {
       echo "$1" 1>&2
       exit 1
   }

   # Update GitHub repo
   echo "Cloning repository from GitHub..."
   cd "$REPO_DIR" || error_exit "Failed to access newly cloned repository"
   git pull "$REPO_URL" || error_exit "Failed to clone repository from GitHub"

   # Activate the virtual environment
   echo "Activating virtual environment..."
   if [ -f "$VENV_DIR/bin/activate" ]; then
       source "$VENV_DIR/bin/activate"
   else
       error_exit "Virtual environment not found"
   fi

   # Install dependencies
   echo "Installing dependencies..."
   pip install -r requirements.txt || error_exit "Failed to install dependencies"

   # Restart Gunicorn
   echo "Restarting Gunicorn..."
   pkill -f gunicorn
   echo "Starting Gunicorn..."
   gunicorn -c "$GUNICORN_CONFIG" quartapp.app:app --daemon || error_exit "Failed to start Gunicorn"
   ```

2. **Make the script executable:**

   ```bash
   chmod +x deploy.sh
   ```

3. **Run the deploy script:**

   ```bash
   ./deploy.sh
   ```

### 8. Verify the Installation

- Open a web browser and navigate to your server's domain or IP address to verify that the application is running correctly.

## Conclusion

You have successfully set up and deployed the backend application on your server. For any issues, refer to the logs and ensure all configurations are correctly set.

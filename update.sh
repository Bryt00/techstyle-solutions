#!/bin/bash
# update.sh - Use this for pushing code changes
set -e

PROJECT_NAME="techstyle"
# Make sure this matches the path used in deploy.sh!
PROJECT_DIR="/home/bryt/sites/$PROJECT_NAME"

cd $PROJECT_DIR

echo "========================================="
echo "  Updating $PROJECT_NAME..."
echo "========================================="

# 1. Pull latest code
echo "=> Pulling latest code..."
git pull origin main

# 2. Activate venv and install/update dependencies
echo "=> Installing dependencies..."
. venv/bin/activate
pip install -r requirements.txt

# 3. Load .env and run Django tasks
echo "=> Running Django migrations & collecting static files..."
python manage.py migrate
python manage.py collectstatic --noinput

# 4. Fix permissions for static/media
echo "=> Setting file permissions..."
USER="bryt"
sudo chown -R $USER:www-data $PROJECT_DIR/staticfiles
sudo chmod -R 755 $PROJECT_DIR/staticfiles
sudo chown -R $USER:www-data $PROJECT_DIR/media
sudo chmod -R 775 $PROJECT_DIR/media

# 5. Restart services
echo "=> Restarting Gunicorn..."
sudo systemctl restart gunicorn_${PROJECT_NAME}
# Only restart Nginx if you changed the nginx config
# sudo systemctl restart nginx

echo "========================================="
echo "  Update complete!"
echo "========================================="
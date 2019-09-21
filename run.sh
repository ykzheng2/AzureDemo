export FLASK_APP=application.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=config.py
chmod +x run.sh
python -m flask run -p 5000
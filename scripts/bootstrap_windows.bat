@echo off
REM Bootstrap script for setting up the streaming bot

echo Setting up the Python virtual environment...
pip install pipenv
pipenv install

echo Cloning configuration files from GitHub...
git clone https://github.com/your-repo/streaming_bot_configs.git configs/

echo Setting up the bot...
pipenv run python scripts/run_bot.py

echo Setup complete. You can now run the bot using pipenv run python scripts/run_bot.py
pause

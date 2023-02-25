# MCprep Helpful Horse

## How to run locally
1. Create a bot with the Discord Developer Portal (https://docs.pycord.dev/en/master/discord.html)
    
    1a. Make sure the bot is able to timeout other users and setup commands

2. Create a file called `config.json` and add the following:
```json
{
    "token" : "TOKEN HERE"
}
```

3. In main.py, edit these globa variables to your liking:
```py
MCPREP_GUILD_ID       = 737871405349339232 # Server ID
IDLE_MINER_CHANNEL_ID = 746745594458144809 # Channel you want to exclude
STAFF_CHAT_ID         = 741151005688987769 # Channel you want to send reports to
```

4. Install Pycord:
```bash
# NOTE: Python 3.8 and above is needed
# Mac and linux
python3 -m pip install -U py-cord

# Windows
py -3 -m pip install -U py-cord
```

5. Run main.py:
```bash
python3 main.py
```

6 (OPTIONAL). Using systemd to run the bot (Requires Linux):

Run:
```bash
sudo nano /etc/systemd/system/mcprep-helpful-horse.service
```

And add these contents:
```service
[Unit]
Description=MCprep_Helpful_Horse
After=network-online.target

[Service]
Type=simple
WorkingDirectory=DIRECTORY_WITH_MAIN_PY
ExecStart=PATH_TO_PYTHON PATH_TO_MAIN_PY
Restart=on-failure
User=USER_TO_EXECUTE_SERVICE_FILE_ON
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

Then you can run these commands:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mcprep-helpful-horse.service # Makes the service file start on boot
sudo systemctl start mcprep-helpful-horse.service # starts service file
sudo systemctl status mcprep-helpful-horse.service # shows the status of the service file
```

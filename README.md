# Housing Waiting List Bot

A Python script that checks apartment waiting list sites (e.g., `findbolig.nu`) every 10 minutes from 8:00–21:50 Copenhagen time on a Raspberry Pi, sending email alerts for changes.
Living in Copenhagen, the housing market is difficult to get into. Some rentals offer good prices, but only if you catch their waiting lists the moment they open. Manually checking sites like `findbolig.nu` was a hassle, so I built this script. It runs every 10 minutes on my Raspberry Pi, checking for changes, and emails me if a waiting list opens—no more constant refreshing :)

## Features
- Scrapes sites for updates
- Emails via Gmail if text != "Lukket for opskrivning" - (Danish for 'The waiting list is closed')
- Runs via cron job

## Setup
1. **Clone Repo**  
   `git clone git@github.com:Mathias2860DK/housing-waiting-list-bot.git && cd housing-waiting-list-bot`

2. **Set Up Virtual Env**  
   `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`

3. **Add Email Credentials**  
   Create `.env`:  
   `echo "EMAIL=your-email@gmail.com" > .env && echo "EMAIL_PASSWORD=your-app-password" >> .env && chmod 600 .env`

4. **Test Script**  
   `python3 scrape-and-alert.py`

5. **Set Cron Job**  
   `crontab -e`  
   Add:  
   `*/10 8-21 * * * /home/pi/housing-waiting-list-bot/venv/bin/python3 /home/pi/housing-waiting-list-bot/scrape-and-alert.py >> /home/pi/housing-waiting-list-bot/cron.log 2>&1`

## Files
- `scrape-and-alert.py`:
- `requirements.txt`: Dependencies
- `.gitignore`: Ignores `venv/`, `.env`, `*.log`

## Notes
- Uses `verify=False` for HTTPS (Help me fix this :P)
- Logs to `scrape.log`

## Author
[Mathias2860DK](https://github.com/Mathias2860DK)

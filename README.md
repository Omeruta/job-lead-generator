# Job Lead Generator 🔎💼

This is a fully automated lead generation tool built with Python.

It:

✅ Scrapes jobs from [RemoteOK](https://remoteok.com)  
✅ Filters by keyword (e.g. "Engineer")  
✅ Enriches company contacts via [Hunter.io API](https://hunter.io)  
✅ Uploads job info to Google Sheets  
✅ Sends daily Slack alerts  
✅ Runs automatically using Task Scheduler on Windows

## 📸 Demo Screenshot
![screenshot](link-if-you-want)

## 🔧 How It Works

1. `ScrapeScript.py` scrapes jobs and filters by keyword
2. `enrich_with_hunter.py` gets verified emails and LinkedIn
3. `upload_to_sheet.py` sends results to Google Sheets
4. `notify_slack.py` sends alerts for new matches
5. `run_scraper.bat` automates the full pipeline (Windows)

## 💡 Tech Stack

- Python
- Playwright
- Google Sheets API
- Hunter.io API
- Slack Webhooks
- Windows Task Scheduler

## 🧪 Example Output (remoteok_jobs.csv)

| title               | company   | email              | linkedin             |
|--------------------|-----------|--------------------|----------------------|
| Backend Engineer   | Orga AI   | jason@orga.ai      | linkedin.com/in/jason |
| Python Developer   | IO Global |                    |                      |

## 🛠️ Run It

```bash
python ScrapeScript.py

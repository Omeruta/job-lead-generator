import requests

def send_slack_alert(jobs, webhook_url):
    if not jobs:
        return

    message = f"*🚨 {len(jobs)} new job(s) found!*\n"
    for job in jobs[:5]:  # Limit preview to 5 jobs
        message += f"• <{job['url']}|{job['title']} at {job['company']}>\n"

    payload = {
        "text": message
    }

    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print("✅ Slack alert sent.")
    else:
        print(f"⚠️ Failed to send Slack alert: {response.status_code} - {response.text}")

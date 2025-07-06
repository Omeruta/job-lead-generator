from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from upload_to_sheet import upload_to_gsheet
from notify_slack import send_slack_alert
from enrich_with_hunter import enrich_company_with_hunter

# --- Configs ---
keyword = "Engineer"
SHEET_ID = "1ekD9L9A56USt7NVh_iU73bKo4jOxPhjufhYcUkWttD0"
SHEET_NAME = "Sheet1"
CREDS_PATH = "creds.json"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
HUNTER_API_KEY = "39609e42d46bfdbed381732edd54ecdaed3e6a0f"


# --- Scraping Function ---
def get_jobs(keyword=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://remoteok.com", timeout=60000)
        page.wait_for_timeout(3000)
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    jobs = []

    rows = soup.find_all("tr", class_="job")
    print(f"Found {len(rows)} job rows on the page.")

    for row in rows:
        title_tag = row.find("h2")
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        company = row.get("data-company")
        link_tag = row.find("a", class_="preventLink")
        link = f"https://remoteok.com{link_tag['href']}" if link_tag else None
        tags = [tag.text for tag in row.find_all("h3", class_="tag")]

        if keyword:
            keyword_lower = keyword.lower()
            if (keyword_lower not in title.lower()) and not any(keyword_lower in tag.lower() for tag in tags):
                continue

        print(f"Found: {title} at {company}")
        jobs.append({
            "title": title,
            "company": company,
            "url": link,
            "tags": tags,
        })

    return jobs


# --- Main Logic ---
print("🟢 Scraper started...")
job_list = get_jobs(keyword)
print(f"✅ Found {len(job_list)} matching jobs.")

# Enrich with Hunter
for job in job_list:
    enrichment = enrich_company_with_hunter(job["company"], HUNTER_API_KEY)

    if enrichment:
        job.update({
            "domain": enrichment.get("domain", ""),
            "email": enrichment.get("email", ""),
            "first_name": enrichment.get("first_name", ""),
            "last_name": enrichment.get("last_name", ""),
            "position": enrichment.get("position", ""),
            "linkedin": enrichment.get("linkedin", ""),
        })
    else:
        job.update({
            "domain": "", "email": "", "first_name": "", "last_name": "", "position": "", "linkedin": ""
        })

# Create final DataFrame
df = pd.DataFrame(job_list)
df["tags"] = df["tags"].apply(lambda tags: ", ".join(tags))

# Save to CSV
df.to_csv("remoteok_jobs.csv", index=False)
print("✅ Saved to remoteok_jobs.csv")

# Upload to Google Sheet
upload_to_gsheet(df, SHEET_NAME, CREDS_PATH, SHEET_ID)
print("✅ Uploaded to Google Sheet")

# Send Slack alert (only after enrichment!)
print(f"🔔 Sending Slack alert for {len(job_list)} jobs...")
send_slack_alert(job_list, SLACK_WEBHOOK_URL)

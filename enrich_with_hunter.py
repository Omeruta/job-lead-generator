import requests

def enrich_company_with_hunter(company_name, api_key):
    search_url = "https://api.hunter.io/v2/domain-search"
    params = {
        "company": company_name,
        "api_key": api_key
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    if response.status_code != 200 or "data" not in data:
        return None

    domain = data["data"].get("domain", "")
    emails = data["data"].get("emails", [])

    if emails:
        primary = emails[0]
        return {
            "domain": domain,
            "email": primary.get("value"),
            "first_name": primary.get("first_name"),
            "last_name": primary.get("last_name"),
            "position": primary.get("position"),
            "linkedin": primary.get("linkedin")
        }

    return {
        "domain": domain,
        "email": "",
        "first_name": "",
        "last_name": "",
        "position": "",
        "linkedin": ""
    }

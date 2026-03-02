import requests
from pathlib import Path
import yaml
import re
from datetime import datetime

# ---------------- CONFIG ----------------
HAL_ID = "pntumbawantumba"  # Your HAL ID
OUTPUT_DIR = Path("/home/pntumba/cnam/Personal Website/pntumbawantumba.github.io/content/publications")
ROWS = 1000  # Fetch all publications

# ---------------- HELPERS ----------------
def safe_filename(title):
    """Safe filename for markdown file."""
    return "".join(c if c.isalnum() else "_" for c in title[:50])

def parse_label(label):
    """
    Extract authors, title, venue, year, DOI from HAL 'label_s'
    """
    # Remove HTML entities
    label = label.replace("&#x27E8;", "").replace("&#x27E9;", "")
    
    parts = label.split(". ")
    authors = parts[0] if len(parts) > 0 else ""
    title = parts[1] if len(parts) > 1 else ""
    venue = parts[2] if len(parts) > 2 else ""
    
    # Extract year (first 4-digit number from 1900–2099)
    year_match = re.search(r"\b(19\d{2}|20\d{2})\b", label)
    year = year_match.group(0) if year_match else str(datetime.today().year)
    
    # Extract DOI if present
    doi_match = re.search(r"10\.[^\s&#]+", label)
    doi = doi_match.group(0) if doi_match else ""
    
    # Detect thesis/technical report
    is_thesis = "thesis" in venue.lower() or "these" in venue.lower() or "tel-" in label.lower()
    
    return authors, title, venue, year, doi, is_thesis

# ---------------- FETCH DATA ----------------
print("Fetching HAL publications...")
url = f"https://api.archives-ouvertes.fr/search/?q=authIdHal_s:{HAL_ID}&wt=json&rows={ROWS}"
resp = requests.get(url)
resp.raise_for_status()
data = resp.json()
docs = data["response"]["docs"]

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------- PROCESS ----------------
for doc in docs:
    label = doc.get("label_s", "")
    uri = doc.get("uri_s", "")
    
    if not label:
        continue
    
    authors, title, venue, year, doi, is_thesis = parse_label(label)
    
    # Define type
    pub_type = "thesis" if is_thesis else "publication"
    
    # Create filename
    filename = OUTPUT_DIR / f"{safe_filename(title)}.md"
    
    # Build YAML front matter
    content = {
        "title": title,
        "date": f"{year}-01-01",
        "type": "publication",
        "authors": [a.strip() for a in authors.split(",")],
        "publication": venue,
        "hugoblox": {
            "ids": {
                "doi": doi if doi else None
            }
        },
        "links": [
            {
                "name": "PDF",
                "url": uri,
                "type": "pdf"
            }
        ]
    }
    
    if not doi:
        content["hugoblox"]["ids"].pop("doi")

    # Write to markdown file
    with open(filename, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(content, f, allow_unicode=True)
        f.write("---\n")

print(f"✅ {len(docs)} publications synced to {OUTPUT_DIR}")
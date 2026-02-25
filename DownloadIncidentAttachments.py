##########################################
## This script downloads all attachments##
## associated with Incident records.    ##
## To use for another table, adjust the ##
## queries and whatnot.                 ##
## This script doesn't get around the   ##
## export limit imposed by ServiceNow.  ##
##########################################

import requests
from concurrent.futures import ThreadPoolExecutor,as_completed
import time
import os
from pathlib import Path
from pathvalidate import sanitize_filename


# User Params
user = 'USERNAME'
pwd = 'PASSWORD'

# Instance Params
instanceURL = 'https://INSTNACENAME.service-now.com'
attachmentQuery = 'table_name=incident'

# Directory to save attachments
DOWNLOAD_DIR="attachments"
os.makedirs(DOWNLOAD_DIR,exist_ok=True)

##########################################
## Download individual attachments      ##
##########################################
def download_attachment(item):
    download_link=item["download_link"]
    file_name=make_windows_safe_filename(item["file_name"])
    table_sys_id=item["table_sys_id"]

    # Fetch incident number
    try:
        inc_url=instanceURL + f"/api/now/table/incident/{table_sys_id}?sysparm_fields=number"
        inc_res=requests.get(inc_url,auth=(user,pwd))
        inc_res.raise_for_status()
        inc_num=inc_res.json()["result"]["number"]
    except:
        inc_num="INCNotFound"

    save_name=f"{inc_num}_{file_name}"
    save_path=os.path.join(DOWNLOAD_DIR,save_name)# Download attachment file
    try:
        r=requests.get(download_link,auth=(user,pwd))
        r.raise_for_status()

        with open(save_path,"wb")as f:
            f.write(r.content)
            return f"Downloaded: {save_name}"
    except Exception as e:
        return f"FAILED: {save_name}({e})"

##########################################
## Ensure safe file names               ##
##########################################
def make_windows_safe_filename(name: str, max_len: int = 255) -> str:
    """
    Ensure a valid Windows file name using pathvalidate.sanitize_filename().
    - Preserves the original extension when possible.
    - Removes characters invalid on Windows (e.g., <>:\"/\\|?*), control chars, etc.
    - Strips trailing spaces and dots (invalid on Windows).
    - Caps the final file name length (default 255 chars for a *file name*, not full path).

    Returns a safe file name string.
    """
    if not name:
        return "unnamed"

    # Split into stem + extension to better preserve original extension
    p = Path(name)
    stem = p.stem or "unnamed"
    ext  = p.suffix  # includes the leading dot if present

    # Sanitize stem and extension separately (extension rarely needs it, but safe to normalize)
    safe_stem = sanitize_filename(stem, platform="windows")
    safe_ext  = sanitize_filename(ext,  platform="windows")

    # Recombine; ensure ext starts with a dot (or is empty)
    if safe_ext and not safe_ext.startswith("."):
        safe_ext = "." + safe_ext

    fname = f"{safe_stem}{safe_ext}" if safe_stem else f"unnamed{safe_ext}"

    # Windows does not allow trailing spaces or dots in file names
    fname = fname.rstrip(" .")

    # Enforce max length for the **name** (not the full path). Keep the extension intact.
    if len(fname) > max_len:
        # Reserve space for extension when trimming
        base_len = max_len - len(safe_ext)
        if base_len <= 0:
            # Extension itself is too long—fallback to hard trim
            fname = fname[:max_len]
        else:
            fname = f"{safe_stem[:base_len]}{safe_ext}"

        # Re‑strip again in case trimming introduced trailing spaces/dots
        fname = fname.rstrip(" .")

    # Final fallback
    return fname or "unnamed"

##########################################
## Get list of attachments              ##
##########################################
url=instanceURL + "/api/now/attachment?sysparm_query=" + attachmentQuery

headers={"Content-Type": "application/json","Accept": "application/json"}
response=requests.get(url,auth=(user,pwd),headers=headers)
response.raise_for_status()
data=response.json()
attachments=data["result"]

print(f"Total attachments: {len(attachments)}")

##########################################
## Parallel download                    ##
##########################################

#----CRITICAL: Set a SAFE concurrency level----# ServiceNow can handle ~1,000 req/sec,but be VERY conservative
MAX_WORKERS=100

print(f"Starting parallel download with {MAX_WORKERS} workers...")

start=time.time()
results=[]

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    future_to_item={executor.submit(download_attachment,item): item for item in attachments}

    for future in as_completed(future_to_item):
        result=future.result()
        print(result)
        results.append(result)
        end=time.time()
        print(f"\nCompleted in {end-start:.2f} seconds.")

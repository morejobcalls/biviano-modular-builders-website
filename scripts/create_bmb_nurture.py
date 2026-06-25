#!/usr/bin/env python3
"""
Create BMB 8-week modular nurture sequence in GHL.
- Creates folder `Nurture - Modular Lead 8 Week` in Biviano sub-account
- Creates 12 HTML email templates (one per .md file) inside that folder
- Each template: subject from frontmatter, plain-text feel, single column
"""
import os, re, sys, json, time
from pathlib import Path
import requests

API_BASE = "https://services.leadconnectorhq.com"
LOCATION_ID = "zPo4vLlEjjXCflgDSXlI"
NURTURE_DIR = Path("/Volumes/T7/SPG/3. FULFILLMENT/Clients/BIVIANO/Marketing/Nurture Sequences/Email - 8 Week Modular Lead")
FOLDER_NAME = "Nurture - Modular Lead 8 Week"

def load_env_key():
    env = Path("/Volumes/T7/SPG/Claude Code/.env").read_text()
    for line in env.splitlines():
        if line.startswith("BMB_GHL_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("BMB_GHL_API_KEY not found in .env")

API_KEY = load_env_key()
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Version": "2021-07-28",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "curl/8.7.1",  # avoid Cloudflare 1010 ban
}

def api(method, path, **kwargs):
    url = f"{API_BASE}{path}"
    r = requests.request(method, url, headers=HEADERS, timeout=30, **kwargs)
    if r.status_code >= 400:
        print(f"ERR {method} {path}: {r.status_code} {r.text[:400]}")
        r.raise_for_status()
    return r.json() if r.text else {}

def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, m.group(2).strip()

def md_to_html(body):
    """Minimal markdown -> HTML. Paragraphs, **bold**, bullet lists, [text](url) links."""
    # Split into blocks (paragraphs separated by blank lines)
    blocks = re.split(r"\n\s*\n", body.strip())
    html_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        # Bullet list
        if all(ln.lstrip().startswith("- ") for ln in block.splitlines() if ln.strip()):
            items = [ln.lstrip()[2:].strip() for ln in block.splitlines() if ln.strip()]
            lis = "".join(f"<li style=\"margin:0 0 8px 0;\">{inline(it)}</li>" for it in items)
            html_blocks.append(f"<ul style=\"margin:0 0 16px 0; padding-left:20px;\">{lis}</ul>")
            continue
        # Numbered list
        if all(re.match(r"^\d+\.\s", ln.strip()) for ln in block.splitlines() if ln.strip()):
            items = [re.sub(r"^\d+\.\s", "", ln.strip()) for ln in block.splitlines() if ln.strip()]
            lis = "".join(f"<li style=\"margin:0 0 8px 0;\">{inline(it)}</li>" for it in items)
            html_blocks.append(f"<ol style=\"margin:0 0 16px 0; padding-left:24px;\">{lis}</ol>")
            continue
        # Paragraph (preserve internal line breaks as <br>)
        para = inline(block).replace("\n", "<br>")
        html_blocks.append(f"<p style=\"margin:0 0 16px 0; font-size:16px; line-height:1.6;\">{para}</p>")
    return "\n".join(html_blocks)

def inline(s):
    # Bold
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    # [text](url) link  -- including our [Book a call → [[BOOK_CALL_URL]]] pattern, leave [[...]] alone
    s = re.sub(r"\[([^\]]+?)\]\(([^)]+)\)", r'<a href="\2" style="color:#4A90C4; text-decoration:underline;">\1</a>', s)
    return s

def wrap_email(html_body):
    """Wrap content in a clean single-column template."""
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0; padding:0; background:#f4f4f2; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif; color:#111110;">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#f4f4f2;">
<tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="max-width:600px; width:100%; background:#ffffff; border-radius:6px;">
<tr><td style="padding:32px 28px;">
{html_body}
</td></tr>
</table>
</td></tr>
</table>
</body></html>"""

def dig_id(res):
    """Best-effort id extraction from varied GHL response shapes."""
    if not isinstance(res, dict):
        return None
    for k in ("id", "_id", "templateId", "folderId"):
        if isinstance(res.get(k), str):
            return res[k]
    redirect = res.get("redirect")
    if isinstance(redirect, str):
        m = re.search(r"/([a-f0-9]{20,})(?:[/?]|$)", redirect)
        if m: return m.group(1)
    elif isinstance(redirect, dict):
        for k in ("id", "_id"):
            if redirect.get(k): return redirect[k]
    for k in ("data", "result", "folder", "template"):
        if isinstance(res.get(k), dict):
            sub = dig_id(res[k])
            if sub: return sub
    return None

def create_folder():
    print(f"\nCreating folder: {FOLDER_NAME}")
    res = api("POST", "/emails/builder", json={
        "locationId": LOCATION_ID,
        "title": FOLDER_NAME,
        "type": "folder",
        "templateType": "folder",
    })
    print(f"  full response: {json.dumps(res)[:400]}")
    fid = dig_id(res)
    print(f"  -> folder id: {fid}")
    return fid

def find_folder():
    """If folder already exists, find it."""
    res = api("GET", f"/emails/builder?locationId={LOCATION_ID}&limit=200")
    items = res.get("templates") or res.get("data") or res.get("items") or []
    for item in items:
        if item.get("type") == "folder" and item.get("title") == FOLDER_NAME:
            return item.get("id") or item.get("_id")
    return None

def create_email(parent_id, md_file):
    text = md_file.read_text()
    meta, body = parse_frontmatter(text)
    subject = meta.get("subject", md_file.stem)
    preview = meta.get("preview", "")
    # Title in GHL = filename order + subject for easy sorting
    title = f"{md_file.stem} — {subject}"
    html_body = md_to_html(body)
    full_html = wrap_email(html_body)

    print(f"\n  Creating: {title}")
    shell = api("POST", "/emails/builder", json={
        "locationId": LOCATION_ID,
        "title": title,
        "type": "html",
        "templateType": "html",
        "editorType": "html",
        "subject": subject,
        "previewText": preview,
        "parentId": parent_id,
    })
    tid = dig_id(shell)
    print(f"    shell id: {tid}")
    if not tid:
        print(f"    SHELL RESPONSE: {json.dumps(shell)[:400]}")
        return None

    # Step 2: save body
    data_res = api("POST", "/emails/builder/data", json={
        "locationId": LOCATION_ID,
        "templateId": tid,
        "editorType": "html",
        "html": full_html,
        "updatedBy": "api",
    })
    print(f"    body saved")
    time.sleep(0.4)
    return tid

def main():
    folder_id = find_folder()
    if folder_id:
        print(f"Folder already exists: {folder_id}")
    else:
        folder_id = create_folder()
    if not folder_id:
        sys.exit("Could not create or find folder")

    files = sorted(NURTURE_DIR.glob("[0-9][0-9]-*.md"))
    print(f"\nFound {len(files)} email files")
    created = []
    for f in files:
        tid = create_email(folder_id, f)
        created.append((f.name, tid))

    print("\n--- DONE ---")
    print(f"Folder: {FOLDER_NAME} ({folder_id})")
    for name, tid in created:
        print(f"  {name}: {tid}")

if __name__ == "__main__":
    main()

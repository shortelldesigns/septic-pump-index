#!/usr/bin/env python3
import html, json, re
from pathlib import Path
import pdfplumber

ROOT = Path('/workspace/septic-pump-index')
PDF = ROOT / 'data/sources/ia-dnr-licensed-septic-tank-cleaners-2026-08-19.pdf'
SOURCE_URL = 'https://www.iowadnr.gov/media/8587/download?inline='
PROGRAM_URL = 'https://www.iowadnr.gov/environmental-protection/water-quality/private-sewage-disposal-and-septage/septic-tank-cleaning'
DOC_DATE = '2026-08-19'
RETRIEVED = '2026-08-29'

def clean(s):
    if s is None:
        return ''
    return re.sub(r'\s+', ' ', str(s).replace('\n', ' ')).strip()

def fmt_phone(p):
    p = clean(p)
    if not p:
        return None
    digits = re.sub(r'\D', '', p)
    if len(digits) == 10:
        return f'({digits[0:3]}) {digits[3:6]}-{digits[6:]}'
    if len(digits) == 11 and digits.startswith('1'):
        return f'({digits[1:4]}) {digits[4:7]}-{digits[7:]}'
    return p

records = []
with pdfplumber.open(PDF) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables() or []
        if not tables:
            continue
        for row in tables[0]:
            if not row or clean(row[0]).lower() == 'license' or not clean(row[0]):
                continue
            lic = clean(row[0])
            if not lic.isdigit():
                continue
            name = clean(row[1])
            contact = clean(row[2]) or None
            email = clean(row[3]) or None
            address = clean(row[4]) or None
            city = clean(row[5]) or None
            state = clean(row[6]) or None
            zipc = clean(row[7]) or None
            county = clean(row[8]) or None
            phone_raw = clean(row[9]) or None
            phone = fmt_phone(phone_raw)
            full_addr = ', '.join(x for x in [address, city, state, zipc] if x)
            records.append({
                'license_number': lic,
                'source_url': SOURCE_URL,
                'source_document_date': DOC_DATE,
                'retrieved': RETRIEVED,
                'name': name,
                'role': 'licensed commercial septic tank cleaner (Iowa DNR)',
                'contact': contact if contact else 'unknown',
                'email': email if email else 'unknown',
                'address': full_addr if full_addr else 'unknown',
                'city': city if city else 'unknown',
                'state': state if state else 'unknown',
                'zip': zipc if zipc else 'unknown',
                'county': county if county else 'unknown',
                'phone': phone if phone else 'unknown',
                'phone_as_printed': phone_raw if phone_raw else 'unknown',
            })

print('records', len(records))
lics = [r['license_number'] for r in records]
print('unique licenses', len(set(lics)))
print('dup license nums', [x for x in set(lics) if lics.count(x) > 1])

payload = {
    'jurisdiction': 'Iowa (statewide)',
    'source': {
        'publisher': 'Iowa Department of Natural Resources',
        'title': 'Iowa DNR Licensed Septic Tank Cleaners (Pumpers)',
        'url': SOURCE_URL,
        'program_url': PROGRAM_URL,
        'document_date': DOC_DATE,
        'retrieved': RETRIEVED,
        'archive': 'data/sources/ia-dnr-licensed-septic-tank-cleaners-2026-08-19.pdf',
        'limitations': 'Transcribed from the Iowa DNR PDF titled Iowa DNR Licensed Septic Tank Cleaners (Pumpers), sorted by county. PDF metadata CreationDate Wed Aug 19 2026. A commercial septic tank cleaner license is not a Time of Transfer inspection credential. Appearance is not an endorsement.',
    },
    'record_count': len(records),
    'records': records,
}
out_json = ROOT / 'data/iowa-pumpers.json'
out_json.write_text(json.dumps(payload, indent=2) + '\n')
print('wrote', out_json)

def e(s):
    return html.escape(str(s), quote=True)

def phone_cell(r):
    p = r['phone']
    if p == 'unknown':
        return '<td class="unknown">unknown</td>'
    digits = re.sub(r'\D', '', r.get('phone_as_printed') or '')
    if len(digits) == 10:
        return f'<td class="phones"><a href="tel:+1{digits}">{e(p)}</a></td>'
    if len(digits) == 11 and digits.startswith('1'):
        return f'<td class="phones"><a href="tel:+{digits}">{e(p)}</a></td>'
    return f'<td class="phones">{e(p)}</td>'

def unk(val):
    if not val or val == 'unknown':
        return '<td class="unknown">unknown</td>'
    return f'<td>{e(val)}</td>'

rows_html = []
for r in records:
    rows_html.append(
        '<tr>'
        f'<td>{e(r["license_number"])}</td>'
        f'<td>{e(r["name"])}</td>'
        + unk(r['county'])
        + unk(r['city'] if r['city'] != 'unknown' else None)
        + unk(r['state'] if r['state'] != 'unknown' else None)
        + phone_cell(r)
        + '</tr>'
    )

nav = '''      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="states.html">States</a></li>
        <li><a href="how-often-to-pump.html">How often</a></li>
        <li><a href="inspection-before-sale.html">Before sale</a></li>
        <li><a href="warning-signs.html">Warning signs</a></li>
        <li><a href="about.html">About</a></li>
      </ul>'''

n = len(records)
page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Iowa Licensed Septic Pumpers | Septic Pump Index</title>
  <meta name="description" content="{n} Iowa DNR licensed commercial septic tank cleaners (pumpers) as of 19 August 2026. License number, county, city, and phone. A pumper license is not a Time of Transfer inspection.">
  <link rel="stylesheet" href="css/site.css">
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <header class="site">
    <div class="brand">
      <h1><a href="index.html">Septic Pump Index</a></h1>
      <p class="tag">A U.S. directory for septic tank owners. Pump on schedule. Inspect before you buy.</p>
    </div>
    <nav class="primary" aria-label="Primary">
{nav}
    </nav>
  </header>
  <main id="content" class="wide">
    <h1 class="page">Iowa licensed commercial septic tank cleaners (pumpers)</h1>
    <p class="lede">Transcribed from Iowa Department of Natural Resources, <cite>Iowa DNR Licensed Septic Tank Cleaners (Pumpers)</cite>, sorted by county. We did not add companies from business directories.</p>
    <p class="meta">Official file retrieved 29 August 2026: <a href="{e(SOURCE_URL)}">Licensed Iowa Septic Tank Cleaners PDF</a> (Iowa DNR media id 8587). PDF metadata CreationDate 19 August 2026 (UTC). Program page: <a href="{e(PROGRAM_URL)}">Septic Tank Cleaning</a>. Iowa Administrative Code 567 Chapter 68.</p>

    <div class="callout">
      <h2>How to read this table</h2>
      <p>Iowa requires septic tanks to be pumped only by a licensed commercial septic tank cleaner. The PDF columns include license number, business name, contact, email, address, city, state, ZIP, county, and phone. This page shows license, business, county, city, state, and phone. Contact and email are in the machine-readable JSON only.</p>
      <p>Counties labeled “(OUT OF STATE)” on the PDF mean the firm’s street address is outside Iowa while the county column names the Iowa county of record. Phone digits are shown as on the PDF (normalized to parentheses where ten digits were present); no digits were invented.</p>
      <p>A commercial septic tank cleaner license is not a Time of Transfer inspection credential. Iowa’s sale-related septic inspections use a separate DNR certification. <a href="inspection-before-sale.html">Inspection before sale</a> · <a href="how-often-to-pump.html">How often to pump</a>.</p>
    </div>

    <div class="table-wrap"><table>
      <caption>{n} licensed cleaners from Iowa DNR, PDF dated 19 August 2026</caption>
      <thead><tr><th>License</th><th>Business</th><th>County</th><th>City</th><th>State</th><th>Phone</th></tr></thead>
      <tbody>
{chr(10).join(rows_html)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="data/iowa-pumpers.json">data/iowa-pumpers.json</a>. Archived PDF: <a href="data/sources/ia-dnr-licensed-septic-tank-cleaners-2026-08-19.pdf">data/sources/ia-dnr-licensed-septic-tank-cleaners-2026-08-19.pdf</a>.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 29 August 2026 (US/Pacific).</p>
      <p><a href="about.html">Methodology and disclosure</a> · <a href="states.html">State directory</a></p>
      <div class="disclaimer">
        <p>This site is not a government agency and does not license pumpers or inspectors. Listings are transcribed from official state or county sources cited on each page. Registration, phones, and who may work in a county change. Confirm with the company and the licensing authority before you hire.</p>
        <p>This site is educational, not legal, engineering, or real-estate advice. We may earn a commission on future product or service links; there are no live affiliate links and no paid placements on this version.</p>
      </div>
    </div>
  </footer>
</body>
</html>
'''
(ROOT / 'iowa.html').write_text(page)
print('wrote iowa.html', len(page), 'bytes')
for r in records:
    d = re.sub(r'\D', '', r.get('phone_as_printed') or '')
    if d and len(d) not in (10, 11):
        print('odd phone', r['license_number'], r['name'], r['phone_as_printed'])

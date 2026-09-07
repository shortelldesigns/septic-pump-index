#!/usr/bin/env python3
"""Build Johnson County KS licensed sanitary disposal contractors (sewage) JSON + HTML."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = (
    'https://www.jocogov.org/sites/default/files/files/2026-08/'
    '2026%20Licensed%20Sanitary%20Disposal%20Contractors%20Lists.pdf'
)
PARENT_URL = 'https://www.jocogov.org/department/environment/septic-systems/pumper-installer-lists'
LICENSING_URL = (
    'https://www.jocogov.org/department/environment/septic-systems/contractor-installer-licensing'
)
DOC_DATE = '2026-06-24'
RETRIEVED = '2026-09-06'
ARCHIVE = 'data/sources/johnson-ks-licensed-sanitary-disposal-contractors-2026.pdf'
ARCHIVE_TXT = 'data/sources/johnson-ks-licensed-sanitary-disposal-contractors-2026.txt'

# Hand-verified from pdftotext -layout of 2026 Licensed Sanitary Disposal Contractors Lists
# (footer: updated 6/24/2026 2:06 PM; PDF CreationDate 25 Aug 2026).
# ONLY the "for Sewage" section — grease-only and portable-toilet-only rows excluded.
# Do not invent addresses or fields not on the PDF. Curly apostrophe in Bill’s kept as printed.
RECORDS = [
    {'license': '26-003', 'name': 'A-1 Sewer & Septic Service Inc.', 'phone': '(913) 631-5201'},
    {'license': '26-025', 'name': 'Bill’s Septic Service', 'phone': '(913) 755-4082'},
    {'license': '26-006', 'name': 'Chapman Septic Services', 'phone': '(913) 287-2280'},
    {'license': '26-017', 'name': 'Crosby Plumbing', 'phone': '(913) 441-5800'},
    {'license': '26-007', 'name': 'Dailey Septic Service', 'phone': '(913) 856-7550'},
    {'license': '26-030', 'name': 'Dump N Pump Septic LLC', 'phone': '(816) 368-2903'},
    {'license': '26-035', 'name': 'Epic Septic of SW KC', 'phone': '(913) 392-5200'},
    {'license': '26-001', 'name': 'EnviroServe', 'phone': '(800) 488-0910'},
    {'license': '26-018', 'name': 'Honey-Wagon Septic & Grease', 'phone': '(913) 681-3563'},
    {'license': '26-034', 'name': 'Honeybee Septic', 'phone': '(785) 841-0399'},
    {'license': '26-009', 'name': 'K Jett Services, LLC', 'phone': '(816) 769-3900'},
    {'license': '26-019', 'name': 'Kissick Construction Company', 'phone': '(816) 363-5530'},
    {'license': '26-020', 'name': 'Koontz Septic Service', 'phone': '(913) 269-0284'},
    {'license': '26-010', 'name': 'Lexington Plumbing', 'phone': '(816) 231-2254'},
    {'license': '26-011', 'name': 'Missouri Drain & Sewer LLC DBA Zoom Drain', 'phone': '(816) 357-5918'},
    {'license': '26-031', 'name': 'Pipeview America', 'phone': '(913) 605-0057'},
    {'license': '26-033', 'name': 'Quality Plumbing', 'phone': '(816) 472-4994'},
    {'license': '26-012', 'name': 'Reddi Services, Inc.', 'phone': '(913) 287-5005'},
    {'license': '26-024', 'name': 'Septic Kings', 'phone': '(816) 816-7667'},
    {'license': '26-022', 'name': 'Solid Ground Excavating LLC', 'phone': '(913) 608-3361'},
    {'license': '26-028', 'name': 'Stahla Services LLC', 'phone': '(844) 900-3190'},
    {'license': '26-027', 'name': 'Sunflower Septic LLC', 'phone': '(913) 443-8628'},
    {'license': '26-013', 'name': 'Truninger Brothers Septic Tank Pumping', 'phone': '(816) 540-5673'},
    {'license': '26-014', 'name': 'Twin Springs Pump Services LLC', 'phone': '(816) 839-7867'},
    {'license': '26-015', 'name': 'Wheatland Contracting LLC', 'phone': '(913) 833-2304'},
]


def e(s):
    return html.escape(str(s), quote=True)


def phone_digits(s):
    return re.sub(r'\D', '', s or '')


def phone_cell(printed):
    digits = phone_digits(printed)
    if not digits:
        return '<td class="unknown">unknown</td>'
    pretty = printed
    return f'<td class="phones"><a href="tel:+1{digits}">{e(pretty)}</a></td>'


def main():
    assert len(RECORDS) == 25, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert '2026 Licensed Sanitary Disposal Contractors for Sewage' in txt
    assert 'updated 6/24/2026' in txt
    for r in RECORDS:
        assert r['license'] in txt, r['license']
        # ASCII-fold curly apostrophe for Bill’s when matching PDF text already has it
        assert r['name'] in txt or r['name'].replace("'", "’") in txt or r['name'].replace("’", "'") in txt, r['name']
        assert r['phone'] in txt, r['phone']
    # Grease-only / portable-only must not appear as sewage rows we claim
    assert 'Brooks Grease Service' in txt  # grease section exists
    assert 'American Waste Systems' in txt  # portable section exists

    records = []
    for r in RECORDS:
        records.append({
            'license_number': r['license'],
            'name': r['name'],
            'phone': r['phone'],
            'phone_digits': phone_digits(r['phone']),
            'category': 'Sewage',
            'role': 'Johnson County KS licensed sanitary disposal contractor (sewage)',
            'source_url': SOURCE_URL,
            'source_document_date': DOC_DATE,
            'retrieved': RETRIEVED,
        })

    payload = {
        'jurisdiction': 'Johnson County, Kansas',
        'source': {
            'publisher': 'Johnson County Department of Health and Environment',
            'title': '2026 Licensed Sanitary Disposal Contractors Lists',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'licensing_url': LICENSING_URL,
            'document_date': DOC_DATE,
            'document_date_as_printed': 'updated 6/24/2026 2:06 PM',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from the Sewage section only of the JCDHE PDF updated 6/24/2026. '
                'Grease-only and portable-toilet-only licensees are not listed here. '
                'Addresses are not on the PDF. Appearance is not an endorsement. '
                'Confirm current licensure on the county website before you hire. '
                'A sanitary disposal contractor license is not an inspection credential.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-johnson-ks.json'
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        rows.append(
            '<tr>'
            f'<td>{e(r["license_number"])}</td>'
            f'<td>{e(r["name"])}</td>'
            + phone_cell(r['phone'])
            + '</tr>'
        )

    n = len(records)
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Johnson County KS Septic Pumpers | Septic Pump Index</title>
  <meta name="description" content="{n} Johnson County, Kansas licensed sanitary disposal contractors (sewage) from the JCDHE 2026 PDF updated 24 June 2026. Pumping is not an inspection.">
  <link rel="stylesheet" href="../css/site.css">
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <header class="site">
    <div class="brand">
      <h1><a href="../index.html">Septic Pump Index</a></h1>
      <p class="tag">A U.S. directory for septic tank owners. Pump on schedule. Inspect before you buy.</p>
    </div>
    <nav class="primary" aria-label="Primary">
      <ul>
        <li><a href="../index.html">Home</a></li>
        <li><a href="../states.html">States</a></li>
        <li><a href="../how-often-to-pump.html">How often</a></li>
        <li><a href="../inspection-before-sale.html">Before sale</a></li>
        <li><a href="../warning-signs.html">Warning signs</a></li>
        <li><a href="../about.html">About</a></li>
      </ul>
    </nav>
  </header>
  <main id="content" class="wide">
    <h1 class="page">Johnson County, Kansas — licensed sanitary disposal contractors (sewage)</h1>
    <p class="lede">Transcribed from Johnson County Department of Health and Environment’s PDF <cite>2026 Licensed Sanitary Disposal Contractors Lists</cite>, footer updated 24 June 2026. We list only the <strong>Sewage</strong> section — firms licensed to pump private sewage treatment systems. Grease-only and portable-toilet-only licensees are omitted. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 6 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">2026 Licensed Sanitary Disposal Contractors Lists.pdf</a>. Parent page: <a href="{e(PARENT_URL)}">Pumper Installer Lists</a>. Licensing: <a href="{e(LICENSING_URL)}">Contractor Installer Licensing</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>JCDHE licenses sanitary disposal contractors (pumpers) annually under the Johnson County Environmental Sanitary Code. License numbers and phones are as printed. Addresses are not on this PDF.</p>
      <p>The same PDF has separate Grease and Portable Toilets sections. Those are different scopes of work. This page is for homeowners who need a sewage tank pumped.</p>
      <p>A sanitary disposal contractor license is not a septic inspection credential. The county also publishes a separate licensed-installers PDF. Pumping a tank is not a full inspection. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a>.</p>
      <p>The PDF itself says: prior to using any contractor, go to the county website to ensure current licensure.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} licensed sanitary disposal contractors for sewage from JCDHE PDF updated 24 June 2026</caption>
      <thead><tr><th>License</th><th>Company</th><th>Phone</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-johnson-ks.json">data/haulers-johnson-ks.json</a>. Archived PDF: <a href="../data/sources/{e(Path(ARCHIVE).name)}">data/sources/{e(Path(ARCHIVE).name)}</a>. Names, license numbers, and phones are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 6 September 2026 (US/Pacific).</p>
      <p><a href="../about.html">Methodology and disclosure</a> · <a href="../states.html">State directory</a></p>
      <div class="disclaimer">
        <p>This site is not a government agency and does not license pumpers or inspectors. Listings are transcribed from official state or county sources cited on each page. Registration, phones, and who may work in a county change. Confirm with the company and the licensing authority before you hire.</p>
        <p>This site is educational, not legal, engineering, or real-estate advice. We may earn a commission on future product or service links; there are no live affiliate links and no paid placements on this version.</p>
      </div>
    </div>
  </footer>
</body>
</html>
'''
    out_html = ROOT / 'ks/johnson.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

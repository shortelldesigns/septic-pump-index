#!/usr/bin/env python3
"""Build Conestoga Township (Lancaster County PA) approved septic haulers JSON + HTML."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://conestogatwp.com/wp-content/uploads/2026/08/2026-Approved-Septic-Haulers-06.2026.pdf'
PARENT_URL = 'https://conestogatwp.com/sewage/'
DEP_URL = 'https://www.pa.gov/services/dep/water/clean-water/register-a-residential-septage-hauler'
DOC_DATE = '2026-06'
RETRIEVED = '2026-10-01'
ARCHIVE = 'data/sources/conestoga-twp-lancaster-pa-approved-septic-haulers-2026-06.pdf'
ARCHIVE_TXT = 'data/sources/conestoga-twp-lancaster-pa-approved-septic-haulers-2026-06.txt'

# Hand-verified from pdftotext -layout of 2026-Approved-Septic-Haulers-06.2026.pdf
# (Conestoga Township, Lancaster County, PA; linked from Sewage page as
# "2026 Approved Septic Haulers 06.2026"). Spellings kept as printed
# (DAVIS, WILLIAM & SONS SEPTIC; KAUFFMAN'S; W. Girl Scout Road; Unit #4).
# Emails exist on the PDF but are not shown in the public table (matches other PA pages).
# PETERS email line prints "None Available - Please Call" — phone only recorded.
RECORDS = [
    {
        'name': 'DAVIS, WILLIAM & SONS SEPTIC',
        'address': '341 Snyder Hollow Road, New Providence, PA 17560',
        'phone_as_printed': '717-284-3688',
    },
    {
        'name': 'DEVONSHIRE SEPTIC LLC',
        'address': '289 Camargo Road, Quarryville, PA 17566',
        'phone_as_printed': '717-786-1998',
    },
    {
        'name': 'FINS ENVIRONMENTAL SERVICES LLC',
        'address': '691 Truce Road, Quarryville, PA 17566',
        'phone_as_printed': '717-284-5228',
    },
    {
        'name': 'FRANK SEARS SANITATION LLC',
        'address': '509 Lime Quarry Road, Gap, PA 17527',
        'phone_as_printed': '717-442-8609',
    },
    {
        'name': 'JOHN KLINE SEPTIC',
        'address': '3869 Old Harrisburg Pike, Mount Joy, PA 17552',
        'phone_as_printed': '717-898-2333',
    },
    {
        'name': "KAUFFMAN'S SEPTIC SERVICES LLC",
        'address': '236 Governor Stable Road, Bainbridge, PA 17502',
        'phone_as_printed': '717-367-8228',
    },
    {
        'name': 'MARKS SEPTIC SERVICE INC',
        'address': '81 Horseshoe Lane, Shillington, PA 19607',
        'phone_as_printed': '610-913-0707',
    },
    {
        'name': 'PETERS SEPTIC TANK PUMPING',
        'address': '117 Keys Road, Peach Bottom, PA 17563',
        'phone_as_printed': '717-786-1454',
    },
    {
        'name': 'SEPTIC SOLUTIONS',
        'address': '310 Tick Hill Road, Kirkwood, PA 17536',
        'phone_as_printed': '717-529-0931',
    },
    {
        'name': 'SHARP SEPTIC LLC',
        'address': '85 Esbenshade Road, Ronks, PA 17572',
        'phone_as_printed': '717-354-6147',
    },
    {
        'name': 'SNYDER & MYLIN SEPTIC SERVICES LLC',
        'address': '1130 Lancaster Pike, Drumore, PA 17518',
        'phone_as_printed': '717-284-0303',
    },
    {
        'name': 'SONLIGHT SERVICES LLC',
        'address': '225 Wood Corner Road Unit #4, Lititz, PA 17543',
        'phone_as_printed': '717-738-2149',
    },
    {
        'name': 'THOMAS ERB & SONS INC',
        'address': '268 Sego Sago Road, Lititz, PA 17543',
        'phone_as_printed': '717-626-5591',
    },
    {
        'name': 'WALTERS ENVIRONMENTAL SERVICES INC',
        'address': '9554 Allentown Blvd, Grantville, PA 17028',
        'phone_as_printed': '717-469-0588',
    },
    {
        'name': 'WEAVER SEPTIC SERVICES LLC',
        'address': '670 W. Girl Scout Road, Stevens, PA 17578',
        'phone_as_printed': '717-733-2339',
    },
    {
        'name': 'WIND RIVER ENVIRONMENTAL LLC',
        'address': '5 Holland Street, Salunga, PA 17538',
        'phone_as_printed': '717-415-5649',
    },
]


def fmt_phone(p):
    p = (p or '').strip()
    if not p:
        return 'unknown'
    digits = re.sub(r'\D', '', p)
    if len(digits) == 10:
        return f'({digits[0:3]}) {digits[3:6]}-{digits[6:]}'
    if len(digits) == 11 and digits.startswith('1'):
        return f'({digits[1:4]}) {digits[4:7]}-{digits[7:]}'
    return p


def e(s):
    return html.escape(str(s), quote=True)


def phone_cell(r):
    p = r['phone']
    raw = r.get('phone_as_printed') or ''
    digits = re.sub(r'\D', '', raw)
    if len(digits) == 10:
        return f'<td class="phones"><a href="tel:+1{digits}">{e(p)}</a></td>'
    if len(digits) == 11 and digits.startswith('1'):
        return f'<td class="phones"><a href="tel:+{digits}">{e(p)}</a></td>'
    if p == 'unknown':
        return '<td class="phones unknown">unknown</td>'
    return f'<td class="phones">{e(p)}</td>'


def main():
    assert len(RECORDS) == 16, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert 'Approved Septic Haulers 2026' in txt
    assert 'DAVIS, WILLIAM & SONS SEPTIC' in txt
    assert 'MARKS SEPTIC SERVICE INC' in txt
    assert 'SONLIGHT SERVICES LLC' in txt
    assert 'WIND RIVER ENVIRONMENTAL LLC' in txt
    assert "KAUFFMAN'S SEPTIC SERVICES LLC" in txt
    assert 'SNYDER & MYLIN SEPTIC SERVICES LLC' in txt
    assert 'W. Girl Scout Road' in txt
    assert '225 Wood Corner Road Unit #4' in txt
    for r in RECORDS:
        assert r['name'] in txt, r['name']
        street = r['address'].split(',')[0].split()[0]
        assert street in txt, r['address']
        assert r['phone_as_printed'] in txt, r['phone_as_printed']

    keys = [(r['name'], r['address']) for r in RECORDS]
    assert len(keys) == len(set(keys)), 'duplicate name+address'

    records = []
    for r in RECORDS:
        phone = fmt_phone(r['phone_as_printed'])
        records.append({
            'license_number': 'unknown',
            'source_url': SOURCE_URL,
            'source_document_date': DOC_DATE,
            'retrieved': RETRIEVED,
            'name': r['name'],
            'role': 'Conestoga Township approved septic hauler',
            'address': r['address'],
            'phone': phone,
            'phone_as_printed': r['phone_as_printed'] or None,
            'pa_dep_transporter_number': 'unknown',
        })

    payload = {
        'jurisdiction': 'Conestoga Township, Lancaster County, Pennsylvania',
        'source': {
            'publisher': 'Conestoga Township',
            'title': 'Approved Septic Haulers 2026 (06.2026)',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'dep_verify_url': DEP_URL,
            'document_date': DOC_DATE,
            'document_date_note': (
                'Parent Sewage page link text is “2026 Approved Septic Haulers 06.2026”; '
                'PDF path is under /wp-content/uploads/2026/08/; title line prints '
                'Approved Septic Haulers 2026. This is Conestoga Township’s approved list '
                '(Lancaster County), not a countywide Lancaster County Health Department roster.'
            ),
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'archive_txt': ARCHIVE_TXT,
            'limitations': (
                'Transcribed from Conestoga Township PDF 2026-Approved-Septic-Haulers-06.2026.pdf '
                '(linked from https://conestogatwp.com/sewage/ as 2026 Approved Septic Haulers 06.2026). '
                '16 named haulers. Spellings kept as printed including DAVIS, WILLIAM & SONS SEPTIC, '
                "KAUFFMAN'S SEPTIC SERVICES LLC, W. Girl Scout Road, and 225 Wood Corner Road Unit #4. "
                'Emails appear on the PDF but are omitted from this table (other Septic Pump Index PA pages '
                'do not publish emails). PETERS SEPTIC TANK PUMPING email line prints '
                '“None Available - Please Call” — phone only. Pennsylvania DEP 5-digit transporter '
                'numbers are not printed on this PDF (marked unknown). This is a township-approved '
                'hauler list for Conestoga Township in Lancaster County — not a full county roster. '
                'Pumping is not an inspection. Appearance is not an endorsement. Verify with '
                'Conestoga Township / its Sewage Enforcement Officer and PA DEP before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-lancaster-pa.json'
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        rows.append(
            '<tr>'
            f'<td>{e(r["name"])}</td>'
            f'<td>{e(r["address"])}</td>'
            + phone_cell(r)
            + '<td class="unknown">unknown</td>'
            + '</tr>'
        )

    n = len(records)
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Conestoga Township (Lancaster County) PA Septic Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Conestoga Township, Lancaster County, Pennsylvania approved septic haulers from the township PDF dated June 2026. DEP transporter numbers marked unknown. Pumping is not an inspection.">
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
    <h1 class="page">Conestoga Township, Lancaster County, Pennsylvania — approved septic haulers</h1>
    <p class="lede">Transcribed from Conestoga Township’s PDF <cite>Approved Septic Haulers 2026</cite> (file <code>2026-Approved-Septic-Haulers-06.2026.pdf</code>). This is the township’s approved septic-hauler list for Conestoga Township in Lancaster County. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 1 October 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">2026-Approved-Septic-Haulers-06.2026.pdf</a>. Parent: <a href="{e(PARENT_URL)}">Sewage Enforcement Officer — Conestoga Township</a>. Pennsylvania DEP issues a 5-digit transporter number; those numbers are <strong>not</strong> printed on this township list.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Conestoga Township (Lancaster County) publishes an approved septic haulers roster. The Sewage page links this file as <strong>2026 Approved Septic Haulers 06.2026</strong>. This is <strong>not</strong> a countywide Lancaster County Health Department roster — only the township’s approved list. DEP 5-digit transporter numbers are not on this PDF — marked <strong>unknown</strong>. Confirm on <a href="{e(DEP_URL)}">PA DEP’s residential septage hauler registration page</a>.</p>
      <p>Spellings are as printed (including <code>DAVIS, WILLIAM &amp; SONS SEPTIC</code>, <code>KAUFFMAN'S SEPTIC SERVICES LLC</code>, <code>W. Girl Scout Road</code>, and <code>225 Wood Corner Road Unit #4</code>). Emails appear on the PDF but are omitted here. The township notes DEP requires septic systems to be inspected / pumped once every 3 years — that is a DEP/municipal rule, not an endorsement of any firm.</p>
      <p>Pumping is not a real-estate inspection or a drainfield repair. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="york.html">York County PA haulers</a> · <a href="chester.html">Chester County PA pumpers</a>.</p>
    </div>
    <div class="table-wrap"><table class="hauler-table">
      <caption>{n} approved septic haulers from Conestoga Township (Lancaster County), PDF 06.2026</caption>
      <thead><tr><th>Business</th><th>Address</th><th>Phone</th><th>DEP transporter no.</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-lancaster-pa.json">data/haulers-lancaster-pa.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, phones, and addresses are as printed on the township PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 1 October 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'pa/lancaster.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

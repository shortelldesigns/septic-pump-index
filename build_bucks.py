#!/usr/bin/env python3
"""Build Bucks County PA approved sewage hauler JSON + HTML from BCHD PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://www.buckscounty.gov/DocumentCenter/View/16662/Approved-Sewage-Hauler-List-2024-2025'
PARENT_URL = 'https://www.buckscounty.gov/1122/Sewage-Hauler-Vehicles'
SEWAGE_PROGRAM_URL = 'https://www.buckscounty.gov/363/Sewage-Program'
DEP_URL = 'https://www.pa.gov/services/dep/water/clean-water/register-a-residential-septage-hauler'
DOC_DATE = '2025-07-07'
RETRIEVED = '2026-09-03'
ARCHIVE = 'data/sources/bucks-pa-approved-sewage-haulers-2025-07-07.pdf'
ARCHIVE_TXT = 'data/sources/bucks-pa-approved-sewage-haulers-2025-07-07.txt'

# Hand-transcribed from pdftotext of Approved-Sewage-Hauler-List-2024-2025
# (Revised 7/07/2025). 42 named firms. DEP transporter numbers not on PDF.
# Three Waste Management location rows have no phone. Pennsburg ZIP printed
# as 1807 — do not invent digits. Franc Environmental phone line prints
# "215-443-0650 / Wind River" — phone only; Wind River noted in limitations.
# Multiple Waste Management rows with different addresses are separate records.
RECORDS = [
    {
        'name': 'ARF Rental Services',
        'address': '3268 S. 61st Street, Philadelphia, PA 19153',
        'phone_as_printed': '1-800-234-6545',
    },
    {
        'name': 'Allstate Septic Systems',
        'address': '5167 Berry Hollow Road, Bangor, PA 18013',
        'phone_as_printed': '610-498-3111',
    },
    {
        'name': 'B&C Septic Service Inc.',
        'address': '305 Three Mile Run Road, Sellersville, PA 18960',
        'phone_as_printed': '215-257-8544',
    },
    {
        'name': 'Bob Drayton, Inc.',
        'address': '151 Big Hill Road, Southampton, NJ 08088',
        'phone_as_printed': '609-859-3629',
    },
    {
        'name': 'Brad S. Nicholas',
        'address': '25 Brandon Way, Kintnersville, PA 18930',
        'phone_as_printed': '610-847-2555',
    },
    {
        'name': 'Bucks County Water & Sewer Authority',
        'address': '1275 Almshouse Road, Warrington, PA 18976',
        'phone_as_printed': '215-343-2538',
    },
    {
        'name': 'Camerlengo Septic Services',
        'address': '1069 Old School Rd, Quakertown, PA 18951',
        'phone_as_printed': '267-424-5784',
    },
    {
        'name': 'Chalfont - New Britain Sewage Authority',
        'address': '1645 Upper State Road, Doylestown, PA 18901',
        'phone_as_printed': '215-345-1225',
    },
    {
        'name': "Christman's Septic Service",
        'address': 'PO Box 714, Fogelsville, PA 18051',
        'phone_as_printed': '610-285-2563',
    },
    {
        'name': 'Clemens Septic Service',
        'address': '673 Keller Creamery Road, Telford, PA 18969',
        'phone_as_printed': '215-723-2122',
    },
    {
        'name': 'Cobra Environmental Inc.',
        'address': '1113 Edgley Road, Bristol, PA 19007',
        'phone_as_printed': '267-421-3924',
    },
    {
        'name': 'Delaware Valley Septic',
        'address': '504 Eagle Rd, Suite B, Springfield, PA 19064',
        'phone_as_printed': '610-947-4800',
    },
    {
        'name': 'Denali Water Solutions (Jesse Baro)',
        'address': '157 Quarry Road, Douglassville, PA 19518',
        'phone_as_printed': '610-323-8783',
    },
    {
        'name': 'Franc Environmental Inc.',
        'address': '960 Jacksonville Road, Ivyland, PA 18974',
        'phone_as_printed': '215-443-0650',
    },
    {
        'name': "Gary's Septic Service, Inc.",
        'address': 'PO Box 333, Pipersville, PA 18947',
        'phone_as_printed': '215-766-1913',
    },
    {
        'name': 'George Allen Wastewater Mgmt.',
        'address': '4375 County Line Road, Chalfont, PA 18914',
        'phone_as_printed': '215-997-3299',
    },
    {
        'name': 'J.H. Freed, Inc.',
        'address': '115 Allentown Road, Souderton, PA 18964',
        'phone_as_printed': '215-723-2426',
    },
    {
        'name': 'L & C Septic Pumping LLC',
        'address': '2659 Geryville Pike, Pennsburg, PA 1807',
        'phone_as_printed': '267-374-4366',
    },
    {
        'name': 'Lukens Septic Service',
        'address': '2412 Hill Road, Sellersville, PA 18960',
        'phone_as_printed': '215-453-1010',
    },
    {
        'name': "Manny’s Septic Service",
        'address': '46 Ashley Court, Downingtown, PA 19335',
        'phone_as_printed': '610-755-2639',
    },
    {
        'name': 'Mark Robbins',
        'address': '3008 Hauck Road, Green Lane, PA 18054',
        'phone_as_printed': '215-234-8314',
    },
    {
        'name': 'McGovern Environmental, LLC',
        'address': '920 South Bolmar Street, West Chester, PA 19382',
        'phone_as_printed': '610-444-5797',
    },
    {
        'name': 'Norbill Disposal Service',
        'address': '5610 Haring Road, Doylestown, PA 18902',
        'phone_as_printed': '215-348-2123',
    },
    {
        'name': 'On Site Management Inc.',
        'address': '1109 Saunders Court, West Chester, PA 19380',
        'phone_as_printed': '610-430-3100',
    },
    {
        'name': 'Piedmont Environmental',
        'address': '82 Cheesefactory Rd, Doylestown, PA 18901',
        'phone_as_printed': '215-360-7478',
    },
    {
        'name': 'Port A Bowl Restroom Co., Inc.',
        'address': 'PO Box 571, Plumsteadville, PA 18949',
        'phone_as_printed': '215-766-8164',
    },
    {
        'name': 'Preston Heckler Liquid Disposal LLC',
        'address': '628 Rustic Drive, Perkasie, PA 18944',
        'phone_as_printed': '215-855-2946',
    },
    {
        'name': 'Richard R. Schmick, Inc.',
        'address': '122 Cedar Street, Macungie, PA 18036',
        'phone_as_printed': '610-797-0630',
    },
    {
        'name': 'River Valley Septic',
        'address': 'P.O. Box 725, Riegelsville, PA 18077',
        'phone_as_printed': '610-749-2001',
    },
    {
        'name': 'Royal Throne Portable Toilets',
        'address': '733 E. Washington Street, Allentown, PA 18109',
        'phone_as_printed': '610-770-1840',
    },
    {
        'name': 'Russell Reid Waste Hauling (United Site Services)',
        'address': '200 Smith Street, Keasbey, NJ 08832',
        'phone_as_printed': '732-692-2440',
    },
    {
        'name': "Stinky's LLC",
        'address': '462 A Route 31, Lambertville, NJ 08530',
        'phone_as_printed': '609-466-5422',
    },
    {
        'name': 'Synagro of Texas CDR, Inc.',
        'address': '435 Williams Court, Suite 100, Baltimore, MD 21220',
        'phone_as_printed': '443-489-9013',
    },
    {
        'name': 'Waste Management',
        'address': '1121 Bordentown Road, Morrisville, PA 19067',
        'phone_as_printed': '',
    },
    {
        'name': 'Waste Management',
        'address': '408 S Oak Ave, Primos, PA 19018',
        'phone_as_printed': '',
    },
    {
        'name': 'Waste Management',
        'address': '200 Bordentown Road, Tullytown, PA 19007',
        'phone_as_printed': '',
    },
    {
        'name': 'Waste Management',
        'address': '400 Progress Drive, Telford, PA 18969',
        'phone_as_printed': '215-453-2431',
    },
    {
        'name': 'Waste Management of PA',
        'address': '107 Silva Street, Ewing, NJ 08628',
        'phone_as_printed': '215-823-0568',
    },
    {
        'name': 'Waste Management of PA, Inc.',
        'address': '1224 Hayes Blvd, Bristol, PA 19007',
        'phone_as_printed': '215-458-9204',
    },
    {
        'name': 'Waste Masters Solutions',
        'address': '19 Davidson Lane, New Castle, DE 19720',
        'phone_as_printed': '302-824-0909',
    },
    {
        'name': 'Winding Creek Septic Services, LLC',
        'address': '2215 Keiper Road, Quakertown, PA 18951',
        'phone_as_printed': '215-237-0552',
    },
    {
        'name': 'Zoom Drain',
        'address': '500 Davis Drive, Plymouth Meeting, PA 19462',
        'phone_as_printed': '610-650-0555',
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
    assert len(RECORDS) == 42, len(RECORDS)
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
            'role': 'Bucks County Health Department approved sewage hauler',
            'address': r['address'],
            'phone': phone,
            'phone_as_printed': r['phone_as_printed'] or None,
            'pa_dep_transporter_number': 'unknown',
        })

    payload = {
        'jurisdiction': 'Bucks County, Pennsylvania',
        'source': {
            'publisher': 'Bucks County Health Department',
            'title': 'APPROVED SEWAGE HAULERS LIST 2024-2025 (Revised 7/07/2025)',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'sewage_program_url': SEWAGE_PROGRAM_URL,
            'dep_verify_url': DEP_URL,
            'document_date': DOC_DATE,
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'archive_txt': ARCHIVE_TXT,
            'limitations': (
                'Transcribed from Bucks County Health Department PDF '
                'Approved-Sewage-Hauler-List-2024-2025 (Revised 7/07/2025). '
                'BCHD licenses sewage hauler vehicles annually; this is the approved '
                'sewage haulers list for 2024-2025. Pennsylvania DEP 5-digit transporter '
                'numbers are not printed on this PDF (marked unknown). Three Waste '
                'Management location rows (Morrisville, Primos, Tullytown) have no phone '
                'printed (marked unknown). Franc Environmental Inc. phone line prints '
                '“215-443-0650 / Wind River” — phone recorded as 215-443-0650; Wind River '
                'is an annotation on the PDF, not a second phone. L & C Septic Pumping LLC '
                'ZIP is printed as 1807 (truncated; not expanded). Multiple Waste Management '
                'rows with different addresses are separate records as printed. Pumping is '
                'not an inspection. Appearance is not an endorsement. Verify with BCHD and '
                'PA DEP before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-bucks-pa.json'
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
  <title>Bucks County PA Septic Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Bucks County, Pennsylvania approved sewage haulers from Bucks County Health Department PDF revised 7 July 2025. DEP transporter numbers marked unknown. Pumping is not an inspection.">
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
    <h1 class="page">Bucks County, Pennsylvania — approved sewage haulers</h1>
    <p class="lede">Transcribed from Bucks County Health Department’s PDF <cite>APPROVED SEWAGE HAULERS LIST 2024-2025 (Revised 7/07/2025)</cite>. Bucks County Health Department licenses sewage hauler vehicles annually. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 3 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">Approved-Sewage-Hauler-List-2024-2025</a>. Parent: <a href="{e(PARENT_URL)}">Sewage Hauler Vehicles</a>. Program: <a href="{e(SEWAGE_PROGRAM_URL)}">Sewage Program</a>. Pennsylvania DEP issues a 5-digit transporter number; those numbers are <strong>not</strong> printed on this county list.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Bucks County Health Department licenses sewage hauler vehicles annually; this list is the approved sewage haulers roster for 2024–2025, revised 7 July 2025. DEP 5-digit transporter numbers are not on this PDF — marked <strong>unknown</strong>. Confirm on <a href="{e(DEP_URL)}">PA DEP’s residential septage hauler registration page</a>.</p>
      <p>Three Waste Management location rows (Morrisville, Primos, Tullytown) have no phone printed — marked unknown. Franc Environmental Inc. prints “215-443-0650 / Wind River”; we record the phone only. L &amp; C Septic Pumping LLC ZIP is printed as <code>1807</code> (truncated; not expanded). Multiple Waste Management rows with different addresses are separate records as printed.</p>
      <p>Pumping is not a real-estate inspection or a drainfield repair. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="york.html">York County PA haulers</a>.</p>
    </div>
    <div class="table-wrap"><table class="hauler-table">
      <caption>{n} approved sewage haulers from Bucks County Health Department, revised 7 July 2025</caption>
      <thead><tr><th>Business</th><th>Address</th><th>Phone</th><th>DEP transporter no.</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-bucks-pa.json">data/haulers-bucks-pa.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Stephen Shortell. Last updated 3 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'pa/bucks.html'
    out_html.write_text(page)
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Build Clark County OH registered septage haulers JSON + HTML from CCCHD 12 Feb 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://ccchd.com/wp-content/uploads/2026/02/2026-Registered-Haulers-List_2.12.2026.pdf'
PARENT_URL = 'https://ccchd.com/environmental-health/household-sewage-septic/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-02-12'
RETRIEVED = '2026-09-15'
ARCHIVE = 'data/sources/clark-oh-2026-registered-haulers-02-12.pdf'
ARCHIVE_TXT = 'data/sources/clark-oh-2026-registered-haulers-02-12.txt'

# Hand-verified from pdftotext -layout of 2026-Registered-Haulers-List_2.12.2026.pdf
# (PDF CreationDate 12 February 2026 UTC; footer Updated 2/12/2026; linked from CCCHD Sewage & Septic
# as 2026 Registered Septage Hauler List). Spellings kept as printed (Frankilin; Urabana; So. Charleston).
RECORDS = [
    {'reg': '591', 'name': 'A to Z Septic', 'operator': 'Glen Henderson', 'phone': '937-829-1858', 'address': '23 Powell Ave. Fairborn, OH 45324'},
    {'reg': '60', 'name': 'AAA Wastewater Services Inc (Triple A Pro Services)', 'operator': 'Timothy DeHart', 'phone': '937-746-6361', 'address': '3677 Anthony Lane Frankilin, OH 45005'},
    {'reg': '589', 'name': 'Alexander Sewer & Drain LLC', 'operator': 'Kelly Goubeaux', 'phone': '937-335-7509', 'address': '2 S. Main St. P.O. Box 64 Casstown, OH 45312'},
    {'reg': '6', 'name': 'Bevan Sanitation LLC', 'operator': 'JoAnn Bevan', 'phone': '937-969-8589', 'address': '4250 Hominy Ridge Rd. Springfield, OH 45502'},
    {'reg': '792', 'name': 'Bobcat Multi-Works (Bobcat Sanitation)', 'operator': 'Steve Moody', 'phone': '937-585-9904', 'address': '2765 County Rd. 21 DeGraff, OH 43318'},
    {'reg': '10', 'name': 'Buckeye Sanitary Services LLC', 'operator': 'Eddis Wiseman', 'phone': '937-399-3242', 'address': '1236 Villa Rd. Springfield, OH 45503'},
    {'reg': '307', 'name': 'C.T. Brown Sanitation', 'operator': 'Tom Brown', 'phone': '937-620-8939', 'address': '1752 Jones Rd. Xenia, OH 45385'},
    {'reg': '799', 'name': 'Darby Creek Septic LLC', 'operator': 'Brandon Yoder', 'phone': '740-206-4856', 'address': '5885 Lafayette-Plain City Rd. London, OH 43140'},
    {'reg': "782", 'name': "Dooley's Sanitation Service LLC", 'operator': 'Ricky Dooley', 'phone': '937-653-3007', 'address': '919 Troy Hill Rd Urbana, OH 43078'},
    {'reg': '550', 'name': "John's Reliable Septic LLC", 'operator': 'John Manus', 'phone': '937-926-1482', 'address': '8710 South Charleston Pk. So. Charleston, OH 45368'},
    {'reg': '183', 'name': "McKeever's", 'operator': 'Jerry Schlagel', 'phone': '937-652-1898', 'address': '1248 East US Hwy 36, Urabana, OH 43078'},
    {'reg': '592', 'name': 'Miami Valley Septic Service', 'operator': 'Joe Baumgardner', 'phone': '937-315-0415', 'address': '6255 New Carlisle Pike Springfield, OH 45504'},
    {'reg': '44', 'name': 'Mr. Clean Port-a-Potties', 'operator': 'Raghvendra Bali', 'phone': '937-284-3382', 'address': 'P.O. Box 41 Springfield, OH 45501'},
    {'reg': '50', 'name': 'Pro Kleen Industrial Services Inc.', 'operator': 'Amanda Neighborgall', 'phone': '740-689-1886', 'address': '1030 Mill Park Drive Lancaster, OH 43140'},
    {'reg': '14', 'name': 'Roto Rooter Services Co.', 'operator': 'Kristen Sizemore', 'phone': '937-353-7093', 'address': '9490 Byers Rd. Miamisburg, OH 45342'},
    {'reg': '781', 'name': 'Royalty Restroom Rentals LLC', 'operator': 'Levi Fox', 'phone': '937-216-2562', 'address': '1147 Hillcrest Dr. Troy, OH 45373'},
    {'reg': '24', 'name': 'Rumpke Transportation Company LLC.', 'operator': 'Sahil Panse', 'phone': '513-851-0122 ext. 3586', 'address': '3990 Generation Dr. Cincinnati, OH 45251'},
    {'reg': '787', 'name': 'That Septic Guy LLC', 'operator': 'Jay Reed', 'phone': '937-342-0629', 'address': '5657 Moorefield Rd. Springfield, OH 45502'},
    {'reg': '506', 'name': "Yoder's Septic Service LLC", 'operator': 'Carl Yoder', 'phone': '740-857-1822', 'address': '5890 Lafayette-Plain City Rd. London, OH 43140'},
    {'reg': '765', 'name': 'Toilets and Co.', 'operator': 'Chad Phillips', 'phone': '937-504-9331', 'address': '4675 Upper Valley Pike Springfield, OH 45502'},
]


def e(s):
    return html.escape(str(s), quote=True)


def phone_cell(printed):
    digits = re.sub(r'\D', '', printed or '')
    # Strip extension digits for tel: when "ext." present — keep display as printed
    if 'ext' in (printed or '').lower():
        base = re.split(r'\s*ext\.?\s*', printed, flags=re.I)[0]
        digits = re.sub(r'\D', '', base)
    if not digits:
        return '<td class="phones unknown">unknown</td>'
    href = f'+1{digits}' if len(digits) == 10 else f'+{digits}' if len(digits) == 11 and digits.startswith('1') else f'+1{digits}'
    return f'<td class="phones"><a href="tel:{href}">{e(printed)}</a></td>'


def main():
    assert len(RECORDS) == 20, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert 'Clark County Combined Health District' in txt
    assert 'Registered Septage Haulers' in txt
    assert 'Updated 2/12/2026' in txt
    assert 'Frankilin' in txt
    assert 'Urabana' in txt
    assert 'ext. 3586' in txt
    for r in RECORDS:
        assert r['name'][:24] in txt or r['name'].split(' (')[0][:24] in txt, r['name']
        assert r['reg'] in txt, r['reg']
        assert r['phone'] in txt, r['phone']
        assert r['operator'] in txt, r['operator']

    names = [r['name'] for r in RECORDS]
    assert len(names) == len(set(names)), 'duplicate names'
    regs = [r['reg'] for r in RECORDS]
    assert len(regs) == len(set(regs)), 'duplicate regs'

    records = []
    for r in RECORDS:
        records.append({
            'source_url': SOURCE_URL,
            'source_document_date': DOC_DATE,
            'retrieved': RETRIEVED,
            'registration_number': r['reg'],
            'name': r['name'],
            'role': 'Clark County Combined Health District registered septage hauler',
            'operator': r['operator'],
            'address': r['address'],
            'phone': r['phone'] or None,
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Clark County, Ohio',
        'source': {
            'publisher': 'Clark County Combined Health District',
            'title': '2026 Registered Septage Haulers (2026-Registered-Haulers-List_2.12.2026.pdf)',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': 'PDF footer Updated 2/12/2026; CreationDate 12 February 2026 UTC; linked from Sewage & Septic Systems as 2026 Registered Septage Hauler List',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Clark County Combined Health District 2026 Registered Septage Haulers PDF '
                '(2026-Registered-Haulers-List_2.12.2026.pdf; Updated 2/12/2026; 20 named haulers). '
                'Spellings kept as printed including Frankilin, OH; Urabana, OH; and So. Charleston. '
                'Rumpke phone kept as printed with extension (513-851-0122 ext. 3586). '
                'Local registration numbers are as printed. ODH statewide bond status is not on this PDF (marked unknown). '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Clark County Combined Health District and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-clark-oh.json'
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        phone = r['phone'] or ''
        rows.append(
            '<tr>'
            f'<td>{e(r["registration_number"])}</td>'
            f'<td>{e(r["name"])}</td>'
            f'<td>{e(r["operator"])}</td>'
            f'<td>{e(r["address"])}</td>'
            + phone_cell(phone)
            + '<td class="unknown">unknown</td>'
            + '</tr>'
        )

    n = len(records)
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Clark County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Clark County, Ohio registered septage haulers from Clark County Combined Health District PDF updated 12 February 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Clark County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Clark County Combined Health District’s PDF <cite>2026 Registered Septage Haulers</cite> (<code>2026-Registered-Haulers-List_2.12.2026.pdf</code>, updated 12 February 2026). Companies that haul septage in Clark County must register with the health district. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 15 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">2026-Registered-Haulers-List_2.12.2026.pdf</a>. Parent page: <a href="{e(PARENT_URL)}">Sewage &amp; Septic Systems</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Clark County septage-hauler registration only. ODH bond status is <strong>unknown</strong> on this PDF.</p>
      <p>The PDF lists <strong>{n}</strong> registered haulers (footer Updated 2/12/2026). Spellings are as printed (including Frankilin, OH; Urabana, OH; and So. Charleston). Rumpke phone is kept as printed with extension (<code>513-851-0122 ext. 3586</code>). Registration numbers are the local CCCHD numbers from the PDF.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="licking.html">Licking County haulers</a> · <a href="marion.html">Marion County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Clark County Combined Health District, PDF updated 12 February 2026</caption>
      <thead><tr><th>Reg #</th><th>Business</th><th>Owner / applicant</th><th>Address</th><th>Phone</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-clark-oh.json">data/haulers-clark-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, registration numbers, owners, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 15 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/clark.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

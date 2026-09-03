#!/usr/bin/env python3
"""Build Lake County OH septage hauler JSON + HTML from LCGHD HAULER-030326.pdf."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://www.lcghd.org/wp-content/uploads/2026/03/HAULER-030326.pdf'
PARENT_URL = 'https://www.lcghd.org/om-program-septic/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-03-03'
RETRIEVED = '2026-09-02'
ARCHIVE = 'data/sources/lake-oh-hauler-2026-03-03.pdf'

# Hand-transcribed from pdftotext -layout of HAULER-030326.pdf (3 pages).
# PDF footer prints "27 TOTAL"; page 1 opens with an empty comma-only address slot
# that is not a named business — 26 named firms are listed below. Phone missing
# on PORTA BANDIT LLC marked unknown. Do not invent fields.
RECORDS = [
    {
        'name': 'A & A PORTA POTTY',
        'contact': 'AUSTIN SESLER',
        'address': '2979 E CENTER STREET, CONNEAUT, OH 44030',
        'phone_as_printed': '1-440-855-2338',
    },
    {
        'name': 'ARIS COMPANY, LLC',
        'contact': 'MICHAEL SKOLARIS',
        'address': 'PO BOX 23097, CHAGRIN FALLS, OH 44023',
        'phone_as_printed': '1-330-562-8300',
    },
    {
        'name': 'ASAP SANITARY SERVICES',
        'contact': 'JOHN ACKWORTH',
        'address': '521 YOUNGSTOWN WARREN ROAD, NILES, OH 44446',
        'phone_as_printed': '1-330-989-5100',
    },
    {
        'name': 'AUBURN-BAINBRIDGE EXCAVATING',
        'contact': 'LEWIS TOMSIC JR',
        'address': 'PO BOX 233, NEWBURY, OH 44065',
        'phone_as_printed': '1-440-543-8371',
    },
    {
        'name': 'CAMEL SERVICES LLC DBA MONARCH SANI SERVICES',
        'contact': 'CHRISTOPHER S HUDAK',
        'address': '7737 MORLEY ROAD, MENTOR, OH 44060',
        'phone_as_printed': '1-440-668-7197',
    },
    {
        'name': 'CEE BEE WASTEWATER',
        'contact': 'CARL BARTHOLOMEW',
        'address': '274 BOWHALL ROAD, PAINESVILLE, OH 44077',
        'phone_as_printed': '1-440-523-1927',
    },
    {
        'name': 'CLN PORTABLE RESTROOM SERVICE COMPANY',
        'contact': 'SCOTT HOAR',
        'address': 'PO BOX 1026, BURTON, OH 44021',
        'phone_as_printed': '1-440-821-0114',
    },
    {
        'name': "COLE'S SEPTIC SERVICE INC. AN ARIS CO LLC CO",
        'contact': 'MIKE SKOLARIS',
        'address': 'PO BOX 771, CHARDON, OH 44024',
        'phone_as_printed': '1-440-942-3464',
    },
    {
        'name': 'COUNTY WASTE SERVICES, LTD.',
        'contact': 'JODI GREEN/BRANDON LAUER',
        'address': 'P O BOX 269, UNIONVILLE, OH 44088',
        'phone_as_printed': '1-800-839-0540',
    },
    {
        'name': 'FRY SEPTIC INDUSTRIES INC.',
        'contact': 'SAMUEL MEDVED',
        'address': '14780 VALENTINE ROAD, THOMPSON, OH 44086',
        'phone_as_printed': '1-440-357-6342',
    },
    {
        'name': 'G. KAUFMAN SEPTIC TANK CLEANING, LLC',
        'contact': 'GARY KAUFMAN',
        'address': '11051 TAYLOR MAY ROAD, AUBURN, OH 44023',
        'phone_as_printed': '1-440-477-3962',
    },
    {
        'name': 'GEAUGA SEPTIC SYSTEM SERVICE, LLC',
        'contact': 'ED GEBER',
        'address': 'PO BOX 301, NEWBURY, OH 44065',
        'phone_as_printed': '1-440-564-5356',
    },
    {
        'name': 'JUDD SEPTIC TANK CLEANING COMPANY',
        'contact': 'RICHARD JUDD JR.',
        'address': '16500 PIONEER ROAD, MIDDLEFIELD, OH 44062',
        'phone_as_printed': '1-440-636-2986',
    },
    {
        'name': "KING'S SANITARY SERVICES, LLC",
        'contact': 'REX KING JR/REX KING SR.',
        'address': '1306 ST.RT. 88, PO BOX 240, BRISTOLVILLE, OH 44402',
        'phone_as_printed': '1-330-360-0735',
    },
    {
        'name': 'KLARICH FARMS DBA FRANK KLARICH',
        'contact': 'FRANK KLARICH',
        'address': 'PO BOX 53, BURTON, OH 44021',
        'phone_as_printed': '1-440-666-9482',
    },
    {
        'name': 'LIQUID ENVIRONMENTAL SOLUTIONS',
        'contact': 'CIRO GRANDINI',
        'address': '37100 RESEARCH DRIVE, EASTLAKE, OH 44095',
        'phone_as_printed': '1-440-942-6867',
    },
    {
        'name': 'MUNN SEPTIC TANK CLEANING AN ARIS CO LLC CO.',
        'contact': 'MICHAEL SKOLARIS',
        'address': 'PO BOX 276, NEWBURY, OH 44065',
        'phone_as_printed': '1-440-564-5711',
    },
    {
        'name': 'NICHOLAS & SON',
        'contact': 'MICHAEL SKOLARIS',
        'address': 'PO BOX 66, MENTOR, OH 44061',
        'phone_as_printed': '1-440-255-4610',
    },
    {
        'name': 'NORTHEAST SEPTIC SERVICE, T & D SERVICES INC.',
        'contact': 'THOMAS J. SNOOK',
        'address': 'P.O. BOX 747, GENEVA, OH 44041',
        'phone_as_printed': '1-440-466-4406',
    },
    {
        'name': 'PORTA BANDIT LLC',
        'contact': 'ETHAN MCLASKEY',
        'address': '12486 GAR HIGHWAY, CHARDON, OH 44024',
        'phone_as_printed': '',
    },
    {
        'name': 'THOMAS STEIGERWALD LLC & STEIGERWALD PLUMBIN',
        'contact': 'THOMAS STEIGERWALD',
        'address': '8678 MAYFIELD ROAD, CHESTERLAND, OH 44026',
        'phone_as_printed': '1-440-729-7867',
    },
    {
        'name': 'TIM FRANK SEPTIC TANK CLEANING COMPANY',
        'contact': 'TOM FRANK',
        'address': 'P.O. BOX 277, HUNTSBURG, OH 44046',
        'phone_as_printed': '1-440-636-5111',
    },
    {
        'name': 'UNITED RENTALS (NORTH AMERICA) INC.',
        'contact': 'RELIABLE ONSITE SERVICES',
        'address': '1050 KILLIAN ROAD, AKRON, OH 44312',
        'phone_as_printed': '1-330-733-9000',
    },
    {
        'name': 'WALT KUCHARSKI SEPTIC SERVICE, INC.',
        'contact': 'W. CLAY KUCHARSKI',
        'address': '2841 STUBBINS ROAD, RICHFIELD, OH 44141',
        'phone_as_printed': '1-440-232-0767',
    },
    {
        'name': 'WILSON SEPTIC TANK',
        'contact': 'ADAM WILSON',
        'address': '5016 WEBB ROAD, PERRY, OH 44081',
        'phone_as_printed': '1-440-728-0717',
    },
    {
        'name': 'WOLCOTT SEPTIC PUMPING, INCORPORATED',
        'contact': 'DENNIS WOLCOTT',
        'address': '13781 GAR HIGHWAY, CHARDON, OH 44024',
        'phone_as_printed': '1-440-285-7604',
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
    assert len(RECORDS) == 26, len(RECORDS)
    names = [r['name'] for r in RECORDS]
    assert len(names) == len(set(names)), 'duplicate names'

    records = []
    for r in RECORDS:
        phone = fmt_phone(r['phone_as_printed'])
        records.append({
            'source_url': SOURCE_URL,
            'source_document_date': DOC_DATE,
            'retrieved': RETRIEVED,
            'name': r['name'],
            'role': 'Lake County General Health District registered septage hauler',
            'contact': r['contact'],
            'address': r['address'],
            'phone': phone,
            'phone_as_printed': r['phone_as_printed'] or None,
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Lake County, Ohio',
        'source': {
            'publisher': 'Lake County General Health District',
            'title': 'Septage Haulers',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from LCGHD HAULER-030326.pdf (footer date 03/03/2026). '
                'PDF footer prints “27 TOTAL”; page 1 opens with an empty comma-only address '
                'slot that is not a named business, so 26 named firms are listed. Phone is '
                'missing on PORTA BANDIT LLC (marked unknown). ODH statewide bond status is '
                'not on this PDF (marked unknown). Business names and operator lines are '
                'printed as on the PDF, including truncated “STEIGERWALD PLUMBIN”. A septage '
                'hauler registration is not a service-provider inspection credential. Appearance '
                'is not an endorsement. Verify with LCGHD and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-lake-oh.json'
    out_json.write_text(json.dumps(payload, indent=2) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        rows.append(
            '<tr>'
            f'<td>{e(r["name"])}</td>'
            f'<td>{e(r["contact"])}</td>'
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
  <title>Lake County OH Septic Pumpers | Septic Pump Index</title>
  <meta name="description" content="{n} Lake County, Ohio registered septage haulers from Lake County General Health District PDF dated 3 March 2026. Ohio local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Lake County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Lake County General Health District’s PDF <cite>Septage Haulers</cite>, dated 3 March 2026 (<code>HAULER-030326.pdf</code>). Companies that pump septic tanks in Lake County must register with LCGHD. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 2 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">HAULER-030326.pdf</a>. Parent page: <a href="{e(PARENT_URL)}">O&amp;M Program for Household Sewage Treatment Systems</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Lake County registration only. ODH bond status is <strong>unknown</strong> on this PDF.</p>
      <p>The PDF footer prints “27 TOTAL.” Page 1 opens with an empty comma-only address slot that is not a named business, so we list the <strong>{n} named firms</strong> printed on the three pages. Phone is missing on PORTA BANDIT LLC — marked unknown. Business names are as printed (including truncated “STEIGERWALD PLUMBIN”).</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="geauga.html">Geauga County pumpers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Lake County General Health District, PDF dated 3 March 2026</caption>
      <thead><tr><th>Business</th><th>Operator</th><th>Address</th><th>Phone</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-lake-oh.json">data/haulers-lake-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, operators, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Stephen Shortell. Last updated 2 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/lake.html'
    out_html.write_text(page)
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

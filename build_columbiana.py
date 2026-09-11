#!/usr/bin/env python3
"""Build Columbiana County OH STS pumpers JSON + HTML from CCGHD 2026-STS-Pumpers.pdf."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://www.columbiana-health.org/wp-content/uploads/2026-STS-Pumpers.pdf'
PARENT_URL = 'https://www.columbiana-health.org/sewage/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-04-22'
RETRIEVED = '2026-09-10'
ARCHIVE = 'data/sources/columbiana-oh-2026-sts-pumpers.pdf'
ARCHIVE_TXT = 'data/sources/columbiana-oh-2026-sts-pumpers.txt'

# Hand-verified from pdftotext -layout of 2026-STS-Pumpers.pdf
# (PDF CreationDate 22 Apr 2026 UTC; title “2026 STS Pumpers Alphabetical by City”).
# 22 rows. Keep spellings as printed (Willam Milner; Charlie Hoffman Septic Svcs.;
# N. Benton; Yo-town Kingsville). ODH bond not on this PDF.
RECORDS = [
    {'name': 'Reliable Onsite Services', 'operator': 'United Rentals (North America)', 'phone': '330-733-9000', 'address': '1050 Killian Rd., Akron, OH 44312'},
    {'name': 'Sosnick Septic Service', 'operator': 'Michael Sosnick', 'phone': '330-584-6718', 'address': '19542 W. Middletown Rd., Beloit, OH 44609'},
    {'name': 'Charlie Hoffman Septic Svcs.', 'operator': 'Mark Biskup', 'phone': '330-584-5466', 'address': '16124 W. Western Reserve Rd., Berlin Center, OH 44401'},
    {'name': 'Morris Drain Service, Inc.', 'operator': 'Ronald Morris', 'phone': '330-788-2560', 'address': '4200 Simon Rd., Boardman, OH 44512'},
    {'name': 'Klarich Farms, LLC', 'operator': 'Frank Klarich', 'phone': '440-285-2550', 'address': 'PO Box 53, Burton, OH 44021'},
    {'name': 'Rosebud Sanitation', 'operator': 'Jay Householder Jr.', 'phone': '330-385-6622', 'address': '49377 Hickman Rd., Calcutta, OH 43920'},
    {'name': 'Chester H3, LLC, dba Erwin Septic Svc.', 'operator': 'Joseph Heretta III', 'phone': '330-627-4700', 'address': '333 Steubenville Rd., SE, Carrollton, OH 44615'},
    {'name': 'Cowboy Miller Septic Pumping', 'operator': 'Sheri Brown', 'phone': '330-821-8060', 'address': '2012 Notman Rd., Deerfield, OH 44411'},
    {'name': 'Gold-N-Deuce, LLC', 'operator': 'Brian Myers / David Brown', 'phone': '330-851-8541', 'address': '6085 Waynesburg Rd. NW, Dellroy, OH 44620'},
    {'name': "Dalton's Service Co., LLC", 'operator': 'Loran & Deborah Dalton', 'phone': '724-752-4545', 'address': '1230 Mercer Rd., Ellwood City, PA 16117'},
    {'name': "Tom's Septic and Drain", 'operator': 'Jeff Chahine Jr.', 'phone': '330-545-8584', 'address': '1057 Trumbull Ave., Girard, OH 44420'},
    {'name': 'Whipkey Septic Pumping LLC', 'operator': 'Clayton Whipkey', 'phone': '330-736-1821', 'address': '4300 Middle St., Homeworth, OH 44634'},
    {'name': 'Novak Septic Pumping', 'operator': 'Timothy & Anita Novak', 'phone': '330-420-9929', 'address': '38350 Adams Rd., Lisbon, OH 44432'},
    {'name': 'Family Flush Septic Service', 'operator': 'Timothy J. Novak & Anita Novak', 'phone': '330-420-5315', 'address': '38350 Adams Rd., Lisbon, OH 44432'},
    {'name': 'Bosley Drain & Septic', 'operator': 'Josh Tully', 'phone': '330-454-4000', 'address': 'PO Box 303, Louisville, OH 44641'},
    {'name': "Milner's Septic", 'operator': 'Willam Milner', 'phone': '330-868-9700', 'address': '100 Arbor Rd., NW, PO Box 2, Minerva, OH 44657'},
    {'name': "CJ's Port a Potty", 'operator': 'Jason Pierce', 'phone': '234-562-0062', 'address': '9379 First East St., N. Benton, OH 44449'},
    {'name': 'Salem Septic', 'operator': 'John Mercer', 'phone': '330-525-7800', 'address': '30761 Georgetown Rd., Salem, OH 44460'},
    {'name': "Steve's Service", 'operator': 'Stephen Utt', 'phone': '330-938-9325', 'address': '298 East Florida Ave., Sebring, OH 44672'},
    {'name': 'A Rooter Man', 'operator': 'James English', 'phone': '877-232-1520', 'address': '195 Potomac Ave., Unit B, Tallmadge, OH 44278'},
    {'name': "Duke's Sanitary Service, Inc.", 'operator': 'Mark Furrie Sr.', 'phone': '330-856-3129', 'address': '1009 Yo-town Kingsville Rd., NE, Vienna, OH 44473'},
    {'name': 'Patterson Specialty Services', 'operator': 'Bill Patterson', 'phone': '330-862-3371', 'address': '300 W. Lisbon St., Waynesburg, OH 44688'},
]


def e(s):
    return html.escape(str(s), quote=True)


def phone_cell(printed):
    digits = re.sub(r'\D', '', printed or '')
    if not digits:
        return '<td class="unknown">unknown</td>'
    href = f'+1{digits}' if len(digits) == 10 else f'+{digits}' if len(digits) == 11 and digits.startswith('1') else f'+1{digits}'
    return f'<td class="phones"><a href="tel:{href}">{e(printed)}</a></td>'


def main():
    assert len(RECORDS) == 22, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert '2026 STS Pumpers' in txt
    assert 'Alphabetical by City' in txt
    for r in RECORDS:
        assert r['name'] in txt, r['name']
        # Operator may wrap; check a distinctive fragment
        op_frag = r['operator'].split('/')[0].strip().split('&')[0].strip()[:12]
        assert op_frag in txt, (r['operator'], op_frag)
        assert r['phone'] in txt, r['phone']
        street = r['address'].split(',')[0]
        assert street in txt, street

    names = [r['name'] for r in RECORDS]
    assert len(names) == len(set(names)), 'duplicate names'

    records = []
    for r in RECORDS:
        records.append({
            'source_url': SOURCE_URL,
            'source_document_date': DOC_DATE,
            'retrieved': RETRIEVED,
            'name': r['name'],
            'role': 'Columbiana County General Health District registered STS pumper',
            'operator': r['operator'],
            'address': r['address'],
            'phone': r['phone'],
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Columbiana County, Ohio',
        'source': {
            'publisher': 'Columbiana County General Health District',
            'title': '2026 STS Pumpers Alphabetical by City',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': 'PDF CreationDate 22 April 2026 UTC; live file 2026-STS-Pumpers.pdf',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Columbiana County General Health District 2026-STS-Pumpers.pdf '
                '(CreationDate 22 Apr 2026). 22 registered STS pumpers listed alphabetical by city. '
                'Spellings kept as printed (Willam Milner; Charlie Hoffman Septic Svcs.; N. Benton; '
                'Yo-town Kingsville). ODH statewide bond status is not on this PDF (marked unknown). '
                'A pumper registration is not a service-provider inspection credential. Appearance '
                'is not an endorsement. Verify with CCGHD and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-columbiana-oh.json'
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        rows.append(
            '<tr>'
            f'<td>{e(r["name"])}</td>'
            f'<td>{e(r["operator"])}</td>'
            f'<td>{e(r["address"])}</td>'
            + phone_cell(r['phone'])
            + '<td class="unknown">unknown</td>'
            + '</tr>'
        )

    n = len(records)
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Columbiana County OH Septic Pumpers | Septic Pump Index</title>
  <meta name="description" content="{n} Columbiana County, Ohio registered STS pumpers from Columbiana County General Health District PDF dated 22 April 2026. Ohio local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Columbiana County, Ohio — registered STS pumpers</h1>
    <p class="lede">Transcribed from Columbiana County General Health District’s PDF <cite>2026 STS Pumpers Alphabetical by City</cite> (<code>2026-STS-Pumpers.pdf</code>, PDF dated 22 April 2026). Companies that pump septic tanks in Columbiana County must register with the health district. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 10 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">2026-STS-Pumpers.pdf</a>. Parent page: <a href="{e(PARENT_URL)}">Sewage</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Columbiana County STS pumper registration only. ODH bond status is <strong>unknown</strong> on this PDF.</p>
      <p>The PDF lists <strong>{n} pumpers</strong> alphabetical by city. Spellings are as printed (including Willam Milner, Charlie Hoffman Septic Svcs., N. Benton, and Yo-town Kingsville).</p>
      <p>A septage pumper registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="portage.html">Portage County haulers</a> · <a href="lake.html">Lake County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered STS pumpers from Columbiana County General Health District, PDF dated 22 April 2026</caption>
      <thead><tr><th>Business</th><th>Operator</th><th>Address</th><th>Phone</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-columbiana-oh.json">data/haulers-columbiana-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, operators, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 10 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/columbiana.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

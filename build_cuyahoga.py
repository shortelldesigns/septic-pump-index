#!/usr/bin/env python3
"""Build Cuyahoga County OH registered septage haulers JSON + HTML from CCBH 3 June 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://ccbh.net/wp-content/uploads/2026/06/2026-Registered-Haulers-6.4.26.pdf'
PARENT_URL = 'https://ccbh.net/household-sewage-downloads/'
PROGRAM_URL = 'https://ccbh.net/sewage-haulers-installers-and-service-providers/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-06-03'
RETRIEVED = '2026-09-16'
ARCHIVE = 'data/sources/cuyahoga-oh-2026-registered-haulers-06-04.pdf'
ARCHIVE_TXT = 'data/sources/cuyahoga-oh-2026-registered-haulers-06-04.txt'

# Hand-verified from pdftotext -layout of 2026-Registered-Haulers-6.4.26.pdf
# (footer Last updated 6/3/2026; filename dated 6.4.26; linked from CCBH Household Sewage Downloads
# as 2026 Registered Septage Haulers). Spellings kept as printed (Llc; P.O Box; Remson; Inc;).
RECORDS = [
    {'name': 'Advanced Plumbing & Drain', 'owner': 'Ernest B. Fisco', 'phone': '440-331-5555', 'address': '7277 Bessemer Ave, Cleveland, OH 44127'},
    {'name': 'A & P Septic', 'owner': 'Don Pack', 'phone': '440-748-3105', 'address': '27654 Crocker Rd, Columbia Station, OH 44028'},
    {'name': 'All Town & Country Septic', 'owner': 'Thomas Blankenship', 'phone': '330-745-2277', 'address': '3500 S. Hametown Rd, Norton, OH 44203'},
    {'name': 'Allen Drain Service', 'owner': 'Bernie Noble', 'phone': '330-673-6482', 'address': '1008 Mogadore Rd, Kent, OH 44240'},
    {'name': 'Aris Company', 'owner': 'Mike Skolaris', 'phone': '330-995-8300', 'address': 'P.O. Box 23097, Chagrin Falls, OH 44023'},
    {'name': 'ASAP Sanitary Services', 'owner': 'John Ackworth', 'phone': '330-989-5100', 'address': '521 Youngstown Warren Rd, Niles, OH 44446'},
    {'name': 'Auburn Bainbridge Excavating', 'owner': 'Lewis C. Tomsic', 'phone': '440-543-8371', 'address': '11313 E. Washington St, Chagrin Falls, OH 44023'},
    {'name': 'Burnetts Septic Services', 'owner': 'Anthony Reueglia', 'phone': '440-355-5526', 'address': '120 Commerce Dr, Lagrange, OH 44050'},
    {'name': 'C & K Industrial Services', 'owner': 'Paul Harrison', 'phone': '216-642-0055', 'address': '5720 E Schaaf Rd, Independence, OH 44131'},
    {'name': 'Camel Services, LLC', 'owner': 'Chris Hudak', 'phone': '440-231-5318', 'address': '7737 Morley Rd, Mentor, OH 44060'},
    {'name': 'CLN Portable Restroom Service', 'owner': 'Scott Hoar', 'phone': '440-821-0114', 'address': 'P.O. Box 1026, Burton, OH 44021'},
    {'name': "Cole's Septic", 'owner': 'Mike Skolaris', 'phone': '440-942-3464', 'address': 'P.O. Box 771, Chardon, OH 44024'},
    {'name': 'County Waste Services, LTD', 'owner': 'Brandon Lauer', 'phone': '440-428-9083', 'address': 'PO Box 269, Unionville, OH 44088'},
    {'name': 'Dewey Pelton Septic, LLC', 'owner': 'Patrick Johnson', 'phone': '440-965-8919', 'address': '6803 St. Rt. 60, Wakeman, OH 44889'},
    {'name': 'Double Flush Septic', 'owner': 'Scott Scholz', 'phone': '330-391-5551', 'address': '2481 Remson Rd, Medina, OH 44256'},
    {'name': 'Dynamerican', 'owner': 'Kevin Church', 'phone': '330-666-8863', 'address': '1011 Lake Rd, Medina, OH 44256'},
    {'name': 'Father & Son Septic Service', 'owner': 'James Coon', 'phone': '440-965-5800', 'address': '53001 Ward Rd, Wakeman, OH 44889'},
    {'name': 'G. Kaufman Septic', 'owner': 'Gary Kaufman', 'phone': '440-477-7510', 'address': '11051 Taylor May Rd, Auburn, OH 44023'},
    {'name': 'Geauga Septic Service Llc', 'owner': 'Edmond Geber', 'phone': '440-564-5356', 'address': 'P.O Box 301, Newbury, OH 44065'},
    {'name': 'Jarvis Septic & Drain', 'owner': 'Ryan Morris', 'phone': '330-336-1893', 'address': '3596 Greenwich Rd, Seville, OH 44273'},
    {'name': 'Judd Septic Tank Cleaning', 'owner': 'Richard A. Judd Jr', 'phone': '440-636-2986', 'address': '16500 Pioneer Rd, Middlefield, OH 44062'},
    {'name': "King's Sanitary Services", 'owner': 'Rex King', 'phone': '330-372-3201', 'address': 'P.O. Box 240, Bristolville, OH 44402'},
    {'name': 'Klarich Farms LLC', 'owner': 'Frank Klarich', 'phone': '440-285-2550', 'address': '11561 Bell Rd, Newbury, OH 44065'},
    {'name': 'Liquid Environmental Solutions', 'owner': 'Amy Pugh', 'phone': '440-942-6867', 'address': '37100 Research Dr, Eastlake, OH 44095'},
    {'name': 'Mack Industries, Inc', 'owner': 'Anna Lohr', 'phone': '866-482-6225', 'address': '201 Columbia Rd., Valley City, OH 44280'},
    {'name': 'McClellan Septic', 'owner': 'Bob Myers', 'phone': '440-237-5082', 'address': '464 State Rd, Hinckley, OH 44233'},
    {'name': 'Munn Septic Tank Cleaning', 'owner': 'Mike Skolaris', 'phone': '440-564-5711', 'address': 'P.O. Box 276, Newbury, OH 44065'},
    {'name': 'Nicholas & Son Inc', 'owner': 'Mike Skolaris', 'phone': '440-255-4610', 'address': 'P.O. Box 66, Mentor, OH 44061'},
    {'name': 'PJ Sanitation, Inc', 'owner': 'Paul Hughett', 'phone': '440-986-8388', 'address': '8039 Pyle Rd, Amherst, OH 44001'},
    {'name': 'Porta Bandit LLC', 'owner': 'Ethan McCaskey', 'phone': '216-820-6444', 'address': '11976 Old State Rd, Chardon, OH 44024'},
    {'name': 'Sanitary Septic Tank', 'owner': 'Charles Dunlap', 'phone': '440-236-9200', 'address': '10915 Station Rd, Columbia Station, OH 44028'},
    {'name': 'Suburban Septic Service Inc', 'owner': 'Patrick Valentine', 'phone': '330-722-4262', 'address': '4229 Beck Rd, Medina, OH 44256'},
    {'name': 'Supeck Septic Services, LLC', 'owner': 'Tim Supeck', 'phone': '888-725-0209', 'address': '6407 Norwalk Rd, Medina, OH 44256'},
    {'name': 'The Waid Corp', 'owner': 'Ronald Waid', 'phone': '216-524-6037', 'address': '10200 Sweet Valley Dr, Valley View, OH 44125'},
    {'name': 'United Rentals (North America), Inc; DBA Reliable Onsite Services', 'owner': 'Lynn Vizdos', 'phone': '330-733-9000', 'address': '8001 Old Granger Rd, Cleveland, OH 44125'},
    {'name': 'Walt Kucharski Septic Service Inc', 'owner': 'Walter Clay Kucharski', 'phone': '440-232-0767', 'address': '2841 Stubbins Rd., Richfield, OH 44141'},
    {'name': 'Wilson Plumbing and Heating, LLC', 'owner': 'John Wilson', 'phone': '330-535-5386', 'address': '1501 Commerce Dr, Stow, OH 44224'},
    {'name': 'Wolcott Septic Tank Cleaning, Inc', 'owner': 'Dennis Wolcott', 'phone': '440-285-7604', 'address': '13781 G.A.R. Highway, Chardon, OH 44024'},
]


def e(s):
    return html.escape(str(s), quote=True)


def phone_cell(printed):
    digits = re.sub(r'\D', '', printed or '')
    if not digits:
        return '<td class="phones unknown">unknown</td>'
    href = f'+1{digits}' if len(digits) == 10 else f'+{digits}' if len(digits) == 11 and digits.startswith('1') else f'+1{digits}'
    return f'<td class="phones"><a href="tel:{href}">{e(printed)}</a></td>'


def main():
    assert len(RECORDS) == 38, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert '2026 STS Registered Haulers' in txt
    assert 'Last updated 6/3/2026' in txt
    assert 'United Rentals (North America), Inc;' in txt
    assert 'DBA Reliable Onsite Services' in txt
    assert 'Geauga Septic Service Llc' in txt
    assert 'P.O Box 301' in txt
    assert 'Remson Rd' in txt
    for r in RECORDS:
        check = r['name'].split(' DBA ')[0].rstrip(';').strip()
        assert check[:28] in txt or r['name'][:28] in txt, r['name']
        assert r['phone'] in txt, r['phone']
        assert r['owner'] in txt, r['owner']

    names = [r['name'] for r in RECORDS]
    assert len(names) == len(set(names)), 'duplicate names'

    records = []
    for r in RECORDS:
        records.append({
            'source_url': SOURCE_URL,
            'source_document_date': DOC_DATE,
            'retrieved': RETRIEVED,
            'name': r['name'],
            'role': 'Cuyahoga County Board of Health registered septage hauler',
            'operator': r['owner'],
            'address': r['address'],
            'phone': r['phone'] or None,
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Cuyahoga County, Ohio',
        'source': {
            'publisher': 'Cuyahoga County Board of Health',
            'title': '2026 STS Registered Haulers (2026-Registered-Haulers-6.4.26.pdf)',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'program_url': PROGRAM_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': 'PDF footer Last updated 6/3/2026; filename 2026-Registered-Haulers-6.4.26.pdf; linked from Household Sewage Downloads as 2026 Registered Septage Haulers',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Cuyahoga County Board of Health 2026 STS Registered Haulers PDF '
                '(2026-Registered-Haulers-6.4.26.pdf; Last updated 6/3/2026; 38 named haulers). '
                'Spellings kept as printed including Geauga Septic Service Llc; P.O Box 301; Remson Rd; '
                'and United Rentals (North America), Inc; DBA Reliable Onsite Services (DBA on a second PDF line). '
                'No local registration numbers on this PDF. Fax and email columns omitted from the HTML table. '
                'ODH statewide bond status is not on this PDF (marked unknown). '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Cuyahoga County Board of Health and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-cuyahoga-oh.json'
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        phone = r['phone'] or ''
        rows.append(
            '<tr>'
            f'<td>{e(r["name"])}</td>'
            f'<td>{e(r["operator"])}</td>'
            f'<td>{e(r["address"])}</td>'
            + phone_cell(phone)
            + '<td class="unknown">unknown</td>'
            + '</tr>'
        )

    n = len(records)
    page = (
        '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cuyahoga County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="__N__ Cuyahoga County, Ohio registered septage haulers from Cuyahoga County Board of Health PDF last updated 3 June 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Cuyahoga County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Cuyahoga County Board of Health’s PDF <cite>2026 STS Registered Haulers</cite> (<code>2026-Registered-Haulers-6.4.26.pdf</code>, last updated 3 June 2026). Companies that haul septage in Cuyahoga County must register with the board of health. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 16 September 2026 (US/Pacific). Official file: <a href="__SOURCE_URL__">2026-Registered-Haulers-6.4.26.pdf</a>. Downloads page: <a href="__PARENT_URL__">Household Sewage Downloads</a>. Program page: <a href="__PROGRAM_URL__">Sewage Haulers, Installers and Service Providers</a>. Verify statewide bonds via <a href="__ODH_URL__">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Cuyahoga County septage-hauler registration only. ODH bond status is <strong>unknown</strong> on this PDF.</p>
      <p>The PDF lists <strong>__N__</strong> registered haulers (footer Last updated 6/3/2026). Spellings are as printed (including Geauga Septic Service Llc; P.O Box 301; Remson Rd). United Rentals DBA line is kept as printed (<code>United Rentals (North America), Inc; DBA Reliable Onsite Services</code>). No local registration numbers appear on this PDF. Fax and email columns from the PDF are omitted here.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="clark.html">Clark County haulers</a> · <a href="geauga.html">Geauga County pumpers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>__N__ registered septage haulers from Cuyahoga County Board of Health, PDF last updated 3 June 2026</caption>
      <thead><tr><th>Business</th><th>Owner</th><th>Address</th><th>Phone</th><th>ODH bond</th></tr></thead>
      <tbody>
__ROWS__
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-cuyahoga-oh.json">data/haulers-cuyahoga-oh.json</a>. Archived PDF: <a href="../__ARCHIVE__">__ARCHIVE__</a>. Names, owners, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 16 September 2026 (US/Pacific).</p>
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
        .replace('__N__', str(n))
        .replace('__SOURCE_URL__', e(SOURCE_URL))
        .replace('__PARENT_URL__', e(PARENT_URL))
        .replace('__PROGRAM_URL__', e(PROGRAM_URL))
        .replace('__ODH_URL__', e(ODH_URL))
        .replace('__ARCHIVE__', e(ARCHIVE))
        .replace('__ROWS__', chr(10).join(rows))
    )
    out_html = ROOT / 'oh/cuyahoga.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Build Darke County OH septage haulers JSON + HTML from DCGHD 1 Apr 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://darkecountyhealth.org/wp-content/uploads/2026/04/SEWAGE-TREATMENT-04-1-2026HAULERS.pdf'
PARENT_URL = 'https://darkecountyhealth.org/services/environmental-health/sewage-treatment-systems/sewage-contractor-registrations/'
PROGRAM_URL = 'https://darkecountyhealth.org/services/environmental-health/sewage-treatment-systems/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-04-01'
RETRIEVED = '2026-09-24'
ARCHIVE = 'data/sources/darke-oh-2026-septage-haulers.pdf'
ARCHIVE_TXT = 'data/sources/darke-oh-2026-septage-haulers.txt'

# Hand-verified from pdftotext -layout of SEWAGE-TREATMENT-04-1-2026HAULERS.pdf
# (Darke County General Health District; footer 04/01/2026; page 2 prints 20 TOTAL).
# Linked from Sewage Contractor Registrations as the current haulers list.
# Spellings kept as printed (BOOSO'S; FLATTER'S; FRECH'S; MIKE'S;
# ARTZ phone printed truncated as 1-459-996-6; ARTZ street GREENVILLE NASHVILLE
# with no Rd/St suffix; PORTA KLEEN operator line singular SERVICE;
# MT SERVICES INC operator line MILLER PORTABLES).
RECORDS = [
    {'name': 'ACCURATE SEPTIC SERVICES', 'operator': 'MARK MOORE', 'phone': '1-937-947-8080', 'address': '11131 MONTGOMERY CO LINE RD BROOKVILLE, OH 45309'},
    {'name': 'ALEXANDER SEWER & DRAIN', 'operator': 'KELLY GOUBEAUX', 'phone': '1-937-875-0068', 'address': 'PO BOX 64 CASSTOWN, OH 45312'},
    {'name': 'ARTZ SEPTIC SERVICES', 'operator': 'KEEGAN ARTZ', 'phone': '1-459-996-6', 'address': '2853 GREENVILLE NASHVILLE GREENVILLE, OH 45331'},
    {'name': 'BARNES SEWER & SEPTIC, LLC', 'operator': 'ROBERT D. BOND', 'phone': '1-765-584-7295', 'address': '3075 N 100 W WINCHESTER, IN 47394'},
    {'name': "BOOSO'S SEPTIC CLEANING", 'operator': 'MARK BOOSO', 'phone': '1-937-962-4435', 'address': '8882 ROCKRIDGE LEWISBURG, OH 45338'},
    {'name': 'COOPER SANITARY SERVICES', 'operator': 'NELSON COOPER JR', 'phone': '1-937-698-6200', 'address': '11567 HABER RD ENGLEWOOD, OH 45322'},
    {'name': 'D & H CONSTRUCTION', 'operator': 'DAVID HANEY', 'phone': '1-937-448-8071', 'address': '5961 RED RIVER WEST GROVE ROAD BRADFORD, OH 45308'},
    {'name': "FLATTER'S SEPTIC TANKS", 'operator': 'GARY FLATTER', 'phone': '1-937-548-7667', 'address': '7972 GREENVILLE CELINA RD GREENVILLE, OH 45331'},
    {'name': 'FRANTZ SEPTIC CLEANING', 'operator': 'JACK FRANTZ', 'phone': '1-937-526-3121', 'address': '10500 BRADFORD BLOOMER RD. COVINGTON, OH 45318'},
    {'name': "FRECH'S SEPTIC LLC", 'operator': 'TODD FRECH', 'phone': '1-937-996-1615', 'address': '2709 WILT RD NEW MADISON, OH 45346'},
    {'name': 'GRIERS POWER DIGGING LLC', 'operator': 'NICHOLAS GRIER', 'phone': '1-419-363-3390', 'address': '9422 ST RT 118 ROCKFORD, OH 45882'},
    {'name': "MIKE'S SANITATION, INC.", 'operator': 'RYAN EVERS', 'phone': '1-419-629-3695', 'address': '8810 BROCKMAN RD NEW BREMEN, OH 45869'},
    {'name': 'MT SERVICES INC', 'operator': 'MILLER PORTABLES', 'phone': '1-800-827-6808', 'address': 'PO BOX 136 BERLIN, OH 44610'},
    {'name': 'PORTA KLEEN INDUSTRIAL SERVICES', 'operator': 'PORTA KLEEN INDUSTRIAL SERVICE', 'phone': '1-513-330-6713', 'address': '1030 MILL PARK DR LANCASTER, OH 43130'},
    {'name': 'PRIME PUMPING AND SERVICES', 'operator': 'NICK TRANTANELLA', 'phone': '1-937-553-7400', 'address': '4076 EIDSON RD CAMDEN, OH 45311'},
    {'name': 'RAEGON GROUP LLC DBA RAEGON SEPTIC', 'operator': 'JEREMY BRIDENBAUGH', 'phone': '1-937-733-8456', 'address': '5183 SOUTH RANGELINE RD WEST MILTON, OH 45383'},
    {'name': 'ROTO-ROOTER SERVICES COMPANY', 'operator': 'ROTO-ROOTER SERVICES COMPANY', 'phone': '1-937-353-7093', 'address': '9490 BYERS RD MIAMISBURG, OH 45342'},
    {'name': 'ROYALTY RESTROOM RENTALS', 'operator': 'LEVI FOX', 'phone': '1-937-216-2562', 'address': '1147 HILLCREST DR TROY, OH 45373'},
    {'name': 'RUMPKE TRANSPORTATION COMPANY, LLC', 'operator': 'KRISTEN DETTY', 'phone': '1-513-851-0122', 'address': '3975 WAGNER FORD RD DAYTON, OH 45414'},
    {'name': 'SANDERS SEPTIC AND SEWER', 'operator': 'BRIAN SANDERS', 'phone': '1-937-564-3907', 'address': '409 SCHOOL ST BRADFORD, OH 45308'},
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
    assert len(RECORDS) == 20, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert 'Septage Haulers' in txt
    assert 'DARKE COUNTY GENERAL HEALTH DISTRICT' in txt
    assert '04/01/2026' in txt
    assert '20 TOTAL' in txt
    assert 'ACCURATE SEPTIC SERVICES' in txt
    assert 'ARTZ SEPTIC SERVICES' in txt
    assert '1-459-996-6' in txt
    assert "FLATTER'S SEPTIC TANKS" in txt
    assert "BOOSO'S SEPTIC CLEANING" in txt
    assert "FRECH'S SEPTIC LLC" in txt
    assert "MIKE'S SANITATION, INC." in txt
    assert 'RAEGON GROUP LLC DBA RAEGON SEPTIC' in txt
    assert 'MILLER PORTABLES' in txt
    assert 'PORTA KLEEN INDUSTRIAL SERVICE' in txt
    assert 'SANDERS SEPTIC AND SEWER' in txt
    for r in RECORDS:
        assert r['name'][:28] in txt, r['name']
        street = r['address'].split()[0]
        assert street in txt, r['address']
        assert r['phone'] in txt, r['phone']
        token = r['operator'].split()[0].replace(',', '')
        assert token in txt, r['operator']

    names = [r['name'] for r in RECORDS]
    assert len(names) == len(set(names)), 'duplicate names'

    records = []
    for r in RECORDS:
        records.append({
            'source_url': SOURCE_URL,
            'source_document_date': DOC_DATE,
            'retrieved': RETRIEVED,
            'name': r['name'],
            'role': 'Darke County General Health District registered septage hauler',
            'operator': r['operator'] or None,
            'address': r['address'],
            'phone': r['phone'] or None,
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Darke County, Ohio',
        'source': {
            'publisher': 'Darke County General Health District',
            'title': 'Septage Haulers (SEWAGE-TREATMENT-04-1-2026HAULERS.pdf)',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'program_url': PROGRAM_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': 'PDF footer 04/01/2026 on each page; page 2 prints 20 TOTAL; CreationDate 1 April 2026 PDT; linked from Sewage Contractor Registrations',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Darke County General Health District Septage Haulers PDF '
                '(SEWAGE-TREATMENT-04-1-2026HAULERS.pdf; footer 04/01/2026; 20 TOTAL). '
                'Spellings kept as printed including BOOSO\'S, FLATTER\'S, FRECH\'S, MIKE\'S, '
                'and ARTZ phone printed truncated as 1-459-996-6 (as on the PDF text layer). '
                'ARTZ street line prints GREENVILLE NASHVILLE with no Rd/St suffix. '
                'MT SERVICES INC operator line prints MILLER PORTABLES; '
                'PORTA KLEEN INDUSTRIAL SERVICES operator line prints singular SERVICE. '
                'No registration numbers on this PDF. ODH statewide bond status is not on this PDF (marked unknown). '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Darke County General Health District and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-darke-oh.json'
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        phone = r['phone'] or ''
        op = r['operator'] or ''
        rows.append(
            '<tr>'
            f'<td>{e(r["name"])}</td>'
            f'<td>{e(op) if op else "—"}</td>'
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
  <title>Darke County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Darke County, Ohio registered septage haulers from Darke County General Health District Septage Haulers PDF dated 1 April 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Darke County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Darke County General Health District’s PDF <cite>Septage Haulers</cite> (<code>SEWAGE-TREATMENT-04-1-2026HAULERS.pdf</code>, footer 1 April 2026). Companies that haul septage in Darke County must register with the health district. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 24 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">SEWAGE-TREATMENT-04-1-2026HAULERS.pdf</a>. Parent page: <a href="{e(PARENT_URL)}">Sewage Contractor Registrations</a>. Program: <a href="{e(PROGRAM_URL)}">Sewage Treatment Systems</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Darke County septage-hauler registration only. ODH bond status is <strong>unknown</strong> on this PDF.</p>
      <p>The PDF prints <strong>{n} TOTAL</strong> (footer 04/01/2026 on each page). Spellings are as printed (including <code>BOOSO'S</code>, <code>FLATTER'S</code>, <code>FRECH'S</code>, <code>MIKE'S</code>). <code>ARTZ SEPTIC SERVICES</code> phone is kept as printed (<code>1-459-996-6</code> — truncated on the PDF text layer); street line prints <code>GREENVILLE NASHVILLE</code> with no Rd/St suffix. <code>MT SERVICES INC</code> operator line prints <code>MILLER PORTABLES</code>; <code>PORTA KLEEN</code> operator line prints singular <code>SERVICE</code>. No registration numbers appear on this PDF.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="butler.html">Butler County haulers</a> · <a href="clark.html">Clark County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Darke County General Health District, PDF dated 1 April 2026</caption>
      <thead><tr><th>Business</th><th>Operator</th><th>Address</th><th>Phone</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-darke-oh.json">data/haulers-darke-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, operators, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 24 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/darke.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

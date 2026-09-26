#!/usr/bin/env python3
"""Build Erie County OH septage haulers JSON + HTML from ECHD 31 Aug 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://eriehealthohio.com/wp-content/uploads/2026/09/HAULERS-LIST.pdf'
PARENT_URL = 'https://eriehealthohio.com/sewage-treatment/'
FORMS_URL = 'https://eriehealthohio.com/forms-codes/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-08-31'
RETRIEVED = '2026-09-25'
ARCHIVE = 'data/sources/erie-oh-2026-haulers-list.pdf'
ARCHIVE_TXT = 'data/sources/erie-oh-2026-haulers-list.txt'

# Hand-verified from pdftotext -layout of HAULERS-LIST.pdf
# (Erie County Health Department; footer 08/31/2026; page 2 prints 17 TOTAL).
# Linked from Sewage Treatment / Forms & Codes as Registered Septage Haulers.
# Spellings kept as printed (BLAKE'S; BURNETT'S; DARR'S; REISING SANITARION;
# ECONOMY … INC without trailing period; KURAS city blank before , OH).
RECORDS = [
    {'name': 'ABEL SANITARY SERVICE', 'operator': 'DAVID S. PINKERTON', 'phone': '1-440-967-7704', 'address': '10515 BERLIN ROAD BERLIN HEIGHTS, OH 44814'},
    {'name': 'ADKINS SANITATION LTD.', 'operator': 'JOHN ADKINS', 'phone': '1-419-332-2873', 'address': '2226 W GARRISON ST FREMONT, OH 43410'},
    {'name': "BLAKE'S SANITATION LTD", 'operator': 'RANDY BLAKE', 'phone': '1-419-929-0208', 'address': '220 SR 60 N NEW LONDON, OH 44851'},
    {'name': "BURNETT'S SEPTIC SERVICE", 'operator': 'ANTHONY REVEGLIA', 'phone': '1-440-355-5526', 'address': '120 COMMERCE DRIVE LAGRANGE, OH 44050'},
    {'name': "DARR'S CLEANING, INC.", 'operator': 'ROGER L. DARR', 'phone': '1-419-547-0410', 'address': '5089 CR 175 CLYDE, OH 43410'},
    {'name': 'DEWEY PELTON SEPTIC, LLC', 'operator': 'PATRICK JOHNSON JR', 'phone': '1-440-965-8919', 'address': '6803 SR 60 WAKEMAN, OH 44889'},
    {'name': 'DOUBLE FLUSH SEPTIC SERVICES', 'operator': 'SCOTT SCHOLZ', 'phone': '1-330-391-5551', 'address': '2481 REMSEN ROAD MEDINA, OH 44256'},
    {'name': 'ECONOMY DRAIN CLEANING & SEPTIC SERVICES, INC', 'operator': 'TATEUM JONES', 'phone': '1-440-963-9275', 'address': '3420 LIBERTY AVE VERMILION, OH 44089'},
    {'name': 'FLUSH PORTABLES LLC', 'operator': 'DUSTIN ANSTEAD', 'phone': '1-567-228-7786', 'address': '3715 S. COUNTY ROAD 198 GREEN SPRINGS, OH 44836'},
    {'name': 'FRANKLIN SANITATION LLC', 'operator': 'GREG FRANKLIN', 'phone': '1-419-433-5169', 'address': '1611 RYE BEACH ROAD HURON, OH 44839'},
    {'name': 'FRED LEWIS SEPTIC TANK SERVICE', 'operator': 'LINDA REED', 'phone': '1-440-774-1972', 'address': '16250 GIFFORD RD OBERLIN, OH 44074'},
    {'name': 'GARNER SANITATION SERVICES, INC.', 'operator': 'PHILLIP MYERS', 'phone': '1-800-473-3205', 'address': '2525 MONROE STREET SANDUSKY, OH 44870'},
    {'name': 'KURAS AERATION SYSTEMS, LLC', 'operator': 'JEFF KURAS', 'phone': '1-419-635-2353', 'address': '5875 W. HARBOR ROAD , OH'},
    {'name': 'MORRIS ENVIRONMENTAL AND SANITATION', 'operator': 'DYLAN MORRIS', 'phone': '1-440-420-5067', 'address': '36225 DETROIT RD #107 AVON, OH 44011'},
    {'name': 'PAUL FOX & SONS EXCAVATING', 'operator': 'PAUL FOX', 'phone': '1-419-609-9980', 'address': '3501 HAYES AVE SANDUSKY, OH 44870'},
    {'name': 'REISING SANITARION SERVICES', 'operator': 'JIM REISING', 'phone': '1-419-681-3596', 'address': '11306 MAIN RD BERLIN HEIGHTS, OH 44814'},
    {'name': 'UNITED RENTALS (NORTH AMERICA)', 'operator': 'LYNN VIZDOS', 'phone': '1-330-774-2507', 'address': '1050 KILLIAN RD AKRON, OH 44312'},
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
    assert len(RECORDS) == 17, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert 'Septage Haulers' in txt
    assert 'ERIE COUNTY' in txt
    assert '08/31/2026' in txt
    assert '17 TOTAL' in txt
    assert 'ABEL SANITARY SERVICE' in txt
    assert "BLAKE'S SANITATION LTD" in txt
    assert 'REISING SANITARION SERVICES' in txt
    assert 'ECONOMY DRAIN CLEANING & SEPTIC SERVICES, INC' in txt
    assert 'KURAS AERATION SYSTEMS, LLC' in txt
    assert 'DOUBLE FLUSH SEPTIC SERVICES' in txt
    assert 'FLUSH PORTABLES LLC' in txt
    assert 'GARNER SANITATION SERVICES, INC.' in txt
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
            'role': 'Erie County Health Department registered septage hauler',
            'operator': r['operator'] or None,
            'address': r['address'],
            'phone': r['phone'] or None,
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Erie County, Ohio',
        'source': {
            'publisher': 'Erie County Health Department',
            'title': 'Septage Haulers (HAULERS-LIST.pdf)',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'forms_url': FORMS_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': 'PDF footer 08/31/2026 on each page; page 2 prints 17 TOTAL; CreationDate 31 August 2026 UTC; linked from Sewage Treatment / Forms & Codes as Registered Septage Haulers',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Erie County Health Department Septage Haulers PDF '
                '(HAULERS-LIST.pdf; footer 08/31/2026; 17 TOTAL). '
                'Spellings kept as printed including BLAKE\'S, BURNETT\'S, DARR\'S, '
                'REISING SANITARION SERVICES, and ECONOMY DRAIN CLEANING & SEPTIC SERVICES, INC '
                '(no trailing period after INC on the PDF text layer). '
                'KURAS AERATION SYSTEMS, LLC city line prints blank before ", OH". '
                'No registration numbers on this PDF. ODH statewide bond status is not on this PDF (marked unknown). '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Erie County Health Department and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-erie-oh.json'
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
  <title>Erie County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Erie County, Ohio registered septage haulers from Erie County Health Department Septage Haulers PDF dated 31 August 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Erie County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Erie County Health Department’s PDF <cite>Septage Haulers</cite> (<code>HAULERS-LIST.pdf</code>, footer 31 August 2026). Companies that haul septage in Erie County must register with the health department. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 25 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">HAULERS-LIST.pdf</a>. Parent page: <a href="{e(PARENT_URL)}">Sewage Treatment</a>. Forms directory: <a href="{e(FORMS_URL)}">Forms &amp; Codes</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Erie County septage-hauler registration only. ODH bond status is <strong>unknown</strong> on this PDF.</p>
      <p>The PDF prints <strong>{n} TOTAL</strong> (footer 08/31/2026 on each page). Spellings are as printed (including <code>BLAKE'S</code>, <code>BURNETT'S</code>, <code>DARR'S</code>, <code>REISING SANITARION SERVICES</code>). <code>ECONOMY DRAIN CLEANING &amp; SEPTIC SERVICES, INC</code> is kept without a trailing period after <code>INC</code> (as on the PDF text layer). <code>KURAS AERATION SYSTEMS, LLC</code> city line prints blank before <code>, OH</code>. No registration numbers appear on this PDF.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="darke.html">Darke County haulers</a> · <a href="seneca.html">Seneca County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Erie County Health Department, PDF dated 31 August 2026</caption>
      <thead><tr><th>Business</th><th>Operator</th><th>Address</th><th>Phone</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-erie-oh.json">data/haulers-erie-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, operators, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 25 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/erie.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

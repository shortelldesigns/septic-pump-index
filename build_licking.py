#!/usr/bin/env python3
"""Build Licking County OH septage haulers JSON + HTML from LCHD 12 Feb 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://lickingcohealth.org/wp-content/uploads/2026/02/sewage-treatment-haulers-02-12-2026.pdf'
PARENT_URL = 'https://lickingcohealth.org/sewage/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-02-12'
RETRIEVED = '2026-09-14'
ARCHIVE = 'data/sources/licking-oh-2026-septage-haulers-02-12.pdf'
ARCHIVE_TXT = 'data/sources/licking-oh-2026-septage-haulers-02-12.txt'

# Hand-verified from pdftotext -layout of sewage-treatment-haulers-02-12-2026.pdf
# (PDF CreationDate 12 February 2026 UTC; footer 02/12/2026; linked from LCHD Sewage as Septic Haulers).
# Spellings kept as printed (BANK SANITATION,LLC; ERICSON ENVIRONMENTAL SERVI truncated; BUCKHILL RD).
RECORDS = [
    {'name': 'A & B SANITATION INC', 'operator': 'JEREMY HUBBARD', 'phone': '1-614-471-8060', 'address': 'PO BOX 358, SUNBURY, OH 43074'},
    {'name': 'ACE SEPTIC TANK CLEANING INC.', 'operator': 'NORMAN BAUMAN/ COLT', 'phone': '1-614-491-2121', 'address': '4210 GROVEPORT, COLUMBUS, OH 43207'},
    {'name': 'AFFORDABLE WASTE SERVICES LLC', 'operator': 'JASON A TOWNSEND', 'phone': '1-740-366-7624', 'address': 'PO BOX 39, PATASKALA, OH 43062'},
    {'name': "AUSTIN'S SEPTIC LLC", 'operator': 'AUSTIN THORPE', 'phone': '1-614-961-9859', 'address': '81 E. COLLEGE AVE, JOHNSTOWN, OH 43031'},
    {'name': 'BANK SANITATION,LLC', 'operator': 'RICHARD D BANK', 'phone': '1-740-397-2595', 'address': '10560 BUTCHER ROAD, MT VERNON, OH 43050'},
    {'name': "BIG AL'S SEPTIC TANK SERVICE, LLC", 'operator': 'DON WISEMAN', 'phone': '1-740-745-1358', 'address': '18600 BUCKHILL RD, FRAZEYSBURG, OH 43822'},
    {'name': 'BO-MIC ENTERPRISE INC. DBA BSS WASTE', 'operator': 'KIM LANNING', 'phone': '1-740-756-9100', 'address': 'PO BOX 879, LOGAN, OH 43138'},
    {'name': 'BUCKEYE PLUMBING & DRAINS LLC', 'operator': 'KEVIN EDMUNDS', 'phone': '1-614-686-5001', 'address': '10385 CREAMER ROAD, ORIENT, OH 43146'},
    {'name': 'CHANDLER SEPTIC & SERVICES LLC', 'operator': 'ZACK CHANDLER', 'phone': '1-740-877-9605', 'address': '2300 ASPEN RD, FRAZEYSBURG, OH 43822'},
    {'name': 'CPR DRAIN CLEANING INC', 'operator': 'DAVID & KENNETH', 'phone': '1-614-279-3445', 'address': '2168 EAKIN RD, COLUMBUS, OH 43223'},
    {'name': 'DARBY CREEK SEPTIC LLC', 'operator': 'BRANDON YODER', 'phone': '1-614-915-6362', 'address': '5885 LAFAYETTE PLAIN CITY RD, LONDON, OH 43140'},
    {'name': 'ECB NORWALK DBA E.C. BABBERT', 'operator': 'E. C. BABBERT', 'phone': '1-614-837-8444', 'address': '7415 DILEY ROAD, CANAL WINCHESTER, OH 43110'},
    {'name': 'ELITE SEPTIC SERVICES, LLC', 'operator': 'WILL BURCHFIELD', 'phone': '1-740-654-8742', 'address': '1322 COLLINS RD NW, LANCASTER, OH 43130'},
    {'name': 'EMERSON PORTABLES', 'operator': 'LEE EMERSON', 'phone': '1-740-819-4254', 'address': '7215 JONES RD, NASHPORT, OH 43830'},
    {'name': 'ERIC J BAUMAN DBA ERICSON ENVIRONMENTAL SERVI', 'operator': 'ERIC BAUMAN', 'phone': '1-614-874-7585', 'address': 'PO BOX 266, GALLOWAY, OH 43119'},
    {'name': 'GOT 2 GO PORTABLE SANITATION LLC', 'operator': 'LARRON PERRY', 'phone': '1-614-701-7287', 'address': '1846 FEDERAL PKWY, COLUMBUS, OH 43207'},
    {'name': "GUY YINGER DBA YINGER CONST CO., BOB'S SEPTIC", 'operator': 'GUY YINGER', 'phone': '1-614-206-0095', 'address': 'P O BOX 359, SUNBURY, OH 43074'},
    {'name': 'HOEKSTRA LLC DBA ALL-STAR SEPTIC', 'operator': 'JAMES M HOEKSTRA', 'phone': '1-740-323-2606', 'address': '4940 BROWNSVILLE RD SE, NEWARK, OH 43056'},
    {'name': "JACK'S SEPTIC TANK CLEANING & CONST INC", 'operator': 'MANUEL DIAZ', 'phone': '1-740-366-3255', 'address': '274 S 6TH STREET, NEWARK, OH 43055'},
    {'name': 'JUDGES SANITATION LLC', 'operator': 'HERMAN E BERK JR', 'phone': '1-614-855-3361', 'address': '10745 FANCHER ROAD, WESTERVILLE, OH 43082'},
    {'name': 'MILLER PORTABLES', 'operator': 'ANDREW MILLER', 'phone': '1-800-827-6808', 'address': '2680 CR 168, DUNDEE, OH 44624'},
    {'name': 'OHIO CAST STONE CO', 'operator': 'ALAN CLEARY', 'phone': '-614-444-2778', 'address': '8548 DUVALL RD, ASHVILLE, OH 43103'},
    {'name': 'ON-SITE SANITATION, LLC', 'operator': 'CHAD SIMS', 'phone': '1-740-393-1181', 'address': '18001 MURRAY ROAD, MOUNT VERNON, OH 43050'},
    {'name': 'PRO KLEEN IND. SERVICES, INC. DBA PORTA KLEEN', 'operator': 'AMANDA NEIGHBORGALL', 'phone': '1-740-689-1886', 'address': '1030 MILL PARK DRIVE, LANCASTER, OH 43130'},
    {'name': 'RELIABLE ONSITE SERVICES', 'operator': 'UNITED RENTALS', 'phone': '1-614-202-3757', 'address': '1760 FEDDERN AVE, GROVE CITY, OH 43123'},
    {'name': 'RENT-A-JOHN PORTABLE SANITATION', 'operator': 'RENT-A-JOHN', 'phone': '1-614-497-1776', 'address': 'P O BOX 753, COLUMBUS, OH 43216'},
    {'name': 'THE DRAIN GUYS LLC', 'operator': 'JEREMY STUMP', 'phone': '1-614-946-0225', 'address': '6520 OLEY SPEAKS WAY STE B, CANAL WINCHESTER, OH 43110'},
    {'name': 'THE WATERWORKS, LLC', 'operator': 'TIM CAIN', 'phone': '1-614-876-0999', 'address': '550 SCHROCK RD, COLUMBUS, OH 43229'},
    {'name': "TIDY TIM'S INC", 'operator': 'TIMOTHY HACK', 'phone': '1-419-947-3121', 'address': '6434 CO RD 100, MOUNT GILEAD, OH 43338'},
    {'name': 'TWO-TAC LLC DBA AMERI-CANS', 'operator': 'CHASE OBERFIELD', 'phone': '', 'address': '13200 MARNE ROAD, NEWARK, OH 43055'},
    {'name': 'UNITED SEPTIC SERVICES', 'operator': 'ANDREW HARPER', 'phone': '1-740-607-3217', 'address': '2595 VIRGINIA RIDGE RD, PHILO, OH 43771'},
    {'name': 'WAS PORTABLES LLC', 'operator': 'SETH ELLINGTON', 'phone': '1-740-366-1811', 'address': '1000 KELLER DRIVE, HEATH, OH 43056'},
    {'name': 'WELLS SEPTIC AND DRAIN LLC', 'operator': 'TAYLOR WELLS', 'phone': '1-740-524-3922', 'address': '1742 HOG BACK RD, SUNBURY, OH 43074'},
    {'name': 'ZEMBA BROS., INC.', 'operator': 'SCOTT ZEMBA', 'phone': '1-740-455-6468', 'address': '3401 EAST PIKE, ZANESVILLE, OH 43701'},
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
    assert len(RECORDS) == 34, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert 'Septage Haulers' in txt
    assert 'Licking County Health Department' in txt
    assert '02/12/2026' in txt
    assert '34 TOTAL' in txt
    assert 'ERICSON ENVIRONMENTAL SERVI' in txt
    assert 'TWO-TAC LLC DBA AMERI-CANS' in txt
    assert '-614-444-2778' in txt
    for r in RECORDS:
        assert r['name'][:28] in txt or r['name'].split(' DBA ')[0][:24] in txt, r['name']
        street = r['address'].split(',')[0]
        assert street in txt, street
        if r['phone']:
            assert r['phone'] in txt, r['phone']

    names = [r['name'] for r in RECORDS]
    assert len(names) == len(set(names)), 'duplicate names'

    records = []
    for r in RECORDS:
        records.append({
            'source_url': SOURCE_URL,
            'source_document_date': DOC_DATE,
            'retrieved': RETRIEVED,
            'name': r['name'],
            'role': 'Licking County Health Department registered septage hauler',
            'operator': r['operator'],
            'address': r['address'],
            'phone': r['phone'] or None,
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Licking County, Ohio',
        'source': {
            'publisher': 'Licking County Health Department',
            'title': 'Septage Haulers (sewage-treatment-haulers-02-12-2026.pdf)',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': 'PDF footer 02/12/2026 on each page; CreationDate 12 February 2026 UTC; linked from Sewage Treatment Program as Septic Haulers; page 4 prints 34 TOTAL',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Licking County Health Department Septage Haulers PDF '
                '(sewage-treatment-haulers-02-12-2026.pdf; footer 02/12/2026; 34 TOTAL). '
                'Spellings kept as printed including BANK SANITATION,LLC; truncated ERIC J BAUMAN DBA ERICSON ENVIRONMENTAL SERVI; '
                'and phone printed as -614-444-2778 for OHIO CAST STONE CO. '
                'TWO-TAC LLC DBA AMERI-CANS has no phone on the PDF (marked unknown). '
                'No registration numbers on this PDF. ODH statewide bond status is not on this PDF (marked unknown). '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Licking County Health Department and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-licking-oh.json'
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
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Licking County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Licking County, Ohio registered septage haulers from Licking County Health Department PDF dated 12 February 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Licking County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Licking County Health Department’s PDF <cite>Septage Haulers</cite> (<code>sewage-treatment-haulers-02-12-2026.pdf</code>, footer 12 February 2026). Companies that haul septage in Licking County must register with the health district. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 14 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">sewage-treatment-haulers-02-12-2026.pdf</a>. Parent page: <a href="{e(PARENT_URL)}">Sewage Treatment Program</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Licking County septage-hauler registration only. ODH bond status is <strong>unknown</strong> on this PDF.</p>
      <p>The PDF prints <strong>{n} TOTAL</strong> (footer 02/12/2026 on each page). Spellings are as printed (including BANK SANITATION,LLC and truncated ERIC J BAUMAN DBA ERICSON ENVIRONMENTAL SERVI). Phone is missing on TWO-TAC LLC DBA AMERI-CANS — marked unknown. OHIO CAST STONE CO phone is kept as printed (<code>-614-444-2778</code>). No registration numbers appear on this PDF.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="marion.html">Marion County haulers</a> · <a href="delaware.html">Delaware County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Licking County Health Department, PDF dated 12 February 2026</caption>
      <thead><tr><th>Business</th><th>Operator</th><th>Address</th><th>Phone</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-licking-oh.json">data/haulers-licking-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, operators, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 14 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/licking.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

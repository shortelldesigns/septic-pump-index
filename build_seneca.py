#!/usr/bin/env python3
"""Build Seneca County OH septage haulers JSON + HTML from SCGHD 28 Apr 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://senecahealthdept.org/wp-content/uploads/2026/04/Septage-Haulers-2026.pdf'
PARENT_URL = 'https://senecahealthdept.org/environmental-health/home-sewage-treatment-systems/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-04-28'
RETRIEVED = '2026-09-19'
ARCHIVE = 'data/sources/seneca-oh-septage-haulers-2026.pdf'
ARCHIVE_TXT = 'data/sources/seneca-oh-septage-haulers-2026.txt'

# Hand-verified from pdftotext -layout of Septage-Haulers-2026.pdf
# (Seneca County General Health District; footer 04/28/2026; page 2 prints 16 TOTAL).
# Linked from Home Sewage Treatment Systems as Approved Septic Haulers 2026.
# Spellings kept as printed (ADKIN'S; GAHRINGS; -419-609-9980 leading dash;
# UNITED RENTALS (NORTH AMERICA), INC with RELIABLE ONSITE SERVICES on operator line).
# FLUSH PORTABLES LLC, T E PRICE INC, and UNITED RENTALS have no phone on the PDF.
# PAUL FOX & SONS EXCAVATING has no operator name line (phone only under name).
RECORDS = [
    {'name': "ADKIN'S SANITATION", 'operator': 'JOHN ADKINS', 'phone': '1-419-332-2873', 'address': '2226 W GARRISON FREMONT, OH 43420'},
    {'name': 'BARNETT EXCAVATING', 'operator': 'JOSEPH BARNETT', 'phone': '1-419-706-2452', 'address': '215 SANDUSKY ST PLYMOUTH, OH 44865'},
    {'name': "BUGNER'S SEWER & PORTABLE RESTROOMS", 'operator': 'NICK BUGNER OR HANK BUGNER', 'phone': '1-419-435-3977', 'address': '468 N SR 587/ PO BOX 230 FOSTORIA, OH 44830'},
    {'name': 'C & L SANITATION, INC.', 'operator': 'THOMAS L STANGE, PRESIDENT', 'phone': '1-419-874-4653', 'address': '27545 GLENWOOD RD, PO BOX 691 PERRYSBURG, OH 43552'},
    {'name': "DARR'S CLEANING", 'operator': 'ROGER DARR', 'phone': '1-419-547-0410', 'address': '5089 CO. RD. 175 CLYDE, OH 43410'},
    {'name': "DISTEL'S SEPTIC TANK SERVICES", 'operator': 'AARON DISTEL', 'phone': '1-419-448-0250', 'address': '30 ELLA STREET TIFFIN, OH 44883'},
    {'name': 'FLUSH PORTABLES LLC', 'operator': 'DUSTIN ANSTEAD', 'phone': '', 'address': '3715 S CR 198 GREEN SPRINGS, OH 44836'},
    {'name': 'GAHRINGS SEWER DRAIN', 'operator': 'MATTHEW GAHRING', 'phone': '1-419-933-1648', 'address': '16651 E TR 12 ATTICA, OH 44807'},
    {'name': 'GARNER SANITATION SERVICES', 'operator': 'PHILLIP MYERS', 'phone': '1-800-473-3205', 'address': '2525 W MONROE ST., PO BOX 1234 SANDUSKY, OH 44871'},
    {'name': "HOOVER'S SEPTIC TANK CLEANING", 'operator': 'RANDY HOOVER', 'phone': '1-419-937-2881', 'address': '1520 N. TWP. RD. 111 TIFFIN, OH 44883'},
    {'name': 'JB WALTER PORTABLE TOILETS', 'operator': 'BRADLEY J WALTER', 'phone': '1-419-694-7895', 'address': '18590 TR 155 MT BLANCHARD, OH 45867'},
    {'name': 'PAUL FOX & SONS EXCAVATING', 'operator': '', 'phone': '-419-609-9980', 'address': '3501 HAYES AVENUE SANDUSKY, OH 44870'},
    {'name': 'STIGER PRECAST INC.', 'operator': 'MIKE STIGER', 'phone': '1-740-482-2313', 'address': '17793 S.H. 231 NEVADA, OH 44849'},
    {'name': 'T E PRICE INC', 'operator': 'KEVIN AURAND', 'phone': '', 'address': '9758 REYNOLDS RD WAYNE, OH 43466'},
    {'name': 'THEIS SEPTIC', 'operator': 'CHARLES E THEIS', 'phone': '1-419-447-9149', 'address': '2729 E US 224 TIFFIN, OH 44883'},
    {'name': 'UNITED RENTALS (NORTH AMERICA), INC', 'operator': 'RELIABLE ONSITE SERVICES', 'phone': '', 'address': '1652 HOLLAND ROAD MAUMEE, OH 43537'},
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
    assert len(RECORDS) == 16, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert 'Septage Haulers' in txt
    assert 'Seneca County General Health District' in txt
    assert '04/28/2026' in txt
    assert '16 TOTAL' in txt
    assert "ADKIN'S SANITATION" in txt
    assert 'GAHRINGS SEWER DRAIN' in txt
    assert '-419-609-9980' in txt
    assert 'UNITED RENTALS (NORTH AMERICA), INC' in txt
    assert 'RELIABLE ONSITE SERVICES' in txt
    assert 'FLUSH PORTABLES LLC' in txt
    assert 'T E PRICE INC' in txt
    for r in RECORDS:
        assert r['name'][:28] in txt, r['name']
        street = r['address'].split()[0]
        assert street in txt, r['address']
        if r['phone']:
            assert r['phone'] in txt, r['phone']
        if r['operator']:
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
            'role': 'Seneca County General Health District registered septage hauler',
            'operator': r['operator'] or None,
            'address': r['address'],
            'phone': r['phone'] or None,
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Seneca County, Ohio',
        'source': {
            'publisher': 'Seneca County General Health District',
            'title': 'Septage Haulers 2026 (Septage-Haulers-2026.pdf)',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': 'PDF footer 04/28/2026 on each page; page 2 prints 16 TOTAL; linked from Home Sewage Treatment Systems as Approved Septic Haulers 2026',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Seneca County General Health District Septage Haulers PDF '
                '(Septage-Haulers-2026.pdf; footer 04/28/2026; 16 TOTAL). '
                'Spellings kept as printed including ADKIN\'S SANITATION, GAHRINGS SEWER DRAIN, '
                'and phone printed as -419-609-9980 for PAUL FOX & SONS EXCAVATING. '
                'FLUSH PORTABLES LLC, T E PRICE INC, and UNITED RENTALS (NORTH AMERICA), INC have no phone on the PDF (marked unknown). '
                'PAUL FOX & SONS EXCAVATING has no operator name line on the PDF. '
                'UNITED RENTALS operator line prints RELIABLE ONSITE SERVICES as on the PDF. '
                'No registration numbers on this PDF. ODH statewide bond status is not on this PDF (marked unknown). '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Seneca County General Health District and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-seneca-oh.json'
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
  <title>Seneca County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Seneca County, Ohio registered septage haulers from Seneca County General Health District Septage Haulers PDF dated 28 April 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Seneca County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Seneca County General Health District’s PDF <cite>Septage Haulers</cite> (<code>Septage-Haulers-2026.pdf</code>, footer 28 April 2026). Companies that haul septage in Seneca County must register with the health district. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 19 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">Septage-Haulers-2026.pdf</a>. Parent page: <a href="{e(PARENT_URL)}">Home Sewage Treatment Systems</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Seneca County septage-hauler registration only. ODH bond status is <strong>unknown</strong> on this PDF.</p>
      <p>The PDF prints <strong>{n} TOTAL</strong> (footer 04/28/2026 on each page). Spellings are as printed (including <code>ADKIN'S SANITATION</code> and <code>GAHRINGS SEWER DRAIN</code>). Phones are missing on <code>FLUSH PORTABLES LLC</code>, <code>T E PRICE INC</code>, and <code>UNITED RENTALS (NORTH AMERICA), INC</code> — marked unknown. PAUL FOX &amp; SONS EXCAVATING phone is kept as printed (<code>-419-609-9980</code>) and has no operator name line. No registration numbers appear on this PDF.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="marion.html">Marion County haulers</a> · <a href="licking.html">Licking County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Seneca County General Health District, PDF dated 28 April 2026</caption>
      <thead><tr><th>Business</th><th>Operator</th><th>Address</th><th>Phone</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-seneca-oh.json">data/haulers-seneca-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, operators, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 19 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/seneca.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

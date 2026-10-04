#!/usr/bin/env python3
"""Build Adams County OH septage haulers JSON + HTML from ACHD 16 Mar 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://www.adamscountyhealth.org/_files/ugd/4712a5_9ee0771923a34aae9b591c70da6841f6.pdf'
PARENT_URL = 'https://www.adamscountyhealth.org/septic-program'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-03-16'
RETRIEVED = '2026-10-03'
ARCHIVE = 'data/sources/adams-oh-2026-septage-haulers.pdf'
ARCHIVE_TXT = 'data/sources/adams-oh-2026-septage-haulers.txt'

# Hand-verified from pdftotext -layout of 4712a5_9ee0771923a34aae9b591c70da6841f6.pdf
# (Adams County Health Department; title Septage Haulers; HDIS; footer 03/16/2026;
# 10 TOTAL; 560 RICE DRIVE WEST UNION OH). Linked from Septic Program as Septage Hauler List.
# Spellings kept as printed (LITTLE'S SEPTIC SERVICE , INC with space before comma;
# R&A (PERTUSET) SEPTIC SOLUTIONS; RELIABLE ONSITE SERVCIES misspelling; LAUR FURLONG).
# Separate Installer List and Service Provider List on the same parent page are not used here.
RECORDS = [
    {'name': 'A-1 SEPTIC', 'operator': 'RYAN HANSON', 'phone': '1-740-703-7117', 'address': '741 BLACKSMITH HILL CHILLICOTHE, OH 45601'},
    {'name': 'AAA SANITATION', 'operator': 'JERRY JONES', 'phone': '1-937-549-3417', 'address': '1240 ISLAND CREEK ROAD MANCHESTER, OH 45144'},
    {'name': "DAY'S SANITATION", 'operator': 'MICHAEL DAY', 'phone': '1-937-549-2683', 'address': '518 E. 6TH STREET, P.O. BOX 193 MANCHESTER, OH 45144'},
    {'name': "LITTLE'S SEPTIC SERVICE , INC", 'operator': 'TRAVIS LITTLE', 'phone': '1-740-574-2033', 'address': '239 CLAY STREET WHEELERSBURG, OH 45694'},
    {'name': 'PROFLO SEPTIC SERVICE', 'operator': 'RYAN HESLER', 'phone': '1-937-681-0292', 'address': '1457 STATE ROUTE 348 WEST UNION, OH 45693'},
    {'name': 'R&A (PERTUSET) SEPTIC SOLUTIONS', 'operator': 'R&A SEPTIC SOLUTIONS, LLC', 'phone': '1-937-587-2427', 'address': 'PO BOX 425, 6260 OLD STATE ROUTE 32 PEEBLES, OH 45660'},
    {'name': 'RUMPKE TRANSPORTATION CO., LLC', 'operator': 'LAUR FURLONG', 'phone': '1-937-378-4126', 'address': '3990 GENERATION DRIVE CINCINNATI, OH 45251'},
    {'name': 'SOUTHERN OHIO SEPTAGE SOLUTIONS', 'operator': 'CODY SPRIGGS', 'phone': '1-937-217-8676', 'address': '445 LLOYD RD WEST UNION, OH 45693'},
    {'name': 'UNITED RENTALS (NORTH AMERICA), INC', 'operator': 'RELIABLE ONSITE SERVCIES', 'phone': '1-513-288-2280', 'address': '4838 SPRING GROVE AVENUE CINCINNATI, OH 45232'},
    {'name': 'XTREME CLEAN & WATER RESTORATION LLC', 'operator': 'JENNY CARRINGTON', 'phone': '1-513-739-9531', 'address': '7336 FREE SOIL RD GEORGETOWN, OH 45121'},
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
    assert len(RECORDS) == 10, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert 'Septage Haulers' in txt
    assert 'Adams County Health Department' in txt
    assert '03/16/2026' in txt
    assert '10 TOTAL' in txt
    assert '560 RICE DRIVE' in txt
    assert 'A-1 SEPTIC' in txt
    assert 'AAA SANITATION' in txt
    assert "DAY'S SANITATION" in txt
    assert "LITTLE'S SEPTIC SERVICE , INC" in txt
    assert 'PROFLO SEPTIC SERVICE' in txt
    assert 'R&A (PERTUSET) SEPTIC SOLUTIONS' in txt
    assert 'RUMPKE TRANSPORTATION CO., LLC' in txt
    assert 'SOUTHERN OHIO SEPTAGE SOLUTIONS' in txt
    assert 'UNITED RENTALS (NORTH AMERICA), INC' in txt
    assert 'XTREME CLEAN & WATER RESTORATION LLC' in txt
    assert 'RELIABLE ONSITE SERVCIES' in txt
    assert 'LAUR FURLONG' in txt
    for r in RECORDS:
        assert r['name'] in txt, r['name']
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
            'role': 'Adams County Health Department registered septage hauler',
            'operator': r['operator'] or None,
            'address': r['address'],
            'phone': r['phone'] or None,
            'local_reg': 'unknown',
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Adams County, Ohio',
        'source': {
            'publisher': 'Adams County Health Department',
            'title': 'Septage Haulers',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': (
                'PDF title prints Septage Haulers; HDIS footer 03/16/2026; 10 TOTAL; '
                'CreationDate 16 March 2026 UTC; linked from Septic Program as Septage Hauler List. '
                'Business, operator, address, and phone printed; no local REG # on this PDF.'
            ),
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'archive_txt': ARCHIVE_TXT,
            'limitations': (
                'Transcribed from Adams County Health Department PDF '
                '4712a5_9ee0771923a34aae9b591c70da6841f6.pdf (linked from '
                'https://www.adamscountyhealth.org/septic-program as Septage Hauler List). '
                '10 TOTAL named haulers (footer 03/16/2026). Spellings kept as printed including '
                "LITTLE'S SEPTIC SERVICE , INC (space before comma), R&A (PERTUSET) SEPTIC SOLUTIONS, "
                'operator line R&A SEPTIC SOLUTIONS, LLC, RELIABLE ONSITE SERVCIES (misspelling as printed), '
                'and LAUR FURLONG. No local registration numbers on this PDF (local REG marked unknown). '
                'ODH statewide bond status is not on this PDF (marked unknown). Separate Installer List '
                'and Service Provider List on the same parent page were not used for this hauler table. '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Adams County Health Department '
                'and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-adams-oh.json'
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
            + '<td class="unknown">unknown</td>'
            + '</tr>'
        )

    n = len(records)
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Adams County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Adams County, Ohio registered septage haulers from Adams County Health Department Septage Haulers PDF dated 16 March 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Adams County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Adams County Health Department’s PDF <cite>Septage Haulers</cite> (HDIS list, footer 16 March 2026, 10 TOTAL). Companies that haul septage in Adams County must register with the health department. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 3 October 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">Septage Hauler List PDF</a>. Parent page: <a href="{e(PARENT_URL)}">Septic Program</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Adams County septage-hauler registration only. Local REG # and ODH bond status are <strong>unknown</strong> on this PDF (no registration numbers printed).</p>
      <p>The PDF prints <strong>{n} TOTAL</strong> (footer 03/16/2026). Spellings are as printed (including <code>LITTLE'S SEPTIC SERVICE , INC</code> with a space before the comma, <code>R&amp;A (PERTUSET) SEPTIC SOLUTIONS</code>, operator <code>RELIABLE ONSITE SERVCIES</code> as misspelled on the PDF, and <code>LAUR FURLONG</code>). The same Septic Program parent page also links an Installer List and a Service Provider List — those lists are separate credentials and are not merged into this hauler table.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="morgan.html">Morgan County haulers</a> · <a href="ashland.html">Ashland County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Adams County Health Department, PDF dated 16 March 2026</caption>
      <thead><tr><th>Business</th><th>Operator</th><th>Address</th><th>Phone</th><th>Local REG #</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-adams-oh.json">data/haulers-adams-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, operators, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 3 October 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/adams.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

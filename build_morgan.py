#!/usr/bin/env python3
"""Build Morgan County OH registered septage haulers JSON + HTML from MCHD 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://morganpublichealth.org/wp-content/uploads/2026/01/2026-registered-septage-haulers.pdf'
PARENT_URL = 'https://morganpublichealth.org/septic/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-01-27'
RETRIEVED = '2026-10-02'
ARCHIVE = 'data/sources/morgan-oh-2026-registered-septage-haulers.pdf'
ARCHIVE_TXT = 'data/sources/morgan-oh-2026-registered-septage-haulers.txt'

# Hand-verified from pdftotext -layout of 2026-registered-septage-haulers.pdf
# (Morgan County Health Department; title 2026 Registered Septage Haulers;
# CreationDate 27 January 2026; linked from Septic page as 2026 Registered Septage Haulers).
# Name + phone only on this PDF (no address, operator, or local REG #).
# Spellings kept as printed (Sickles; Pro Kleen; Jones Jons LLC; Haas Septic & Portable Toilets).
# Separate STS Installers and Service Providers PDFs on the same parent page are not used here.
RECORDS = [
    {'name': 'Fouss Septic Systems', 'phone': '740-896-2425'},
    {'name': 'Sickles Sanitation', 'phone': '740-592-3480'},
    {'name': 'Pro Kleen Industrial Services', 'phone': '740-689-1886'},
    {'name': 'Myers Septic Service', 'phone': '740-423-9323'},
    {'name': 'United Septic Services', 'phone': '740-607-3217'},
    {'name': 'Emerson Portables', 'phone': '740-819-4254'},
    {'name': 'Eagle Eye Septic', 'phone': '740-454-7867'},
    {'name': 'Jones Jons LLC', 'phone': '740-260-8084'},
    {'name': 'Haas Septic & Portable Toilets', 'phone': '740-891-1010'},
    {'name': 'Zemba Brothers', 'phone': '740-452-1880'},
    {'name': 'Irwin Property Services', 'phone': '740-591-6243'},
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
    assert len(RECORDS) == 11, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert 'Morgan County Health Department' in txt
    assert '2026 Registered Septage Haulers' in txt
    assert 'Fouss Septic Systems' in txt
    assert 'Sickles Sanitation' in txt
    assert 'Pro Kleen Industrial Services' in txt
    assert 'Jones Jons LLC' in txt
    assert 'Haas Septic & Portable Toilets' in txt
    assert 'Zemba Brothers' in txt
    assert 'Irwin Property Services' in txt
    assert 'Eagle Eye Septic' in txt
    assert 'Emerson Portables' in txt
    for r in RECORDS:
        assert r['name'] in txt, r['name']
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
            'role': 'Morgan County Health Department registered septage hauler',
            'phone': r['phone'] or None,
            'local_reg': 'unknown',
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Morgan County, Ohio',
        'source': {
            'publisher': 'Morgan County Health Department',
            'title': '2026 Registered Septage Haulers',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': (
                'PDF title prints 2026 Registered Septage Haulers; path under '
                '/wp-content/uploads/2026/01/; CreationDate 27 January 2026; '
                'linked from Septic page as 2026 Registered Septage Haulers. '
                'Name and phone only — no address, operator, or local REG # on this PDF.'
            ),
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'archive_txt': ARCHIVE_TXT,
            'limitations': (
                'Transcribed from Morgan County Health Department PDF '
                '2026-registered-septage-haulers.pdf (linked from '
                'https://morganpublichealth.org/septic/ as 2026 Registered Septage Haulers). '
                '11 named haulers. Spellings kept as printed including Sickles Sanitation, '
                'Pro Kleen Industrial Services, Jones Jons LLC, and Haas Septic & Portable Toilets. '
                'No addresses, operators, or local registration numbers on this PDF '
                '(local REG marked unknown). ODH statewide bond status is not on this PDF '
                '(marked unknown). Separate 2026 Registered STS Installers and 2026 Registered '
                'Service Providers PDFs on the same parent page were not used for this hauler table. '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Morgan County Health Department '
                'and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-morgan-oh.json'
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        phone = r['phone'] or ''
        rows.append(
            '<tr>'
            f'<td>{e(r["name"])}</td>'
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
  <title>Morgan County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Morgan County, Ohio registered septage haulers from Morgan County Health Department 2026 Registered Septage Haulers PDF (CreationDate 27 January 2026). Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Morgan County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Morgan County Health Department’s PDF <cite>2026 Registered Septage Haulers</cite> (<code>2026-registered-septage-haulers.pdf</code>, CreationDate 27 January 2026). Companies that haul septage in Morgan County must register with the health department. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 2 October 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">2026-registered-septage-haulers.pdf</a>. Parent page: <a href="{e(PARENT_URL)}">Septic</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Morgan County septage-hauler registration only. Local REG # and ODH bond status are <strong>unknown</strong> on this PDF (name and phone only).</p>
      <p>The PDF lists <strong>{n}</strong> named haulers. Spellings are as printed (including <code>Sickles Sanitation</code>, <code>Pro Kleen Industrial Services</code>, <code>Jones Jons LLC</code>, and <code>Haas Septic &amp; Portable Toilets</code>). The same Septic parent page also links 2026 Registered STS Installers and 2026 Registered Service Providers — those lists are separate credentials and are not merged into this hauler table.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="muskingum.html">Muskingum County haulers</a> · <a href="ashland.html">Ashland County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Morgan County Health Department, 2026 PDF (CreationDate 27 January 2026)</caption>
      <thead><tr><th>Business</th><th>Phone</th><th>Local REG #</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-morgan-oh.json">data/haulers-morgan-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names and phones are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 2 October 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/morgan.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

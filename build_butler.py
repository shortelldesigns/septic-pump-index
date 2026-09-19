#!/usr/bin/env python3
"""Build Butler County OH registered septage haulers JSON + HTML from BCGHD 23 Jul 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://health.bcohio.gov/Documents/Environmental%20Health%20and%20Plumbing%20Services/Registered%20Professionals%207-23-26.pdf'
PARENT_URL = 'https://health.bcohio.gov/environmental_health_and_plumbing_services/sewage_and_private_water.php'
FORMS_URL = 'https://health.bcohio.gov/environmental_health_and_plumbing_services/forms.php'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-07-23'
RETRIEVED = '2026-09-18'
ARCHIVE = 'data/sources/butler-oh-registered-professionals-07-23-26.pdf'
ARCHIVE_TXT = 'data/sources/butler-oh-registered-professionals-07-23-26.txt'

# Hand-verified from pdftotext -layout of Registered Professionals 7-23-26.pdf
# (Butler County Board of Health / Butler County Health District).
# SEPTAGE HAULER section only — SERVICE PROVIDER and INSTALLER sections omitted.
# Spellings kept as printed (LANSCAPING; AMERICIA; NORTH AMERICIA with space after '(';
# Attn: Melissa; Harrison, Ohio; West College Corner, Indiana).
# EXNIL GREASE LLC and TRENTELS have no phone on the PDF.
# EXNIL hauler row prints CINCINNATI, OH with no ZIP (ZIP 45214 appears only on the service-provider row — not copied here).
# Local Bond Company column is not ODH statewide bond status (odh_bond marked unknown).
RECORDS = [
    {'reg': '11SH', 'name': '4 ACES PLUMBING & EXCAVATING, INC.', 'phone': '513-422-2772', 'address': '2500 Oxford State Road MIDDLETOWN, OH 45044'},
    {'reg': '16SH', 'name': 'A.K. BUTLER SERVICES', 'phone': '513-738-3902', 'address': 'Attn: Melissa P.O. Box 157 ROSS, OH 45061'},
    {'reg': '4SH', 'name': 'AAA WASTEWATER SERVICES INC. DBA TRIPLE A PRO SERVICES', 'phone': '937-746-6361', 'address': '3677 Anthony Lane FRANKLIN, OH 45005'},
    {'reg': '42SH', 'name': 'AARON ANDREWS SEPTIC SERVICE', 'phone': '513-625-0059', 'address': '5051 Eagles View Cincinnati, OH 45244'},
    {'reg': '35SH', 'name': 'ACE SANITATION SERVICE', 'phone': '513-353-2260', 'address': '4525 State Route 128 Cleves, OH 45002'},
    {'reg': '53SH', 'name': 'ALL REPAIR SEPTIC SERVICE', 'phone': '513-739-2417', 'address': '1780 STATE RT 232 NEW RICHMOND, OH 45157'},
    {'reg': '27SH', 'name': 'BLACK WATER SEPTIC PROS', 'phone': '513-623-1792', 'address': '2065 DECAMP ROAD HAMILTON, OH 45013'},
    {'reg': '33SH', 'name': 'BLUE LAGOON, INC.', 'phone': '513-608-6204', 'address': '3704 LOVELL AVENUE Cincinnati, OH 45211'},
    {'reg': '54SH', 'name': 'EXNIL GREASE LLC', 'phone': '', 'address': '2160 KINDEL AVE CINCINNATI, OH'},
    {'reg': '5SH', 'name': "GEORGE'S SEPTIC TANK & SEWER SERVICE", 'phone': '513-893-8995', 'address': '2061 Hamilton Richmond Road HAMILTON, OH 45013'},
    {'reg': '10SH', 'name': "JOHNNY'S A-1 SANITATION, LLC", 'phone': '513-464-0044', 'address': '4807 Wayne Madison Road TRENTON, OH 45067'},
    {'reg': '34SH', 'name': 'MULLIS SEPTIC SERVICES', 'phone': '513-446-0404', 'address': '5641 YEATMAN RD CINCINNATI, OH 45252'},
    {'reg': '41SH', 'name': 'PALM PORTABLE RESTROOMS', 'phone': '513-266-3604', 'address': '8028 W. Mill Street P.O. Box 622 Miamitown, OH 45041'},
    {'reg': '44SH', 'name': 'PERFECT-A-WASTE SEWAGE EQUIPMENT LLC', 'phone': '513-851-8886', 'address': '2106 W North Bend Rd Cincinnati, OH 45224'},
    {'reg': '28SH', 'name': 'PRIME PUMPING & SERVICES', 'phone': '937-533-7400', 'address': '4076 Edison Road Camden, OH 45311'},
    {'reg': '50SH', 'name': 'ROTO-ROOTER SERVICES COMPANY', 'phone': '937-353-7093', 'address': '9490 BYERS ROAD MIAMISBURG, OH 45342'},
    {'reg': '6SH', 'name': 'ROYAL ROOTER PLUMBING & DRAIN CLEANING, INC.', 'phone': '513-422-0819', 'address': '6165 Elk Creek Road MIDDLETOWN, OH 45042'},
    {'reg': '8SH', 'name': 'RUMPKE TRANSPORTATION COMPANY, LLC', 'phone': '513-245-7901 X7015', 'address': '3990 Generation Drive Attn: Laura CINCINNATI, OH 45251'},
    {'reg': '26SH', 'name': 'SAVINGS LIQUID WASTE, INC.', 'phone': '513-367-4196', 'address': 'P.O. Box 25 Harrison, Ohio 45030'},
    {'reg': '23SH', 'name': 'SEPTEK LLC', 'phone': '937-746-2663', 'address': '3101 Beal Road Franklin, OH 45005'},
    {'reg': '25SH', 'name': 'SPEEDY SEPTIC SERVICE, LLC', 'phone': '765-732-3248', 'address': '4766 East Sand Run Road West College Corner, Indiana 47003'},
    {'reg': '50DSH', 'name': 'TRENTELS DESIGN & LANSCAPING DBA TRENTELS PORTABLES', 'phone': '', 'address': '5225 GLENMINA DR DAYTON, OH 45440'},
    {'reg': '14SH', 'name': 'TRI-STATE LIQUID WASTE', 'phone': '513-353-3233', 'address': 'PO BOX 4070 LAWRENCEBURG, IN 47025'},
    {'reg': '46SH', 'name': 'UNITED RENTALS ( NORTH AMERICIA)', 'phone': '513-288-2280', 'address': '4838 SPRING GROVE AVE CINCINNATI, OH 45232'},
    {'reg': '3SH', 'name': 'WINELCO', 'phone': '513-755-8050', 'address': '6141 Centre Park Drive WEST CHESTER, OH 45069'},
]


def e(s):
    return html.escape(str(s), quote=True)


def phone_cell(printed):
    if not printed:
        return '<td class="phones unknown">unknown</td>'
    base = printed
    if 'ext' in printed.lower() or re.search(r'\sX\d', printed, re.I):
        base = re.split(r'\s*(?:ext\.?|X)\s*', printed, flags=re.I)[0]
    digits = re.sub(r'\D', '', base)
    if not digits:
        return '<td class="phones unknown">unknown</td>'
    href = f'+1{digits}' if len(digits) == 10 else f'+{digits}' if len(digits) == 11 and digits.startswith('1') else f'+1{digits}'
    return f'<td class="phones"><a href="tel:{href}">{e(printed)}</a></td>'


def main():
    assert len(RECORDS) == 25, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert 'SEPTAGE HAULER' in txt
    assert 'SERVICE PROVIDER' in txt
    # Ensure we stop before service providers — key hauler-only tokens
    hauler_block = txt.split('SERVICE PROVIDER')[0]
    assert 'AMERICIA' in hauler_block
    assert 'LANSCAPING' in hauler_block
    assert '50DSH' in hauler_block
    assert '513-245-7901 X7015' in hauler_block
    for r in RECORDS:
        assert r['reg'] in hauler_block, r['reg']
        # Multi-line names: check a distinctive fragment
        token = r['name'].split()[0].replace("'", '').replace('(', '')
        assert token in hauler_block or r['name'][:20] in hauler_block, r['name']
        if r['phone']:
            assert r['phone'] in hauler_block, r['phone']
        # Address street/token
        addr_token = r['address'].split()[0]
        if addr_token not in ('Attn:', 'P.O.', 'PO'):
            assert addr_token in hauler_block or r['address'][:12] in hauler_block, r['address']

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
            'role': 'Butler County Health District registered septage hauler',
            'address': r['address'],
            'phone': r['phone'] or None,
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Butler County, Ohio',
        'source': {
            'publisher': 'Butler County Board of Health / Butler County Health District',
            'title': 'Registered Professionals 7-23-26.pdf (SEPTAGE HAULER section)',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'forms_url': FORMS_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': 'PDF filename Registered Professionals 7-23-26.pdf; document-center listing on BCGHD forms and sewage pages; Crystal Reports PDF',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Butler County Health District Registered Professionals PDF dated 23 July 2026 '
                '(Registered Professionals 7-23-26.pdf). Full PDF lists SEPTAGE HAULER, SERVICE PROVIDER, and INSTALLER '
                'sections; this table includes only the 25 SEPTAGE HAULER rows. '
                'Spellings kept as printed including TRENTELS DESIGN & LANSCAPING, UNITED RENTALS ( NORTH AMERICIA), '
                'Attn: Melissa, Harrison Ohio, and West College Corner Indiana. '
                'EXNIL GREASE LLC and TRENTELS have no phone on the PDF. '
                'EXNIL hauler address prints CINCINNATI, OH with no ZIP. '
                'Rumpke phone kept as printed with X7015. Local license numbers (…SH / 50DSH) are as printed. '
                'The PDF Bond Company column is not ODH statewide bond verification (odh_bond marked unknown). '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Butler County Health District and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-butler-oh.json'
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        phone = r['phone'] or ''
        rows.append(
            '<tr>'
            f'<td>{e(r["registration_number"])}</td>'
            f'<td>{e(r["name"])}</td>'
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
  <title>Butler County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Butler County, Ohio registered septage haulers from Butler County Health District Registered Professionals PDF dated 23 July 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Butler County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Butler County Health District’s PDF <cite>Registered Professionals 7-23-26</cite> (dated 23 July 2026). Companies that haul septage in Butler County must register with the health district. We tabulated only the SEPTAGE HAULER section. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 18 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">Registered Professionals 7-23-26.pdf</a>. Sewage &amp; private water page: <a href="{e(PARENT_URL)}">Sewage and Private Water</a>. Forms listing: <a href="{e(FORMS_URL)}">Environmental Health forms</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Butler County septage-hauler registration only. ODH bond status is <strong>unknown</strong> on this PDF (the Bond Company column is not ODH verification).</p>
      <p>The PDF lists <strong>{n}</strong> SEPTAGE HAULER rows (filename dated 7-23-26). SERVICE PROVIDER and INSTALLER sections are omitted. Spellings kept as printed (including <code>LANSCAPING</code>; <code>UNITED RENTALS ( NORTH AMERICIA)</code>; <code>Attn: Melissa</code>). <code>EXNIL GREASE LLC</code> and <code>TRENTELS</code> have no phone on the PDF. EXNIL hauler address prints Cincinnati with no ZIP. Rumpke phone kept as printed with <code>X7015</code>.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="summit.html">Summit County haulers</a> · <a href="clark.html">Clark County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Butler County Health District, PDF dated 23 July 2026</caption>
      <thead><tr><th>License #</th><th>Business</th><th>Address</th><th>Phone</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-butler-oh.json">data/haulers-butler-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, license numbers, phones, and addresses are as printed on the county PDF (SEPTAGE HAULER section only).</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 18 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/butler.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Build Summit County OH registered septage haulers JSON + HTML from SCPH 2 Sept 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://scph.link/STS_Contractors'
PARENT_URL = 'https://www.scph.org/water-quality/operation-permits'
PROGRAM_URL = 'https://www.scph.org/water-quality/sts-contractor'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-09-02'
RETRIEVED = '2026-09-17'
ARCHIVE = 'data/sources/summit-oh-2026-sts-registered-contractors-09-02.pdf'
ARCHIVE_TXT = 'data/sources/summit-oh-2026-sts-registered-contractors-09-02.txt'

# Hand-verified from Summit County Public Health printable PDF
# (scph.link/STS_Contractors → Google Sheets publish PDF titled
# "2026 STS Registered Contractors List - Table 1.pdf", Updated: 9/2/26).
# Only rows with Septage Hauler = Y (installer-only / service-provider-only omitted).
# Street addresses are not on this PDF — City column only. Spellings/spacing kept as printed
# (including POPS SEPTIC &  DRAIN SERVICE double space; WERAB ENTERPRISES / FRED'S SEPTIC;
# SKELLEY SEPTIC & WELL INSPECTIONS; CLN PORTABLE RESTROOM; DANIEL ODY / MIKE NEWELL).
RECORDS = [
    {'name': 'ALL TOWN & COUNTRY SEPTIC', 'contact': 'TY BLANKENSHIP', 'phone': '330-745-2277', 'city': 'NORTON'},
    {'name': 'ALLEN DRAIN SERVICE', 'contact': 'SARA GLESS', 'phone': '330-673-6482', 'city': 'KENT'},
    {'name': 'ARIS COMPANY', 'contact': 'MIKE SKOLARIS', 'phone': '330-562-8300', 'city': 'CHAGRIN FALLS'},
    {'name': 'A ROOTER MAN', 'contact': 'JAMES ENGLISH', 'phone': '877-232-1520', 'city': 'TALLMADGE'},
    {'name': 'ATOMIC SEWER', 'contact': 'GUY WEISEL', 'phone': '330-492-1000', 'city': 'MIDDLEBRANCH'},
    {'name': 'BOSLEY DRAIN & SEPTIC', 'contact': 'JOSHUA PAUL TULLY', 'phone': '330-454-4000', 'city': 'LOUISVILLE'},
    {'name': 'CLN PORTABLE RESTROOM', 'contact': 'SCOTT HOAR', 'phone': '440-821-0114', 'city': 'BURTON'},
    {'name': 'CLP SERVICES', 'contact': 'XAVIER BURGSTALLER', 'phone': '330-716-3272', 'city': 'BOLIVAR'},
    {'name': 'COWBOY MILLER SEPTIC PUMPING', 'contact': 'SHERI BROWN', 'phone': '330-821-8060', 'city': 'DEERFIELD'},
    {'name': 'DOUBLE FLUSH SEPTIC SERVICE', 'contact': 'SCOTT SCHOLZ', 'phone': '330-391-5551', 'city': 'MEDINA'},
    {'name': 'DOWNS SEPTIC & DRAIN', 'contact': 'LAURIE METZ', 'phone': '330-535-5386', 'city': 'STOW'},
    {'name': 'DYNAMERICAN', 'contact': 'KEVIN CHURCH', 'phone': '330-666-8863', 'city': 'MEDINA'},
    {'name': 'GOLD-N-DEUCE', 'contact': 'BRIAN MYERS', 'phone': '330-581-8541', 'city': 'DELLROY'},
    {'name': 'HUMBERT SANITARY SERVICE', 'contact': 'MIKE HUMBERT', 'phone': '330-494-3000', 'city': 'NORTH CANTON'},
    {'name': 'JARVIS SEPTIC & DRAIN', 'contact': 'RYAN MORRIS', 'phone': '330-336-1893', 'city': 'WADSWORTH'},
    {'name': "KING'S SANITARY SERVICES", 'contact': 'REX KING JR', 'phone': '330-372-3201', 'city': 'BRISTOLVILLE'},
    {'name': 'KLARICH FARMS', 'contact': 'FRANK KLARICH', 'phone': '440-285-2550', 'city': 'BURTON'},
    {'name': 'LEHMAN DRAIN', 'contact': 'SONIA LEHMAN', 'phone': '234-322-5766', 'city': 'HARTVILLE'},
    {'name': 'MILLER PORTABLES', 'contact': 'ANDREW MILLER', 'phone': '800-827-6808', 'city': 'BERLIN'},
    {'name': 'MILLER SEPTIC', 'contact': 'SETH MILLER', 'phone': '330-893-2355', 'city': 'BERLIN'},
    {'name': 'PATTERSON SPECIALTY SERVICES', 'contact': 'LYNETTE BURKE', 'phone': '330-862-3371', 'city': 'WAYNESBURG'},
    {'name': 'POPS SEPTIC &  DRAIN SERVICE', 'contact': 'BRAD WAYBRIGHT', 'phone': '330-854-2021', 'city': 'CANAL FULTON'},
    {'name': 'RELIABLE ONSITE SERVICES', 'contact': 'LYNN VIZDOS', 'phone': '330-733-9000', 'city': 'AKRON'},
    {'name': 'SEPTICLEAN', 'contact': 'MATT WOODFORD', 'phone': '330-428-1918', 'city': 'DEERFIELD'},
    {'name': 'SKELLEY SEPTIC & WELL INSPECTIONS', 'contact': 'BEN SKELLEY', 'phone': '330-267-8485', 'city': 'BOLIVAR'},
    {'name': 'SPEEDIE SEPTIC & SEWER', 'contact': 'NANCY CREGAN', 'phone': '330-878-6042', 'city': 'STRASBURG'},
    {'name': 'SUBURBAN SEPTIC SERVICE', 'contact': 'PATRICK VALENTINE', 'phone': '330-722-4262', 'city': 'MEDINA'},
    {'name': 'SUFFIELD SEPTIC SERVICE', 'contact': 'JULIE PHILLIP', 'phone': '330-699-9186', 'city': 'MOGADORE'},
    {'name': 'SUMMIT EXCAVATING', 'contact': 'MARIE EASTERLING', 'phone': '330-825-2035', 'city': 'CLINTON'},
    {'name': 'SUPECK SEPTIC SERVICES', 'contact': 'TIM SUPECK', 'phone': '888-725-0209', 'city': 'MEDINA'},
    {'name': 'SUPERIOR DRAINAGE & PLUMBING', 'contact': 'DANIEL ODY / MIKE NEWELL', 'phone': '330-753-7711', 'city': 'AKRON'},
    {'name': 'WALT KUCHARSKI SEPTIC SERVICE', 'contact': 'WALTER CLAY KUCHARSKI', 'phone': '440-232-0767', 'city': 'RICHFIELD'},
    {'name': "WERAB ENTERPRISES / FRED'S SEPTIC", 'contact': 'CHAD J. WERAB', 'phone': '330-947-9902', 'city': 'ATWATER'},
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
    assert len(RECORDS) == 33, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert 'Updated: 9/2/26' in txt
    assert 'Summit County Public Health' in txt
    assert 'Sewage Treatment System Contractors' in txt
    assert 'Septage' in txt and 'Hauler' in txt
    for r in RECORDS:
        assert r['phone'] in txt, r['phone']
        assert r['contact'] in txt, r['contact']
        assert r['city'] in txt, r['city']
        # Wrapped names appear across lines — check first significant token
        token = r['name'].split()[0].replace("'", '')
        assert token in txt or r['name'][:18] in txt, r['name']
    assert 'POPS SEPTIC' in txt
    assert 'SKELLEY SEPTIC' in txt
    assert "WERAB ENTERPRISES / FRED'S" in txt or 'WERAB ENTERPRISES' in txt
    assert 'DANIEL ODY / MIKE NEWELL' in txt

    names = [r['name'] for r in RECORDS]
    assert len(names) == len(set(names)), 'duplicate names'

    records = []
    for r in RECORDS:
        records.append({
            'source_url': SOURCE_URL,
            'source_document_date': DOC_DATE,
            'retrieved': RETRIEVED,
            'name': r['name'],
            'role': 'Summit County Public Health registered septage hauler',
            'operator': r['contact'],
            'city': r['city'],
            'phone': r['phone'] or None,
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Summit County, Ohio',
        'source': {
            'publisher': 'Summit County Public Health',
            'title': '2026 STS Registered Contractors List (Updated: 9/2/26)',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'program_url': PROGRAM_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': 'PDF header Updated: 9/2/26; official printable PDF linked as scph.link/STS_Contractors from Operation Permits / Homeowner Resources / STS Contractor pages; Google Sheets publish export filename 2026 STS Registered Contractors List - Table 1.pdf',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Summit County Public Health 2026 STS Registered Contractors List '
                '(Updated: 9/2/26). Full PDF lists installers, service providers, and septage haulers; '
                'this table includes only the 33 rows with Septage Hauler = Y. '
                'Street addresses are not on this PDF (City column only). '
                'Spellings and spacing kept as printed including POPS SEPTIC &  DRAIN SERVICE (double space), '
                "WERAB ENTERPRISES / FRED'S SEPTIC, SKELLEY SEPTIC & WELL INSPECTIONS, "
                'CLN PORTABLE RESTROOM, and DANIEL ODY / MIKE NEWELL. '
                'ODH statewide bond status is not on this PDF (marked unknown). '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Summit County Public Health and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-summit-oh.json'
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        phone = r['phone'] or ''
        rows.append(
            '<tr>'
            f'<td>{e(r["name"])}</td>'
            f'<td>{e(r["operator"])}</td>'
            f'<td>{e(r["city"])}</td>'
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
  <title>Summit County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="__N__ Summit County, Ohio registered septage haulers from Summit County Public Health STS contractors PDF updated 2 September 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Summit County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Summit County Public Health’s printable PDF <cite>2026 STS Registered Contractors List</cite> (Updated: 9/2/26). Companies that haul septage in Summit County must register with SCPH. We tabulated only rows marked Septage Hauler = Y. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 17 September 2026 (US/Pacific). Official printable file: <a href="__SOURCE_URL__">scph.link/STS_Contractors</a>. Operation permits page: <a href="__PARENT_URL__">Registered Contractors</a>. STS contractor page: <a href="__PROGRAM_URL__">STS Contractor</a>. Verify statewide bonds via <a href="__ODH_URL__">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Summit County septage-hauler registration only. ODH bond status is <strong>unknown</strong> on this PDF.</p>
      <p>The full contractors PDF lists installers, service providers, and haulers. We list the <strong>__N__</strong> rows with Septage Hauler = Y (Updated: 9/2/26). Street addresses are not on this PDF — City only. Spellings kept as printed (including <code>POPS SEPTIC &amp;  DRAIN SERVICE</code> double space; <code>WERAB ENTERPRISES / FRED'S SEPTIC</code>; <code>SKELLEY SEPTIC &amp; WELL INSPECTIONS</code>; <code>CLN PORTABLE RESTROOM</code>).</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="cuyahoga.html">Cuyahoga County haulers</a> · <a href="portage.html">Portage County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>__N__ registered septage haulers from Summit County Public Health, PDF updated 2 September 2026</caption>
      <thead><tr><th>Business</th><th>Contact</th><th>City</th><th>Phone</th><th>ODH bond</th></tr></thead>
      <tbody>
__ROWS__
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-summit-oh.json">data/haulers-summit-oh.json</a>. Archived PDF: <a href="../__ARCHIVE__">__ARCHIVE__</a>. Names, contacts, cities, and phones are as printed on the county PDF (Septage Hauler = Y rows only).</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 17 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/summit.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

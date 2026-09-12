#!/usr/bin/env python3
"""Build Coshocton County OH registered haulers JSON + HTML from CPHD 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://www.coshoctoncounty.net/health/wp-content/uploads/sites/16/2026/05/Septic-Haulers-Installers-Service-Providers-2026.pdf'
PARENT_URL = 'https://www.coshoctoncounty.net/health/private-sewage/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-05-29'
RETRIEVED = '2026-09-11'
ARCHIVE = 'data/sources/coshocton-oh-2026-registered-contractors.pdf'
ARCHIVE_TXT = 'data/sources/coshocton-oh-2026-registered-contractors.txt'

# Hand-verified from pdftotext -layout of Septic-Haulers-Installers-Service-Providers-2026.pdf
# (PDF CreationDate 29 May 2026 UTC; linked from Coshocton Public Health District Private Sewage).
# Hauler role only — installers-only and service-providers-only omitted.
# Spellings kept as printed (Wondiland; Will M. & Patrick F.; INC capitalization).
RECORDS = [
    {'name': 'Affordable Portables', 'operator': 'Drew Krosesel', 'phone': '(740) 366-1811', 'address': '1000 Keller Dr., Heath, OH 43056', 'roles': 'Hauler'},
    {'name': 'B&C Septic Pumping, LLC', 'operator': 'Corey A. Jones', 'phone': '(740) 607-8807', 'address': '1640 Friendship Dr., New Concord, OH 43762', 'roles': 'Hauler'},
    {'name': 'Bobcat Multi-Works', 'operator': 'Steve Moody', 'phone': '(937) 585-9904', 'address': '2765 CR 21, Degraff, OH 43318', 'roles': 'Hauler'},
    {'name': 'Chandler Septic & Services, LLC', 'operator': 'Zack Chandler', 'phone': '(740) 577-9605', 'address': '2300 Aspen Rd., Frazeysburg, OH 43822', 'roles': 'Installer & Hauler'},
    {'name': 'CLP Services', 'operator': 'B. Xavier Burgstaller', 'phone': '(330) 716-3272', 'address': '125 Canal St. NE, Bolivar, OH 44612', 'roles': 'Hauler'},
    {'name': "Dick's Plumbing/Uhl's Septic Cleaning", 'operator': 'Richard Uhl', 'phone': '(330) 674-1424', 'address': '4437 TR 305, Millersburg, OH 44654', 'roles': 'Installer, Hauler & Service Provider'},
    {'name': 'Eagle Eye Septic Solutions', 'operator': 'Tom Bintz', 'phone': '(740) 454-7867', 'address': '8015 Wondiland Rd., Chandlersville, OH 43701', 'roles': 'Hauler'},
    {'name': 'Emerson Portables', 'operator': 'Lee Emerson', 'phone': '(740) 819-4254', 'address': '7215 Jones Rd., Nashport, OH 43830', 'roles': 'Hauler'},
    {'name': 'Forest Hill Septic Service', 'operator': 'Tyler Jamison', 'phone': '(740) 545-1212', 'address': '614 S. 14th St., Coshocton, OH 43812', 'roles': 'Hauler'},
    {'name': "Jim's Septic Service", 'operator': 'Jim Hagan', 'phone': '(740) 498-5246', 'address': '1245 Dunlap Creek Rd., Newcomerstown, OH 43832', 'roles': 'Hauler'},
    {'name': 'Miller Septic, LLC', 'operator': 'Seth Miller', 'phone': '(330) 893-2355', 'address': 'PO Box 328, Berlin, OH 44610', 'roles': 'Hauler & Service Provider'},
    {'name': 'Porta Kleen/Pro Kleen Industrial Svc.', 'operator': 'Jim Aldrich', 'phone': '(740) 689-1886', 'address': '1030 Mill Park Drive, Lancaster, OH 43130', 'roles': 'Hauler'},
    {'name': 'Site Work Services / Valley Septic', 'operator': 'James Dennison', 'phone': '(330) 897-3001', 'address': '9750 Ragersville Rd. SW, Baltic, OH 43804', 'roles': 'Installer, Hauler & Service Provider'},
    {'name': 'Stull Septic Pumping, LLC', 'operator': 'Nathan Stull', 'phone': '(740) 504-8741', 'address': '17783 Apple Valley Road, Howard, OH 43028', 'roles': 'Hauler'},
    {'name': 'Two-Tac LLC dba Ameri-Cans LLC', 'operator': 'Will M. & Patrick F.', 'phone': '(833) 363-7244', 'address': '13200 Marne Road NE, Newark, OH 43055', 'roles': 'Hauler'},
    {'name': 'William Albert, INC', 'operator': 'Joilynn Jones', 'phone': '(740) 622-3045', 'address': '1300 Cassingham Hollow, Coshocton, OH 43812', 'roles': 'Installer, Hauler & Service Provider'},
    {'name': 'Zemba Bros, INC', 'operator': 'Scott Zemba', 'phone': '(740) 452-1880', 'address': '3401 East Pike, Zanesville, OH 43701', 'roles': 'Installer & Hauler'},
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
    assert len(RECORDS) == 17, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert '2026 Registered Contractors' in txt
    assert 'Coshocton Public Health District' in txt
    for r in RECORDS:
        assert r['name'] in txt, r['name']
        op_frag = r['operator'].split('&')[0].strip()[:10]
        assert op_frag in txt, (r['operator'], op_frag)
        assert r['phone'] in txt, r['phone']
        street = r['address'].split(',')[0]
        assert street in txt, street
        assert 'Hauler' in r['roles']

    names = [r['name'] for r in RECORDS]
    assert len(names) == len(set(names)), 'duplicate names'

    records = []
    for r in RECORDS:
        records.append({
            'source_url': SOURCE_URL,
            'source_document_date': DOC_DATE,
            'retrieved': RETRIEVED,
            'name': r['name'],
            'role': 'Coshocton Public Health District registered hauler',
            'roles_printed': r['roles'],
            'operator': r['operator'],
            'address': r['address'],
            'phone': r['phone'],
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Coshocton County, Ohio',
        'source': {
            'publisher': 'Coshocton Public Health District',
            'title': '2026 Registered Contractors',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': 'PDF CreationDate 29 May 2026 UTC; live file Septic-Haulers-Installers-Service-Providers-2026.pdf under /2026/05/',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Coshocton Public Health District 2026 Registered Contractors PDF '
                '(CreationDate 29 May 2026). Full PDF lists installers, haulers, and service providers; '
                'this dataset includes only rows whose role column includes Hauler (17 firms). '
                'Installer-only and service-provider-only rows are omitted. Spellings kept as printed '
                '(Wondiland; Will M. & Patrick F.; INC capitalization). Emails not tabulated. '
                'ODH statewide bond status is not on this PDF (marked unknown). A hauler registration '
                'is not a service-provider inspection credential. Appearance is not an endorsement. '
                'Verify with Coshocton Public Health District and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-coshocton-oh.json'
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
            + f'<td>{e(r["roles_printed"])}</td>'
            + '<td class="unknown">unknown</td>'
            + '</tr>'
        )

    n = len(records)
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Coshocton County OH Septic Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Coshocton County, Ohio registered septic haulers from Coshocton Public Health District 2026 Registered Contractors PDF dated 29 May 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Coshocton County, Ohio — registered septic haulers</h1>
    <p class="lede">Transcribed from Coshocton Public Health District’s PDF <cite>2026 Registered Contractors</cite> (<code>Septic-Haulers-Installers-Service-Providers-2026.pdf</code>, PDF dated 29 May 2026). Companies that haul septage in Coshocton County must register with the health district. We listed only rows whose role includes Hauler. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 11 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">2026 Registered Installers, Haulers, and Service Providers</a>. Parent page: <a href="{e(PARENT_URL)}">Private Sewage</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Coshocton County hauler registration only. Installer-only and service-provider-only rows on the same PDF are omitted. ODH bond status is <strong>unknown</strong> on this PDF.</p>
      <p>The PDF role column includes Hauler for <strong>{n} firms</strong>. Spellings are as printed (including Wondiland Rd., Will M. &amp; Patrick F., and INC capitalization). Emails from the PDF are not shown here.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="columbiana.html">Columbiana County pumpers</a> · <a href="portage.html">Portage County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered haulers from Coshocton Public Health District, PDF dated 29 May 2026</caption>
      <thead><tr><th>Business</th><th>Operator</th><th>Address</th><th>Phone</th><th>Roles (as printed)</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-coshocton-oh.json">data/haulers-coshocton-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, operators, phones, addresses, and roles are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 11 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/coshocton.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

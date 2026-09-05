#!/usr/bin/env python3
"""Build Benton County MN Maintainer (Pumper) JSON + HTML from Benton County SSTS PDF."""
import html, json, re
from pathlib import Path
import pdfplumber

ROOT = Path(__file__).resolve().parent
PDF = ROOT / 'data/sources/benton-mn-licensed-ssts-2026-05-06.pdf'
SOURCE_URL = 'https://www.bentoncountymn.gov/DocumentCenter/View/238'
PARENT_URL = 'https://www.bentoncountymn.gov/228/Subsurface-Sewage-Treatment-Systems'
MPCA_URL = 'https://www.pca.state.mn.us/business-with-us/ssts-business-licensing'
DOC_DATE = '2026-05-06'
RETRIEVED = '2026-09-01'
ARCHIVE = 'data/sources/benton-mn-licensed-ssts-2026-05-06.pdf'

# Hand-verified from PDF Maintainer column (x≈718) across all 9 pages.
# Only firms with Maintainer (Pumper) marked. Do not invent fields.
RECORDS = [
    {
        'name': 'ABSOLUTE SEPTIC INC',
        'license_number': '2633',
        'license_as_printed': 'LICE#2633',
        'address': '12245 120TH St, Milaca MN 56353',
        'phone_as_printed': '320-983-5280',
        'maintainer_exp': '8/14/2027',
        'contact': 'Dennis Earl - C6637; Erika Earn - C1681',
    },
    {
        'name': 'ANDERSEN EXCAVATING',
        'license_number': '1879',
        'license_as_printed': 'LIC# 1879',
        'address': 'PO Box 771, Albany MN 56307',
        'phone_as_printed': '320/845-4576',
        'maintainer_exp': '9/15/27',
        'contact': 'Steven Andersen',
    },
    {
        'name': 'BUSSE SEPTIC SERVICE',
        'license_number': '1643',
        'license_as_printed': 'LIC# 1643',
        'address': '10600 - 26th St SE, St Cloud MN 56304',
        'phone_as_printed': '320/743-2483',
        'maintainer_exp': '3/23/27',
        'contact': 'Terrance Busse',
    },
    {
        'name': 'CLINK SEPTIC SOLUTIONS',
        'license_number': '4211',
        'license_as_printed': 'LIC# 4211',
        'address': '42915 CR 17, Sauk Centre MN 56378',
        'phone_as_printed': '320-249-7609',
        'maintainer_exp': '4/26/26',
        'contact': 'Benjamin D Clink, Patrick M Moritz',
    },
    {
        'name': 'FIEDLERS YOUR PUMPING SPECIALISTS',
        'license_number': '3318',
        'license_as_printed': 'LIC# 3318',
        'address': '18627 Nature Rd, Royalton MN 56373',
        'phone_as_printed': '320-252-9916',
        'maintainer_exp': '4/19/25',
        'contact': 'Cindy Tiemann',
    },
    {
        'name': 'IMHOLTE EXCAVATION & TRUCKING INC',
        'license_number': '4014',
        'license_as_printed': 'LIC# 4014',
        'address': '13484 77th St, Clear Lake MN 55319',
        'phone_as_printed': '320-291-6675',
        'maintainer_exp': '5/17/2027',
        'contact': 'Martin Imholte',
    },
    {
        'name': 'JOHNSON SEPTIC SERVICE',
        'license_number': '1023',
        'license_as_printed': 'LIC# 1023',
        'address': '8291 - 140th St, Milaca MN 56353',
        'phone_as_printed': '320-983-6622',
        'maintainer_exp': '6/01/26',
        'contact': 'Jeremiah Johnson',
    },
    {
        'name': 'NELSON SANITATION & RENTAL',
        'license_number': '4293',
        'license_as_printed': 'LIC# 4293',
        'address': 'PO Box 85, Rice MN 56367',
        'phone_as_printed': '320-393-2787',
        'maintainer_exp': '04/21/27',
        'contact': 'Derrick Nelson Tyler Nelson',
    },
    {
        'name': 'SEPTIC CHECK, INC',
        'license_number': '2624',
        'license_as_printed': 'LIC# 2624',
        'address': '6074 Keystone Road, Milaca MN 56353',
        'phone_as_printed': '320-983-2447',
        'maintainer_exp': '02/21/27',
        'contact': 'Brian Koski',
    },
    {
        'name': 'WRM SERVICES INC',
        'license_number': '1921',
        'license_as_printed': 'LIC# 1921',
        'address': '9075 155th St, Kimball MN 55353',
        'phone_as_printed': '320-398-2705',
        'maintainer_exp': '06/11/26',
        'contact': 'Bernard Miller',
    },
]


def fmt_phone(p):
    p = (p or '').strip()
    digits = re.sub(r'\D', '', p)
    if len(digits) == 10:
        return f'({digits[0:3]}) {digits[3:6]}-{digits[6:]}'
    if len(digits) == 11 and digits.startswith('1'):
        return f'({digits[1:4]}) {digits[4:7]}-{digits[7:]}'
    return p


def verify_maintainer_marks():
    found = []
    with pdfplumber.open(PDF) as pdf:
        assert len(pdf.pages) == 9, len(pdf.pages)
        for page in pdf.pages:
            words = page.extract_words()
            maint_x0 = None
            for w in words:
                if 'Maintainer' in w['text']:
                    maint_x0 = w['x0']
            if maint_x0 is None:
                continue
            for w in words:
                if w['text'] in ('x', 'x(X)', 'X') and w['x0'] >= maint_x0 - 15:
                    band = [ww for ww in words if abs(ww['top'] - w['top']) < 10 and ww['x0'] < 280]
                    name = ' '.join(ww['text'] for ww in sorted(band, key=lambda z: z['x0']))
                    found.append(name)
    return found


def e(s):
    return html.escape(str(s), quote=True)


def phone_cell(r):
    p = r['phone']
    digits = re.sub(r'\D', '', r.get('phone_as_printed') or '')
    if len(digits) == 10:
        return f'<td class="phones"><a href="tel:+1{digits}">{e(p)}</a></td>'
    if len(digits) == 11 and digits.startswith('1'):
        return f'<td class="phones"><a href="tel:+{digits}">{e(p)}</a></td>'
    return f'<td class="phones">{e(p)}</td>'


def main():
    marks = verify_maintainer_marks()
    print('Maintainer column marks:', len(marks))
    for m in marks:
        print(' ', m)
    assert len(marks) == 10, marks
    for r in RECORDS:
        assert any(r['name'].split(',')[0] in m or r['name'] in m for m in marks), r['name']

    records = []
    for r in RECORDS:
        phone = fmt_phone(r['phone_as_printed'])
        records.append({
            'license_number': r['license_number'],
            'license_as_printed': r['license_as_printed'],
            'source_url': SOURCE_URL,
            'source_document_date': DOC_DATE,
            'retrieved': RETRIEVED,
            'name': r['name'],
            'role': 'MPCA SSTS Maintainer (Pumper) — Benton County list',
            'address': r['address'],
            'phone': phone,
            'phone_as_printed': r['phone_as_printed'],
            'maintainer_exp': r['maintainer_exp'],
            'contact': r['contact'],
        })

    payload = {
        'jurisdiction': 'Benton County, Minnesota',
        'source': {
            'publisher': 'Benton County, Minnesota',
            'title': 'Licensed Designers, Inspectors, Installers, Maintainers & Service Providers',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'mpca_verify_url': MPCA_URL,
            'document_date': DOC_DATE,
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Benton County SSTS licensed-contractor PDF dated 5/6/2026. '
                'Only firms with Maintainer (Pumper) marked are listed. Designer, Inspector, Installer, '
                'and Service Provider columns were not treated as pumpers. Maintainer expiration dates are '
                'printed as on the PDF even if expired relative to the document date. Benton County does not '
                'endorse firms on the list. Appearance is not an endorsement. Verify licenses via MPCA SSTS search.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-benton-mn.json'
    out_json.write_text(json.dumps(payload, indent=2) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        rows.append(
            '<tr>'
            f'<td>{e(r["name"])}</td>'
            f'<td>{e(r["license_number"])}</td>'
            f'<td>{e(r["address"])}</td>'
            + phone_cell(r)
            + f'<td>{e(r["maintainer_exp"])}</td>'
            + '</tr>'
        )

    n = len(records)
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Benton County MN Septic Pumpers | Septic Pump Index</title>
  <meta name="description" content="{n} Benton County, Minnesota licensed SSTS Maintainers (Pumpers) from the county PDF dated 5/6/2026. Minnesota MPCA license. Pumping is not an inspection.">
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
    <h1 class="page">Benton County, Minnesota — licensed Maintainers (Pumpers)</h1>
    <p class="lede">Transcribed from Benton County’s PDF of licensed SSTS designers, inspectors, installers, maintainers, and service providers, dated 5/6/2026. We list only businesses marked <strong>Maintainer (Pumper)</strong>. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 1 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">DocumentCenter/View/238</a> (PDF dated 5/6/2026). Parent page: <a href="{e(PARENT_URL)}">Subsurface Sewage Treatment Systems</a>. Verify a license with the <a href="{e(MPCA_URL)}">Minnesota MPCA SSTS search</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Minnesota licenses Subsurface Sewage Treatment System (SSTS) businesses through the Minnesota Pollution Control Agency (MPCA). On this county list the columns are Designer (Advanced), Inspector (Advanced), Installer, Service Provider, and <strong>Maintainer (Pumper)</strong>. Only the Maintainer column means the firm is listed here as a pumper.</p>
      <p>Designer, Installer, Inspector, and Service Provider marks were <strong>not</strong> treated as pumping credentials. A pumping is not an inspection. Benton County states it does not specifically endorse or recommend firms on the list.</p>
      <p>Maintainer expiration dates are printed as on the PDF — including dates that appear expired relative to 5/6/2026. Confirm current status with the company and MPCA before you hire. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} licensed Maintainers (Pumpers) from Benton County MN, PDF dated 5/6/2026</caption>
      <thead><tr><th>Business</th><th>License #</th><th>Address</th><th>Phone</th><th>Maintainer exp</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-benton-mn.json">data/haulers-benton-mn.json</a>. Archived PDF: <a href="../data/sources/benton-mn-licensed-ssts-2026-05-06.pdf">data/sources/benton-mn-licensed-ssts-2026-05-06.pdf</a>. Names, phones, addresses, and license numbers are as printed on the county PDF (ABSOLUTE SEPTIC INC is labeled <code>LICE#2633</code> on that file).</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 1 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'mn/benton.html'
    out_html.write_text(page)
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

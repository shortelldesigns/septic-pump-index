#!/usr/bin/env python3
"""Build Marion County OH registered septage haulers JSON + HTML from MPH June 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://marionpublichealth.org/wp-content/uploads/2026/06/Marion-County-Registered-Septage-Haulers-2026.06.16.pdf'
PARENT_URL = 'https://marionpublichealth.org/household-sewage-treatment-systems/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-06-16'
RETRIEVED = '2026-09-13'
ARCHIVE = 'data/sources/marion-oh-2026-registered-haulers-06-16.pdf'
ARCHIVE_TXT = 'data/sources/marion-oh-2026-registered-haulers-06-16.txt'

# Hand-verified from pdftotext -layout of Marion-County-Registered-Septage-Haulers-2026.06.16.pdf
# (PDF CreationDate 16 June 2026 UTC; linked from Marion Public Health HSTS page as Registered Septage Haulers List).
# Spellings kept as printed (Underbross; Redbox + Dumpsters of Greater Columbus; Hanes Environmental Inc. as installer name).
RECORDS = [
    {'name': 'Able Sanitation Inc', 'operator': 'Amy Parrett', 'reg': '28', 'phone': '740-369-2542', 'address': '3360 Owen Fraley Rd, Delaware, OH 43015'},
    {'name': 'B & B Drain Service', 'operator': 'Steven R Brown Sr', 'reg': '42', 'phone': '419-524-1992', 'address': 'P O BOX 391, Mansfield, OH 44901'},
    {'name': "Bob's Septic Tank Service", 'operator': 'Guy Yinger', 'reg': '22', 'phone': '740-965-2122', 'address': 'PO BOX 359, Sunbury, OH 43074'},
    {'name': 'Buckeye Plumbing & Drains', 'operator': 'Kevin Edmonds', 'reg': '45', 'phone': '614-686-5001', 'address': '10385 Creamer Rd, Orient, OH 43146'},
    {'name': 'Emergency Plumbing Service', 'operator': 'Doug Rose', 'reg': '38', 'phone': '740-548-5453', 'address': '3354 US Hwy 23 N, Delaware, OH 43015'},
    {'name': 'Hanes Environmental Inc.', 'operator': 'Hanes Environmental Inc.', 'reg': '17', 'phone': '740-361-6080', 'address': 'PO Box 134, Caledonia, OH 43314'},
    {'name': 'Kincaid Wastewater Services, Inc.', 'operator': 'John S. Kincaid', 'reg': '3', 'phone': '740-386-3768', 'address': '2538 East River Road, Marion, OH 43302'},
    {'name': 'MJC Septic Services LLC', 'operator': 'Marcus Caplin', 'reg': '40', 'phone': '740-816-3945', 'address': '7696 Marysville Rd, Ostrander, OH 43061'},
    {'name': 'Shetler Services Inc.', 'operator': 'Greg Shetler', 'reg': '46', 'phone': '330-988-4373', 'address': '3656 E Messner Rd, Wooster, OH 44691'},
    {'name': 'SLM, LLC dba CLP Services', 'operator': 'Xavier Burgstaller', 'reg': '43', 'phone': '330-874-7131', 'address': '125 Canal St NE, PO Box 387, Bolivar, OH 44612'},
    {'name': 'Stiger Precast Inc.', 'operator': 'Mike Stiger', 'reg': '12', 'phone': '740-482-2313', 'address': '17793 St. Hwy. 231, Nevada, OH 44849'},
    {'name': 'The Waterworks, LLC', 'operator': 'Tim Cain', 'reg': '27', 'phone': '614-505-8211', 'address': '550 Schrock Rd, Columbus, OH 43229'},
    {'name': "Tidy Tim's, Inc.", 'operator': 'Tim Hack', 'reg': '14', 'phone': '419-947-3121', 'address': '6434 County Road 100, Mount Gilead, OH 43338'},
    {'name': 'Triple Crown Septic, LLC', 'operator': 'John Neidhart', 'reg': '29', 'phone': '740-225-2424', 'address': '2891 Firstenberger Rd, Marion, OH 43302'},
    {'name': 'Underbross Holdings, LLC', 'operator': 'Redbox + Dumpsters of Greater Columbus', 'reg': '39', 'phone': '419-855-5052', 'address': 'PO Box 555, Bellville, OH 44813'},
    {'name': 'United Rentals (North America), Inc dba Reliable Onsite Services', 'operator': 'DBA: Reliable Onsite Services', 'reg': '35', 'phone': '614-957-1616', 'address': '1760 Feddern Ave., Grove City, OH 43123'},
    {'name': 'Wells Septic and Drain', 'operator': 'Taylor Wells', 'reg': '25', 'phone': '740-524-3922', 'address': '1742 Hogback Road, Sunbury, OH 43074'},
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
    assert '2026 Marion County Registered Septage Haulers' in txt
    assert 'Updated: 6/16/2026' in txt
    assert 'Shetler Services Inc.' in txt
    for r in RECORDS:
        assert r['name'].split(' dba ')[0][:20] in txt or r['name'][:24] in txt, r['name']
        assert r['phone'] in txt, r['phone']
        assert r['reg'] in txt, r['reg']
        street = r['address'].split(',')[0]
        assert street in txt, street

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
            'name': r['name'],
            'role': 'Marion Public Health registered septage hauler',
            'operator': r['operator'],
            'registration_number': r['reg'],
            'address': r['address'],
            'phone': r['phone'] or None,
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Marion County, Ohio',
        'source': {
            'publisher': 'Marion Public Health',
            'title': '2026 Marion County Registered Septage Haulers (Marion-County-Registered-Septage-Haulers-2026.06.16.pdf)',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': 'PDF footer Updated: 6/16/2026; CreationDate 16 June 2026 UTC; linked from HSTS page as Registered Septage Haulers List',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Marion Public Health Registered Septage Haulers PDF '
                '(Marion-County-Registered-Septage-Haulers-2026.06.16.pdf; footer Updated: 6/16/2026; 17 named haulers). '
                'Spellings kept as printed including Underbross Holdings, LLC; installer name Hanes Environmental Inc.; '
                'and United Rentals (North America), Inc dba Reliable Onsite Services. '
                'Business phone used when printed (cell phones omitted from the table). Emails not tabulated. '
                'ODH statewide bond status is not on this PDF (marked unknown). '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Marion Public Health and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-marion-oh.json'
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        phone = r['phone'] or ''
        rows.append(
            '<tr>'
            f'<td>{e(r["name"])}</td>'
            f'<td>{e(r["operator"])}</td>'
            f'<td>{e(r["registration_number"])}</td>'
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
  <title>Marion County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Marion County, Ohio registered septage haulers from Marion Public Health PDF dated 16 June 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Marion County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Marion Public Health’s PDF <cite>2026 Marion County Registered Septage Haulers</cite> (<code>Marion-County-Registered-Septage-Haulers-2026.06.16.pdf</code>, updated 16 June 2026). Companies that haul septage in Marion County must register with the health district. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 13 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">Marion-County-Registered-Septage-Haulers-2026.06.16.pdf</a>. Parent page: <a href="{e(PARENT_URL)}">Household Sewage Treatment (HSTS)</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Marion County septage-hauler registration only. ODH bond status is <strong>unknown</strong> on this PDF.</p>
      <p>The PDF lists <strong>{n}</strong> named haulers (footer Updated: 6/16/2026). Spellings are as printed (including Underbross Holdings, LLC and Hanes Environmental Inc. as the installer name). Business phone is shown; cell phones and emails from the PDF are omitted.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="delaware.html">Delaware County haulers</a> · <a href="coshocton.html">Coshocton County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Marion Public Health, PDF updated 16 June 2026</caption>
      <thead><tr><th>Business</th><th>Operator / installer</th><th>Reg #</th><th>Address</th><th>Phone</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-marion-oh.json">data/haulers-marion-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, operators, registration numbers, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 13 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/marion.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

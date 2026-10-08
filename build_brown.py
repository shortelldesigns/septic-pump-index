#!/usr/bin/env python3
"""Build Brown County OH septage haulers JSON + HTML from BCHD 31 Jul 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://www.browncountyhealth.org/index.php/downloads/category/3-registered-contractors?download=378%3A2026-registered-septic-haulers-7-31-26'
PARENT_URL = 'https://www.browncountyhealth.org/index.php/downloads/category/3-registered-contractors'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-07-31'
RETRIEVED = '2026-10-07'
ARCHIVE = 'data/sources/brown-oh-2026-septage-haulers.pdf'
ARCHIVE_TXT = 'data/sources/brown-oh-2026-septage-haulers.txt'

# Hand-verified from pdftotext -layout of the Brown County Health Department
# "2026 Registered Septic Haulers 7-31-26" PDF (title Septage Haulers; HDIS; footer
# 07/31/2026; 17 TOTAL; 9116 HAMER ROAD, SUITE 101 GEORGETOWN OH). Linked from the
# Registered Contractors downloads page. Spellings kept as printed.
# Separate Service Providers / Installers lists on the same page are not used here.
RECORDS = [
    {'name': 'AAA SANITATION', 'operator': 'JERRY JONES', 'phone': '1-937-549-3417', 'address': '1240 ISLAND CREEK ROAD MANCHESTER, OH 45144'},
    {'name': 'AARON-ANDREWS SEPTIC SERVICE', 'operator': 'AARON PENNINGTON', 'phone': '1-513-625-0059', 'address': '5051 EAGLES VIEW CINCINNATI, OH 45244'},
    {'name': "BARBER'S SEPTIC SERVICE", 'operator': 'ROGER BARBER', 'phone': '1-937-444-4090', 'address': '119 SOUTH HIGH STREET MT ORAB, OH 45154'},
    {'name': 'CLEAN STREAM LLC', 'operator': 'DAMIEN PITTS', 'phone': '1-937-205-8431', 'address': '4985 DAWSON ROAD LYNCHBURG, OH 45142'},
    {'name': "DAY'S SANITATION SERVICE", 'operator': 'MICHAEL R. DAY', 'phone': '1-937-549-2683', 'address': 'P.O. BOX 193 MANCHESTER, OH 45144'},
    {'name': 'DOODY HAULS', 'operator': 'WILLIAM LAWRENCE', 'phone': '1-606-407-0855', 'address': '8123 AA HIGHWAY MAYSVILLE, KY 41056'},
    {'name': 'EAST FORK SANITATION LLC', 'operator': 'CHRISTOPHER BONINE', 'phone': '1-740-606-5184', 'address': '2873 EAST FORK ROAD RIPLEY, OH 45167'},
    {'name': 'G & C SEPTIC', 'operator': 'GEORGE TEEGARDEN', 'phone': '1-937-392-0084', 'address': '6265 OLD US 68 GEORGETOWN, OH 45121'},
    {'name': 'GULLETT SANITATION SERVICE INC.', 'operator': 'DAN GULLETT', 'phone': '1-513-734-2227', 'address': 'P.O. BOX 59 BETHEL, OH 45106'},
    {'name': 'MYERS LAND SERVICE LLC', 'operator': 'JORDAN MYERS', 'phone': '1-937-344-6727', 'address': '3359 PATTERSON ROAD BETHEL, OH 45106'},
    {'name': "NEAL'S SEPTIC SERVICE, LLC", 'operator': 'MIKE NEAL', 'phone': '1-513-625-9074', 'address': '6110 UNITED STATES ROUTE 133 GOSHEN, OH 45122'},
    {'name': 'PORTA KLEEN', 'operator': 'CHRIS WAITE', 'phone': '1-513-926-2625', 'address': '3206 PRODUCTION DR FAIRFIELD, OH 45014'},
    {'name': 'PROFLO SEPTIC SERVICES', 'operator': 'RYAN HESLER', 'phone': '1-937-217-3329', 'address': '1457 STATE ROUTE 348 WEST UNION, OH 45693'},
    {'name': 'RUMPKE TRANSPORTATION', 'operator': 'SHANE ELLIOTT/LAURA FURLONG', 'phone': '1-937-378-4126', 'address': '9427 BEYERS ROAD GEORGETOWN, OH 45121'},
    {'name': 'UNITED RENTALS INC. DBA RELIABLE ONSITE SVCS', 'operator': 'UNITED RENTALS (NORTH AMERICA)', 'phone': '1-513-288-2280', 'address': '4838 SPRING GROVE AVE CINCINNATI, OH 45232'},
    {'name': 'WILDCAT PORTA-POTTI, LLC', 'operator': 'TYLER MCCOLLISTER', 'phone': '1-937-218-4823', 'address': '112 BOURBON STREET BLANCHESTER, OH 45107'},
    {'name': 'XTREME CLEAN AND WATER RESTORATION LLC', 'operator': 'BRYAN CARRINGTON', 'phone': '1-513-739-9531', 'address': '7336 FREESOIL ROAD GEORGETOWN, OH 45121'},
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
    assert 'Brown County Health Department' in txt
    assert '07/31/2026' in txt
    assert '17 TOTAL' in txt
    assert '9116 HAMER ROAD' in txt
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
            'role': 'Brown County Health Department registered septage hauler',
            'operator': r['operator'] or None,
            'address': r['address'],
            'phone': r['phone'] or None,
            'local_reg': 'unknown',
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Brown County, Ohio',
        'source': {
            'publisher': 'Brown County Health Department',
            'title': 'Septage Haulers',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': (
                'PDF title prints Septage Haulers; HDIS footer 07/31/2026; 17 TOTAL; '
                'CreationDate 31 July 2026 UTC; linked from Registered Contractors downloads as 2026 Registered Septic Haulers 7-31-26. '
                'Business, operator, address, and phone printed; no local REG # on this PDF.'
            ),
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'archive_txt': ARCHIVE_TXT,
            'limitations': (
                'Transcribed from Brown County Health Department PDF '
                '2026 Registered Septic Haulers 7-31-26 (linked from '
                'https://www.browncountyhealth.org/index.php/downloads/category/3-registered-contractors). '
                '17 TOTAL named haulers (footer 07/31/2026). Spellings kept as printed including '
                "UNITED RENTALS INC. DBA RELIABLE ONSITE SVCS, operator line UNITED RENTALS (NORTH AMERICA), "
                'and the shared operator line SHANE ELLIOTT/LAURA FURLONG for RUMPKE TRANSPORTATION. One hauler (DOODY HAULS) prints a Maysville, KY address. '
                'No local registration numbers on this PDF (local REG marked unknown). '
                'ODH statewide bond status is not on this PDF (marked unknown). Separate 2026 Service Providers '
                'and 2026 registered septic installers lists on the same downloads page were not used for this hauler table. '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Brown County Health Department '
                'and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-brown-oh.json'
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
  <title>Brown County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Brown County, Ohio registered septage haulers from Brown County Health Department Septage Haulers PDF dated 31 July 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Brown County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Brown County Health Department’s PDF <cite>Septage Haulers</cite> (HDIS list, footer 31 July 2026, 17 TOTAL). Companies that haul septage in Brown County must register with the health department. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 7 October 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">2026 Registered Septic Haulers 7-31-26 PDF</a>. Parent page: <a href="{e(PARENT_URL)}">Registered Contractors downloads</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Brown County septage-hauler registration only. Local REG # and ODH bond status are <strong>unknown</strong> on this PDF (no registration numbers printed).</p>
      <p>The PDF prints <strong>{n} TOTAL</strong> (footer 07/31/2026). Spellings are as printed (including <code>UNITED RENTALS INC. DBA RELIABLE ONSITE SVCS</code> and the shared operator line <code>SHANE ELLIOTT/LAURA FURLONG</code>). One registered hauler, <code>DOODY HAULS</code>, prints a Maysville, Kentucky address. The same Registered Contractors downloads page also links 2026 Service Providers and 2026 registered septic installers lists — those lists are separate credentials and are not merged into this hauler table.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="adams.html">Adams County haulers</a> · <a href="clark.html">Clark County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Brown County Health Department, PDF dated 31 July 2026</caption>
      <thead><tr><th>Business</th><th>Operator</th><th>Address</th><th>Phone</th><th>Local REG #</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-brown-oh.json">data/haulers-brown-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, operators, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 7 October 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/brown.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

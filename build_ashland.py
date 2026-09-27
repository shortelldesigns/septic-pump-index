#!/usr/bin/env python3
"""Build Ashland County OH septage haulers JSON + HTML from ACHD 5 Aug 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://www.health-ashlandcounty-oh.gov/wp-content/uploads/2026/08/Haulers.pdf'
PARENT_URL = 'https://www.health-ashlandcounty-oh.gov/services/sewage-treatment-systems/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-08-05'
RETRIEVED = '2026-09-26'
ARCHIVE = 'data/sources/ashland-oh-2026-septage-haulers.pdf'
ARCHIVE_TXT = 'data/sources/ashland-oh-2026-septage-haulers.txt'

# Hand-verified from pdftotext -layout of Haulers.pdf
# (Ashland County Health Department; footer 08/05/2026; page 3 prints 25 TOTAL).
# Linked from Sewage Treatment Systems as 2026 Septage Haulers.
# Spellings kept as printed (BLAKE'S; BRENNER'S; BRENNY'S; BURNETT'S; DOUBLEFLUSH;
# JAKE'S; JOHN'S; KEITH'S; TIDY TIM'S; WEBB'S; SIDLE …,LLC DBA BUTLER SAN;
# UBER DROSS … DBA RED BOX; P.O.BOX 391; ST. RT. 39; MT. GILEAD).
RECORDS = [
    {'name': 'A & B SEPTIC CLEANING', 'operator': 'TODD YOUNG', 'phone': '1-419-368-5805', 'address': '1976 SR 89 JEROMESVILLE, OH 44840'},
    {'name': 'A-1 SEPTIC TANK CLEANING SERVICE', 'operator': 'MIKE MUTCHLER', 'phone': '1-419-368-3566', 'address': '1892 BELL ROAD WOOSTER, OH 44691'},
    {'name': 'ACTION DRAIN & SEPTIC', 'operator': 'PAMELA K. BLANTON', 'phone': '1-419-774-0323', 'address': 'PO BOX 904 MANSFIELD, OH 44901'},
    {'name': 'ASHLAND PRICE SEPTIC CLEANING', 'operator': 'JEREMY YOUNCE', 'phone': '1-419-606-2644', 'address': '734 TR 462 SULLIVAN, OH 44880'},
    {'name': 'B&B DRAIN & SEPTIC SERVICE', 'operator': 'STEVE R. BROWN SR.', 'phone': '1-419-524-1992', 'address': 'P.O.BOX 391 MANSFIELD, OH 44901'},
    {'name': "BLAKE'S SANITATION LTD", 'operator': 'RANDY BLAKE', 'phone': '1-419-929-0208', 'address': '220 SR 60 N NEW LONDON, OH 44851'},
    {'name': "BRENNER'S SANITARY SERVICE", 'operator': 'BRYAN MAST', 'phone': '1-330-464-7080', 'address': '5262 MESSNER RD APPLE CREEK, OH 44606'},
    {'name': "BRENNY'S SANITARY SERVICE LLC", 'operator': 'ALVIN BRENNEMAN', 'phone': '1-330-683-1611', 'address': '13627 BACK MASSILLON RD ORRVILLE, OH 44667'},
    {'name': "BURNETT'S SEPTIC SERVICES", 'operator': 'ANTHONY REVEGLIA', 'phone': '1-440-355-5526', 'address': '120 COMMERCE DR. LAGRANGE, OH 44050'},
    {'name': 'DOUBLEFLUSH SEPTIC SERVICES', 'operator': 'SCOTT SCHOLZ', 'phone': '1-330-391-5551', 'address': '2481 REMSEN RD MEDINA, OH 44256'},
    {'name': 'DYNAMERICAN', 'operator': 'KEVIN CHURCH', 'phone': '1-330-666-8863', 'address': '1011 LAKE RD MEDINA, OH 44256'},
    {'name': "JAKE'S JOHNS", 'operator': 'JAKE HOVERSTOCK', 'phone': '1-419-606-1357', 'address': '2227 SR 179 JEROMESVILLE, OH 44840'},
    {'name': "JOHN'S SEPTIC", 'operator': 'JOHN VERMILYA', 'phone': '1-419-606-8418', 'address': '2186 SR 179 JEROMESVILLE, OH 44840'},
    {'name': "KEITH'S DRAIN & SEPTIC SERVICE INC.", 'operator': 'KEITH SMITH', 'phone': '1-419-631-8870', 'address': '1755 SR 39 LUCAS, OH 44843'},
    {'name': 'LIBERTY FLUID MANAGEMENT LTD', 'operator': 'ROB CUTLIP', 'phone': '1-330-465-7467', 'address': '696 ST. RT. 39 PERRYSVILLE, OH 44864'},
    {'name': 'MILLER SEPTIC LLC', 'operator': 'SETH MILLER', 'phone': '1-330-893-2355', 'address': '2680 CR 168 DUNDEE, OH 44624'},
    {'name': 'MT SERVICES INC', 'operator': 'CLINTON MILLER', 'phone': '1-330-893-2355', 'address': '2680 CR 168 DUNDEE, OH 44624'},
    {'name': 'SHETLER SERVICES INC', 'operator': 'GREG SHETLER', 'phone': '1-330-988-4373', 'address': '3656 E. MESSNER RD WOOSTER, OH 44691'},
    {'name': 'SIDLE SANITATION SOLUTIONS,LLC DBA BUTLER SAN', 'operator': 'WAYNE SIDLE', 'phone': '1-419-585-0701', 'address': '3173 BROKAW RD BUTLER, OH 44822'},
    {'name': 'STULL SEPTIC PUMPING, LLC', 'operator': 'NATHAN STULL', 'phone': '1-740-504-8741', 'address': '17783 APPLE VALLEY ROAD HOWARD, OH 43028'},
    {'name': "TIDY TIM'S INC", 'operator': 'TIM HACK', 'phone': '1-419-947-3121', 'address': '6434 CR 100 MT. GILEAD, OH 43338'},
    {'name': 'UBER DROSS HOLDINGS LLC DBA RED BOX', 'operator': 'SCOTT SELLERS', 'phone': '1-419-855-5052', 'address': 'PO BOX 555 BELLVILLE, OH 44813'},
    {'name': 'UHL SEPTIC CLEANING', 'operator': 'RICHARD B UHL', 'phone': '1-330-674-1424', 'address': '4437 TWP RD 305 MILLERSBURG, OH 44654'},
    {'name': 'UNITED RENTALS (NORTH AMERICA)', 'operator': 'JEFF WALKER', 'phone': '1-330-744-2507', 'address': '1050 KILLIAN RD AKRON, OH 44312'},
    {'name': "WEBB'S SEPTIC TANK CLEANING & MAINTENANCE", 'operator': 'STEVE PASHEILICH', 'phone': '1-419-522-3539', 'address': '1460 CHEW RD MANSFIELD, OH 44903'},
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
    assert len(RECORDS) == 25, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert 'Septage Haulers' in txt
    assert 'ASHLAND COUNTY' in txt
    assert '08/05/2026' in txt
    assert '25 TOTAL' in txt
    assert 'A & B SEPTIC CLEANING' in txt
    assert "BLAKE'S SANITATION LTD" in txt
    assert 'DOUBLEFLUSH SEPTIC SERVICES' in txt
    assert 'DYNAMERICAN' in txt
    assert "JAKE'S JOHNS" in txt
    assert 'SIDLE SANITATION SOLUTIONS,LLC DBA BUTLER SAN' in txt
    assert 'UBER DROSS HOLDINGS LLC DBA RED BOX' in txt
    assert "WEBB'S SEPTIC TANK CLEANING & MAINTENANCE" in txt
    assert "BRENNER'S SANITARY SERVICE" in txt
    assert "BRENNY'S SANITARY SERVICE LLC" in txt
    for r in RECORDS:
        assert r['name'][:28] in txt, r['name']
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
            'role': 'Ashland County Health Department registered septage hauler',
            'operator': r['operator'] or None,
            'address': r['address'],
            'phone': r['phone'] or None,
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Ashland County, Ohio',
        'source': {
            'publisher': 'Ashland County Health Department',
            'title': 'Septage Haulers (Haulers.pdf)',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': 'PDF footer 08/05/2026 on each page; page 3 prints 25 TOTAL; linked from Sewage Treatment Systems as 2026 Septage Haulers',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Ashland County Health Department Septage Haulers PDF '
                '(Haulers.pdf; footer 08/05/2026; 25 TOTAL). '
                'Spellings kept as printed including BLAKE\'S, BRENNER\'S, BRENNY\'S, BURNETT\'S, '
                'DOUBLEFLUSH SEPTIC SERVICES (one word), JAKE\'S JOHNS, JOHN\'S SEPTIC, KEITH\'S, '
                'TIDY TIM\'S INC, WEBB\'S, SIDLE SANITATION SOLUTIONS,LLC DBA BUTLER SAN '
                '(comma before LLC; DBA truncated as printed), and UBER DROSS HOLDINGS LLC DBA RED BOX. '
                'B&B address prints P.O.BOX 391 (no space after P.O.). '
                'LIBERTY street prints ST. RT. 39; TIDY TIM\'S city prints MT. GILEAD. '
                'No registration numbers on this PDF. ODH statewide bond status is not on this PDF (marked unknown). '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Ashland County Health Department and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-ashland-oh.json'
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
  <title>Ashland County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Ashland County, Ohio registered septage haulers from Ashland County Health Department Septage Haulers PDF dated 5 August 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Ashland County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Ashland County Health Department’s PDF <cite>Septage Haulers</cite> (<code>Haulers.pdf</code>, footer 5 August 2026). Companies that haul septage in Ashland County must register with the health department. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 26 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">Haulers.pdf</a>. Parent page: <a href="{e(PARENT_URL)}">Sewage Treatment Systems</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Ashland County septage-hauler registration only. ODH bond status is <strong>unknown</strong> on this PDF.</p>
      <p>The PDF prints <strong>{n} TOTAL</strong> (footer 08/05/2026 on each page). Spellings are as printed (including <code>BLAKE'S</code>, <code>BRENNER'S</code>, <code>BRENNY'S</code>, <code>BURNETT'S</code>, <code>DOUBLEFLUSH SEPTIC SERVICES</code>, <code>JAKE'S JOHNS</code>, <code>SIDLE SANITATION SOLUTIONS,LLC DBA BUTLER SAN</code>, <code>UBER DROSS HOLDINGS LLC DBA RED BOX</code>). <code>B&amp;B</code> address prints <code>P.O.BOX 391</code> (no space after <code>P.O.</code>). No registration numbers appear on this PDF.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="erie.html">Erie County haulers</a> · <a href="darke.html">Darke County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Ashland County Health Department, PDF dated 5 August 2026</caption>
      <thead><tr><th>Business</th><th>Operator</th><th>Address</th><th>Phone</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-ashland-oh.json">data/haulers-ashland-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, operators, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 26 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/ashland.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

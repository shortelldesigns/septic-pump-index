#!/usr/bin/env python3
"""Build Delaware County OH registered septage haulers JSON + HTML from DPHD July 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://www.delawarehealth.org/wp-content/uploads/2026/07/HAULERS-JULY-2026.pdf'
PARENT_URL = 'https://www.delawarehealth.org/sewage/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-07-21'
RETRIEVED = '2026-09-12'
ARCHIVE = 'data/sources/delaware-oh-2026-septage-haulers-07-21.pdf'
ARCHIVE_TXT = 'data/sources/delaware-oh-2026-septage-haulers-07-21.txt'

# Hand-verified from pdftotext -layout of HAULERS-JULY-2026.pdf
# (PDF CreationDate 21 July 2026 UTC; linked from Delaware Public Health District sewage page as SEPTIC HAULERS).
# Spellings kept as printed (CHUCKS…IN truncation; MASRYSVILLE; REDBOX & truncation; JEREMY HEAVEN).
RECORDS = [
    {'name': 'A & B SANITATION, INC', 'operator': 'JEREMY HUBBARD', 'phone': '1-614-471-8060', 'address': 'PO BOX 358, SUNBURY, OH 43074'},
    {'name': 'ABLE SANITATION INC', 'operator': 'AMY PARRETT', 'phone': '1-740-369-2542', 'address': '3360 OWEN FRALEY RD, DELAWARE, OH 43015'},
    {'name': 'ACE SEPTIC TANK CLEANING INC', 'operator': 'ALICE AND COLT BAUMAN', 'phone': '1-614-491-2121', 'address': '4210 GROVEPORT RD, OBETZ, OH 43207'},
    {'name': 'AUSTINS SEPTIC LLC', 'operator': 'AUSTIN THORPE', 'phone': '1-740-263-6925', 'address': '81 E COLLEGE AVE, JOHNSTOWN, OH 43031'},
    {'name': 'BANK SANITATION LLC DBA STULL SEPTIC PUMPING', 'operator': 'NATHAN STULL', 'phone': '1-740-504-8741', 'address': '17783 APPLE VALLEY RD, HOWARD, OH 43028'},
    {'name': 'BLOODHOUND SANITATION SERVICES LLC', 'operator': 'KEVIN ADKINS', 'phone': '', 'address': '12540 ROBINS RD, WESTERVILLE, OH 43082'},
    {'name': "BOB'S SEPTIC TANK SERVICE", 'operator': 'GUY YINGER', 'phone': '1-740-965-2122', 'address': 'PO BOX 359, SUNBURY, OH 43074'},
    {'name': 'BOBCAT SANITATION MULTI-WORKS', 'operator': 'STEVE MOODY', 'phone': '1-937-585-9904', 'address': '2765 COUNTY ROAD 21, DE GRAFF, OH 43318'},
    {'name': 'BUCKEYE PLUMBING AND DRAINS', 'operator': 'KEVIN EDMONDS', 'phone': '1-614-686-5001', 'address': 'PO BOX 75, ORIENT, OH 43146'},
    {'name': 'CHUCKS SEPTIC TANK SEWER & DRAIN CLEANING IN', 'operator': 'STEVE BESSE', 'phone': '1-614-875-9508', 'address': '2136 HARDY PKWY, GROVE CITY, OH 43123'},
    {'name': 'CLARRIDGES DISCOUNT SEPTIC, LLC', 'operator': 'SUZANNE/TY CLARRIDGE', 'phone': '1-937-644-3191', 'address': '20444 RAYMOND RD, MARYSVILLE, OH 43040'},
    {'name': 'CPR DRAIN CLEANING INC.', 'operator': 'DAVID TURBERVILLE', 'phone': '1-614-279-3445', 'address': '2168 EAKIN RD, COLUMBUS, OH 43223'},
    {'name': 'DARBY CREEK SEPTIC LLC', 'operator': 'BRANDON YODER & DENISE YODER', 'phone': '1-740-206-4856', 'address': '5885 LAFAYETTE PLAIN CITY RD, LONDON, OH 43140'},
    {'name': 'E C BABBERT INC', 'operator': 'JOHN LENDRUM', 'phone': '1-614-837-8444', 'address': 'PO BOX 203, CANAL WINCHESTER, OH 43110'},
    {'name': 'EMERGENCY PLUMBING COMPANY LLC', 'operator': 'NICK ROSE/COLTON RETTERER', 'phone': '1-740-548-5453', 'address': 'PO BOX 91, DELAWARE, OH 43015'},
    {'name': 'ERICSON ENVIRONMENTAL SERVICES', 'operator': 'ERIC BAUMAN', 'phone': '1-614-874-7585', 'address': 'PO BOX 266, GALLOWAY, OH 43119'},
    {'name': 'GOT 2 GO PORTABLE SANITATION', 'operator': 'LARRON PERRY', 'phone': '1-614-701-7287', 'address': '1846 FEDERAL PARKWAY, COLUMBUS, OH 43207'},
    {'name': "JACK'S SEPTIC TANK CLEANING & CONST. INC.", 'operator': 'MANNY DIAZ', 'phone': '1-740-366-3255', 'address': '274 S 6TH ST, NEWARK, OH 43055'},
    {'name': 'JUDGES SANITATION & EXCAVATION LLC', 'operator': 'HERMAN E BERK JR', 'phone': '1-614-855-3361', 'address': '10745 FANCHER RD, WESTERVILLE, OH 43082'},
    {'name': 'KINCAID WASTEWATER SERVICES INC', 'operator': 'JOHN S KINCAID', 'phone': '1-740-386-3768', 'address': '2538 EAST RIVER RD, MARION, OH 43302'},
    {'name': 'M. T. SERVICE INC DBA MILLER PORTABLES', 'operator': 'ANDREW MILLER', 'phone': '1-800-827-6808', 'address': 'PO BOX 136, BERLIN, OH 44610'},
    {'name': 'MJC SEPTIC SERVICES', 'operator': 'MARCUS CAPLIN', 'phone': '1-740-833-5166', 'address': '7696 MASRYSVILLE RD, OSTRANDER, OH 43061'},
    {'name': 'OHIO CAST STONE CO. LLC', 'operator': 'ALAN CLEARY', 'phone': '1-614-444-2278', 'address': '8548 DUVALL RD, ASHVILLE, OH 43103'},
    {'name': 'PORTA KLEEN', 'operator': 'AMANDA NEIGHBERGALL', 'phone': '1-740-689-1886', 'address': '1030 MILL PARK DR, LANCASTER, OH 43130'},
    {'name': 'RENT A JOHN PORTABLE SANITATION', 'operator': 'ANTHONY CAIN', 'phone': '1-614-497-1776', 'address': '4522 LOCKBOURNE RD, COLUMBUS, OH 43207'},
    {'name': 'STIGER PRECAST INC', 'operator': 'MIKE STIGER/CATHY SCHEFFLER', 'phone': '1-740-482-2313', 'address': '17793 STATE HWY 231, NEVADA, OH 44849'},
    {'name': 'T & J EXCAVATING', 'operator': 'THOMAS HEAVENER/ JEREMY HEAVEN', 'phone': '1-740-605-0859', 'address': '2380 JAMESTOWN RD, CROOKSVILLE, OH 43731'},
    {'name': 'THE DRAIN GUYS LLC', 'operator': 'JEREMY STUMP', 'phone': '1-614-946-0225', 'address': '6520 OLEY SPEAKS WAY, CANAL WINCHESTER, OH 43110'},
    {'name': 'THE WATERWORKS, LLC', 'operator': 'BRAD SHEPHERD', 'phone': '1-614-876-0999', 'address': '550 SCHROCK RD, COLUMBUS, OH 43229'},
    {'name': "TIDY TIM'S INC", 'operator': 'TIM HACK', 'phone': '1-419-947-3121', 'address': '6434 CO RD 100, MOUNT GILEAD, OH 43338'},
    {'name': 'UBERDROSS HOLDINGS LLC DBA REDBOX &', 'operator': 'SCOTT SELLERS', 'phone': '1-419-855-5053', 'address': 'PO BOX 555, BELLVILLE, OH 44813'},
    {'name': 'UNITED RENTALS DBA RELIABLE ONSITE SERVICES', 'operator': 'JEFF WALKER', 'phone': '1-614-957-1616', 'address': '791 EAST 64TH AVE, DENVER, CO 80229'},
    {'name': "WARNER'S LIQUID WASTE HAULING", 'operator': 'CHRISTOPHER L. WARNER', 'phone': '1-614-873-8648', 'address': '8180 RICKARD RD, PLAIN CITY, OH 43064'},
    {'name': 'WAS PORTABLES DBA AFFORDABLE PORTABLES', 'operator': 'DREW KNOESEL', 'phone': '1-740-366-1811', 'address': '1000 KELLER DR, HEATH, OH 43056'},
    {'name': 'WELLS SEPTIC AND DRAIN LLC', 'operator': 'TAYLOR WELLS', 'phone': '1-740-524-3922', 'address': '1742 HOGBACK RD, SUNBURY, OH 43074'},
    {'name': 'YODERS SEPTIC SERVICE', 'operator': 'CARL YODER', 'phone': '1-740-857-1822', 'address': '5890 LAFAYETTE PLAIN CITY RD, LONDON, OH 43140'},
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
    assert len(RECORDS) == 36, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert 'Septage Haulers' in txt
    assert 'Delaware Public Health District' in txt
    assert '36 TOTAL' in txt
    assert '07/21/2026' in txt
    for r in RECORDS:
        assert r['name'] in txt, r['name']
        op_frag = r['operator'].split('/')[0].split('&')[0].strip()[:10]
        assert op_frag in txt, (r['operator'], op_frag)
        if r['phone']:
            assert r['phone'] in txt, r['phone']
        street = r['address'].split(',')[0]
        assert street in txt, street

    names = [r['name'] for r in RECORDS]
    assert len(names) == len(set(names)), 'duplicate names'

    records = []
    for r in RECORDS:
        records.append({
            'source_url': SOURCE_URL,
            'source_document_date': DOC_DATE,
            'retrieved': RETRIEVED,
            'name': r['name'],
            'role': 'Delaware Public Health District registered septage hauler',
            'operator': r['operator'],
            'address': r['address'],
            'phone': r['phone'] or None,
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Delaware County, Ohio',
        'source': {
            'publisher': 'Delaware Public Health District',
            'title': 'Septage Haulers (HAULERS-JULY-2026.pdf)',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': 'PDF footer 07/21/2026; CreationDate 21 July 2026 UTC; linked from sewage page as SEPTIC HAULERS',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Delaware Public Health District Septage Haulers PDF '
                '(HAULERS-JULY-2026.pdf; footer 07/21/2026; PDF prints 36 TOTAL). '
                'Spellings kept as printed including truncated business names '
                '(CHUCKS SEPTIC TANK SEWER & DRAIN CLEANING IN; UBERDROSS HOLDINGS LLC DBA REDBOX &), '
                'MASRYSVILLE RD, and JEREMY HEAVEN. BLOODHOUND phone printed as dashes (unknown). '
                'ODH statewide bond status is not on this PDF (marked unknown). '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Delaware Public Health District and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-delaware-oh.json'
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        phone = r['phone'] or ''
        rows.append(
            '<tr>'
            f'<td>{e(r["name"])}</td>'
            f'<td>{e(r["operator"])}</td>'
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
  <title>Delaware County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Delaware County, Ohio registered septage haulers from Delaware Public Health District HAULERS-JULY-2026.pdf dated 21 July 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Delaware County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Delaware Public Health District’s PDF <cite>Septage Haulers</cite> (<code>HAULERS-JULY-2026.pdf</code>, footer dated 21 July 2026). Companies that haul septage in Delaware County must register with the health district. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 12 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">HAULERS-JULY-2026.pdf</a>. Parent page: <a href="{e(PARENT_URL)}">Sewage</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Delaware County septage-hauler registration only. ODH bond status is <strong>unknown</strong> on this PDF.</p>
      <p>The PDF prints <strong>{n} TOTAL</strong>. Spellings are as printed (including truncated names CHUCKS…IN and UBERDROSS…REDBOX &amp;, MASRYSVILLE Rd., and JEREMY HEAVEN). BLOODHOUND’s phone was printed as dashes and is marked unknown here.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="coshocton.html">Coshocton County haulers</a> · <a href="portage.html">Portage County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Delaware Public Health District, PDF dated 21 July 2026</caption>
      <thead><tr><th>Business</th><th>Operator</th><th>Address</th><th>Phone</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-delaware-oh.json">data/haulers-delaware-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, operators, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 12 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/delaware.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

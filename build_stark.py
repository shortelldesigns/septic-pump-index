#!/usr/bin/env python3
"""Build Stark County OH septage haulers JSON + HTML from SCHD 5 Mar 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://www.starkcountyohio.gov/Stark%20County%20Health%20Department/Our%20Programs/Online%20Forms/Sewage/Installers,%20Service%20Providers%20and%20Haulers/2026%20HAULER%20LIST.pdf'
PARENT_URL = 'https://www.starkhealth.org/government/offices/public_health/environmental_health/sewage.php'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-03-05'
RETRIEVED = '2026-10-14'
ARCHIVE = 'data/sources/stark-oh-2026-hauler-list.pdf'
ARCHIVE_TXT = 'data/sources/stark-oh-2026-hauler-list.txt'

# Hand-verified from pdftotext -layout of Stark County Health Department
# "2026 HAULER LIST.pdf" (title Septage Haulers; HDIS; footer 03/05/2026;
# 36 TOTAL; 7235 WHIPPLE AVE NW NORTH CANTON OH). Spellings kept as printed.
# Separate installer / service-provider PDFs in the same folder are not used.
RECORDS = [
    {'name': 'A ROOTER MAN', 'operator': 'JAMES ENGLISH', 'phone': '1-877-232-1520', 'address': '195 POTOMAC AVE UNIT B TALLMADGE, OH 44278'},
    {'name': 'ALL TOWN & COUNTRY', 'operator': 'GEORGE T BLANKENSHIP', 'phone': '1-330-745-2277', 'address': '3500 S HAMETOWN RD NORTON, OH 44203'},
    {'name': 'ALLEN DRAIN SERVICE, INC.', 'operator': 'BERNIE NOBLE', 'phone': '-330-673-6482', 'address': '1008 MOGADORE RD KENT, OH 44240'},
    {'name': 'ATOMIC SEWER LLC', 'operator': 'GUY C WEISEL', 'phone': '1-330-492-1000', 'address': 'PO BOX 196 MIDDLEBRANCH, OH 44652'},
    {'name': 'BOSLEY DRAIN AND SEPTIC', 'operator': 'JOSHUA-PAUL TULLY', 'phone': '-330-454-4000', 'address': 'PO BOX 303 LOUISVILLE, OH 44641'},
    {'name': "BRENNY'S SANITARY SERVICE LLC", 'operator': 'ALVIN BRENNEMAN', 'phone': '1-330-683-1611', 'address': '13627 BACK MASSILLON RD ORRVILLE, OH 44667'},
    {'name': 'CHARLIE HOFFMAN SEPTIC SERVICES', 'operator': 'MARK BISKUP', 'phone': '-330-584-5466', 'address': '16124 W WESTERN RESERVE RD BERLIN CENTER, OH 44401'},
    {'name': 'CHESTER H3 LLC, DBA ERWIN SEPTIC SERVICE', 'operator': 'JOSEPH HERETTA', 'phone': '1-330-627-4700', 'address': '333 STEUBENVILLE RD SE CARROLLTON, OH 44615'},
    {'name': 'DOUBLE FLUSH SEPTIC SERVICES', 'operator': 'SCOTT SCHOLZ', 'phone': '1-330-391-5551', 'address': '2481 REMSEN RD MEDINA, OH 44256'},
    {'name': 'DYNAMERICAN', 'operator': 'WOOD INVESTMENT PROPERTY LLC', 'phone': '1-330-666-8863', 'address': '1011 LAKE RD MEDINA, OH 44256'},
    {'name': 'ESZBIBB DBA COWBOY MILLER SEPTIC PUMPING INC', 'operator': 'SHERI BROWN', 'phone': '1-330-821-8060', 'address': '2012 NOTMAN RD DEERFIELD, OH 44411'},
    {'name': 'GOLD-N-DEUCE LLC', 'operator': 'BRIAN MYERS', 'phone': '', 'address': '187 W MOHAWK DR MALVERN, OH 44644'},
    {'name': 'HUMBERT SANITARY SERVICE', 'operator': 'MIKE HUMBERT', 'phone': '1-330-494-3000', 'address': '1581 APPLEGROVE NW NORTH CANTON, OH 44720'},
    {'name': "JJC2, LTD DBA TOM'S SEPTIC AND SEPTIC", 'operator': 'JEFF CHAHNE', 'phone': '-330-545-8584', 'address': '1057 TRUMBULL AVE (UNIT L) GIRARD, OH 44420'},
    {'name': "KING'S SANITARY SERVICES, LLC", 'operator': 'REX KING JR', 'phone': '1-330-372-3201', 'address': 'PO BOX 240 BRISTOLVILLE, OH 44402'},
    {'name': "KLINE'S ENVIRONMENTAL SERVICE, LLC", 'operator': 'NELSON KLINE', 'phone': '1-330-231-7358', 'address': 'PO BOX 23 WINESBURG, OH 44690'},
    {'name': "LARRY'S SEPTIC SERVICE", 'operator': 'LARRY SHAW', 'phone': '1-330-699-2120', 'address': '10681 MARKET AVE NORTH HARTVILLE, OH 44632'},
    {'name': 'MILLER SEPTIC, LLC', 'operator': 'SETH MILLER', 'phone': '1-330-893-2355', 'address': 'PO BOX 328 BERLIN, OH 44610'},
    {'name': 'MILNER SEPTIC SERVICE', 'operator': 'WILLIAM MILNER', 'phone': '1-330-868-9700', 'address': 'P.O. BOX 2 MINERVA, OH 44657'},
    {'name': 'PATTERSON SPECIALTY SERVICES', 'operator': 'BILL PATTERSON', 'phone': '1-330-862-3371', 'address': '300 W LISBON ST WAYNESBURG, OH 44688'},
    {'name': "POP'S SEPTIC & DRAIN SERVICE INC", 'operator': 'BRAD WAYBRIGHT', 'phone': '1-330-854-6405', 'address': '6235 AKRON AVE CANAL FULTON, OH 44614'},
    {'name': 'SALEM SEPTIC', 'operator': 'JOHN MERCER', 'phone': '1-330-525-7800', 'address': '30761 GEORGETOWN RD SALEM, OH 44460'},
    {'name': 'SEPTICLEAN', 'operator': 'MATT WOODFORD', 'phone': '1-330-428-1918', 'address': '9655 BERLIN HTS DR DEERFIELD, OH 44411'},
    {'name': 'SHETLER SERVICES', 'operator': 'SHETLER SERVICES', 'phone': '1-330-988-4373', 'address': '3656 E MESSNER RD WOOSTER, OH 44691'},
    {'name': 'SKELLEY SEPTIC SERVICES LLC', 'operator': 'BEN SKELLEY', 'phone': '1-330-267-8485', 'address': '869 OLDE ORCHARD RD BOLIVAR, OH 44612'},
    {'name': 'SOSNICK SEPTIC SERVICE', 'operator': 'MICHAEL SOSNICK', 'phone': '1-330-584-6718', 'address': '19542 MIDDLETOWN RD BELOIT, OH 44609'},
    {'name': 'SPEEDIE SEPTIC & SEWER', 'operator': '', 'phone': '1-330-878-5423', 'address': '300 - 6TH ST SW STRASBURG, OH 44680'},
    {'name': "STEVE'S SERVICE", 'operator': 'STEPHEN UTT', 'phone': '1-330-206-5349', 'address': '298 EAST FLORIDA AVE SEBRING, OH 44672'},
    {'name': 'SUMMIT EXCAVATING INC', 'operator': 'MARIE EASTERLING', 'phone': '1-330-825-2035', 'address': '3316 GRILL RD CLINTON, OH 44216'},
    {'name': 'T.E. GRIFFITH SEPTIC', 'operator': 'TERRY GRIFFITH', 'phone': '1-330-484-5554', 'address': '4060 DUEBER SW CANTON, OH 44706'},
    {'name': 'TISSOT SANITARY SERVICES LLC', 'operator': 'SCOTT & SCOTTIE TISSOT', 'phone': '1-330-268-7928', 'address': '3491 CLERMONT AVE NW NORTH LAWRENCE, OH 44666'},
    {'name': 'UNITED RENTALS DBA RELIABLE ONSITE SERVICES', 'operator': 'LYNN VIZDOS', 'phone': '1-330-733-9000', 'address': '1050 KILLIAN RD AKRON, OH 44312'},
    {'name': 'WALT KUCHARSKI SEPTIC SERVICE, INC.', 'operator': 'WALTER CLAY KUCHARSKI', 'phone': '-440-232-0767', 'address': '2841 STUBBINS RD RICHFIELD, OH 44141'},
    {'name': 'WERAB ENTERPRISES LLC D|B|A FREDS SEPTIC SERV', 'operator': 'CHAD WERAB', 'phone': '1-330-947-9902', 'address': '1521 BANK ST ATWATER, OH 44201'},
    {'name': 'WHIPKEY SEPTIC PUMPING LLC', 'operator': 'CLAYTON WHIPKEY', 'phone': '-330-736-1821', 'address': '4300 MIDDLE ST HOMEWORTH, OH 44634'},
    {'name': 'XPERT SEPTIC SERVICE', 'operator': 'THOMAS FARRIS', 'phone': '1-330-456-3939', 'address': 'PO BOX 7535 CANTON, OH 44705'},
]


def e(s):
    return html.escape(str(s), quote=True)


def phone_cell(printed):
    raw = (printed or '').strip()
    if not raw or raw == '- - -':
        return '<td class="phones unknown">unknown</td>'
    digits = re.sub(r'\D', '', raw)
    if not digits:
        return '<td class="phones unknown">unknown</td>'
    # Leading dash phones like -330-673-6482 still have 10 digits after strip
    if len(digits) == 10:
        href = f'+1{digits}'
    elif len(digits) == 11 and digits.startswith('1'):
        href = f'+{digits}'
    else:
        href = f'+1{digits}'
    return f'<td class="phones"><a href="tel:{href}">{e(raw)}</a></td>'


def main():
    assert len(RECORDS) == 36, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert 'Septage Haulers' in txt
    assert 'STARK COUNTY HEALTH DEPARTMENT' in txt
    assert '03/05/2026' in txt
    assert '36 TOTAL' in txt
    assert '7235 WHIPPLE AVE NW' in txt
    for r in RECORDS:
        assert r['name'] in txt, r['name']
        street = r['address'].split()[0]
        assert street in txt, r['address']
        if r['phone']:
            assert r['phone'] in txt, r['phone']
        else:
            assert '- - -' in txt
        if r['operator']:
            token = r['operator'].split()[0].replace(',', '').replace('&', '')
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
            'role': 'Stark County Health Department registered septage hauler',
            'operator': r['operator'] or None,
            'address': r['address'],
            'phone': r['phone'] or None,
            'local_reg': 'unknown',
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Stark County, Ohio',
        'source': {
            'publisher': 'Stark County Health Department',
            'title': 'Septage Haulers',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': (
                'PDF title prints Septage Haulers; HDIS footer 03/05/2026 on each page; 36 TOTAL; '
                'CreationDate 5 March 2026 PST; file name 2026 HAULER LIST.pdf under Online Forms / Sewage / '
                'Installers, Service Providers and Haulers. Business, operator, address, and phone printed; '
                'no local REG # on this PDF. GOLD-N-DEUCE LLC phone prints as - - -.'
            ),
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'archive_txt': ARCHIVE_TXT,
            'limitations': (
                'Transcribed from Stark County Health Department PDF 2026 HAULER LIST.pdf '
                f'({SOURCE_URL}). '
                '36 TOTAL named haulers (footer 03/05/2026). Spellings kept as printed including '
                "JJC2, LTD DBA TOM'S SEPTIC AND SEPTIC, WERAB ENTERPRISES LLC D|B|A FREDS SEPTIC SERV, "
                'ESZBIBB DBA COWBOY MILLER SEPTIC PUMPING INC, and SPEEDIE SEPTIC & SEWER with a blank operator line. '
                'Several phones print with a leading dash and no leading 1 (e.g. -330-673-6482); GOLD-N-DEUCE LLC '
                'phone prints as - - - (marked unknown). No local registration numbers on this PDF (local REG marked unknown). '
                'ODH statewide bond status is not on this PDF (marked unknown). Separate 2026 installer and '
                'service-provider PDFs in the same Online Forms folder were not used for this hauler table. '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Stark County Health Department '
                'and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-stark-oh.json'
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
  <title>Stark County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Stark County, Ohio registered septage haulers from Stark County Health Department Septage Haulers PDF dated 5 March 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Stark County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Stark County Health Department’s PDF <cite>Septage Haulers</cite> (HDIS list, footer 5 March 2026, 36 TOTAL). Companies that haul septage in Stark County must register with the health department. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 14 October 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">2026 HAULER LIST PDF</a>. Parent page: <a href="{e(PARENT_URL)}">Stark County sewage / environmental health</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Stark County septage-hauler registration only. Local REG # and ODH bond status are <strong>unknown</strong> on this PDF (no registration numbers printed).</p>
      <p>The PDF prints <strong>{n} TOTAL</strong> (footer 03/05/2026). Spellings are as printed (including <code>JJC2, LTD DBA TOM&#x27;S SEPTIC AND SEPTIC</code>, <code>WERAB ENTERPRISES LLC D|B|A FREDS SEPTIC SERV</code>, and <code>ESZBIBB DBA COWBOY MILLER SEPTIC PUMPING INC</code>). <code>SPEEDIE SEPTIC &amp; SEWER</code> prints a blank operator line. Several phones print with a leading dash and no leading 1; <code>GOLD-N-DEUCE LLC</code> prints <code>- - -</code> (shown as unknown). The same Online Forms folder also hosts 2026 installer and service-provider lists — those are separate credentials and are not merged into this hauler table.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="brown.html">Brown County haulers</a> · <a href="summit.html">Summit County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Stark County Health Department, PDF dated 5 March 2026</caption>
      <thead><tr><th>Business</th><th>Operator</th><th>Address</th><th>Phone</th><th>Local REG #</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-stark-oh.json">data/haulers-stark-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, operators, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 14 October 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/stark.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

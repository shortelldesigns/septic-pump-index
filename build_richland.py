#!/usr/bin/env python3
"""Build Richland County OH septage haulers page + JSON from Richland Public Health PDF (footer 06/12/2026)."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://richlandhealth.org/wp-content/uploads/2026/06/SEWAGE-HAULERS-06-12-2026.pdf'
PARENT_URL = 'https://richlandhealth.org/home-health-services/sewage-treatment-companies/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-06-12'
RETRIEVED = '2026-11-04'
ARCHIVE = 'data/sources/richland-oh-2026-hauler-list.pdf'
ARCHIVE_TXT = 'data/sources/richland-oh-2026-hauler-list.txt'

# Hand-transcribed from pdftotext -layout; spellings as printed.
R = [
    ("A-1 SEPTIC TANK CLEANING, LLC", "MIKE MUTCHLER", "1892 BELL RD WOOSTER, OH 44691", "1-419-368-3566"),
    ("ACTION DRAIN & SEPTIC", "PAMELA BLANTON", "253 9TH AVE MANSFIELD, OH 44905", "1-419-774-0323"),
    ("ASHLAND PRICE SEPTIC", "JEREMY YOUNCE", "734 TOWNSHIP RD 462 SULLIVAN, OH 44880", "1-419-606-2644"),
    ("B & B DRAIN SERVICE", "STEVEN R BROWN SR", "401 ASHLAND RD MANSFIELD, OH 44901", "1-419-524-1992"),
    ("BOND SEPTIC SERVICE", "RICK BOND", "247 EAST CHESROWN RD MANSFIELD, OH 44903", "1-419-564-1359"),
    ("JAKE'S JOHNS", "JAKE HOVERSTOCK", "2227 ST RT 179 JEROMESVILLE, OH 44840", "1-419-606-1357"),
    ("JOHN R HORNING FOR RICK BOND-LAND APP", "JOHN R. HORNING", "5923 MANSFIELD ADARIO RD GREENWICH, OH 44837", ""),
    ("JOHN'S SEPTIC", "JOHN VERMILYA", "2186 STATE ROUTE 179 JEROMESVILLE, OH 44840", "1-419-606-8418"),
    ("KEITH'S DRAIN & SEPTIC SERVICE INC.", "KEITH SMITH", "1755 ST RT 39 LUCAS, OH 44843", "1-419-571-8573"),
    ("LACEY PASHEILICH EXCAV. DBA WEBBS SEPTIC", "STEVE PASHEILICH", "1460 CHEW RD MANSFIELD, OH 44903", "1-419-522-3539"),
    ("LIBERTY FLUID MANAGEMENT", "ROB CUTLIP", "696 ST RT 39 PERRYSVILLE, OH 44864", "1-330-465-7467"),
    ("MILLER SEPTIC", "SETH MILLER", "2680 COUNTY ROAD 168 DUNDEE, OH 44624", "1-330-893-2355"),
    ("MT SERVICE INC. DBA MILLER PORTABLES", "ANDREW MLLER", "2680 COUNTY ROAD 168 DUNDEE, OH 44624", "1-800-827-6808"),
    ("OYSTER'S RECEPTION & APP.-HAULER'S", "LARRY OYSTER", "444 ST RT 97 BELLVILLE, OH 44813", "1-419-886-2214"),
    ("OYSTER'S RECEPTION & APP.-MATT OYSTER-NMS", "LARRY OYSTER", "444 ST RT 97 E BELLVILLE, OH 44813", ""),
    ("OYSTERS RECEPTION & APP.-CHRIS OYSTER NS", "CHRIS OYSTER", "444 ST RT 97 E BELLVILLE, OH 44813", ""),
    ("SHETLER SERVICES INC.", "GREG SHETLER", "3656 E. MESSNER ROAD WOOSTER, OH 44691", "1-330-988-4373"),
    ("SIDLE SANITATION SOLUTIONS, LLC BUTLER SAN", "HEIDI SIDLE", "3173 BROKAW RD BUTLER, OH 44822", "1-419-595-0701"),
    ("STULL SEPTIC PUMPING LLC", "NATHAN STULL", "17783 APPLE VALLEY ROAD HOWARD, OH 43028", "1-740-504-8741"),
    ("TIDY TIM'S, INC.", "TIMOTHY HACK", "113 E. HIGH STREET EDISON, OH 43320", "1-419-947-3121"),
    ("UBER DROSS HOLDINGS LLC DBA REDBOX PLUS", "SCOTT SELLERS", "119 MAIN STREET BELLVILLE, OH 44813", "1-419-855-5052"),
    ("UNITED RENTALS (NORTH AMERICA), INC. DBA RELI", "RELIABLE ONSITE SERVICES", "1050 KILLIAN RD AKRON, OH 44312", "1-330-733-9000"),
]

def e(s): return html.escape(str(s), quote=True)

def main():
    txt = (ROOT / ARCHIVE_TXT).read_text()
    for needle in ['Septage Haulers', 'Richland Public Health', '06/12/2026', '22 TOTAL']:
        assert needle in txt, needle
    assert len(R) == 22
    flat = re.sub(r'\s+', ' ', txt)
    for name, op, addr, ph in R:
        assert name in txt, name
        assert op in txt, op
        street, city = addr.rsplit(' ', 3)[0], ' '.join(addr.rsplit(' ', 3)[1:])
        assert city in txt, city
        if ph: assert ph in txt, ph
    recs = [{'source_url': SOURCE_URL, 'source_document_date': DOC_DATE, 'retrieved': RETRIEVED,
             'name': n, 'role': 'Richland Public Health registered septage hauler', 'operator': o,
             'address': a, 'phone': p or None, 'odh_bond': 'unknown'} for n, o, a, p in R]
    payload = {'jurisdiction': 'Richland County, Ohio',
               'source': {'publisher': 'Richland Public Health', 'title': 'Septage Haulers (SEWAGE-HAULERS-06-12-2026.pdf)',
                          'url': SOURCE_URL, 'parent_url': PARENT_URL, 'odh_verify_url': ODH_URL,
                          'document_date': DOC_DATE, 'document_date_note': 'Footer 06/12/2026 on both pages; page 2 prints 22 TOTAL; parent page labels it Registered Septage Haulers (Updated 06/12/2026)',
                          'retrieved': RETRIEVED, 'archive': ARCHIVE,
                          'limitations': 'Transcribed as printed. Three rows print no phone (- - - or blank). No registration numbers printed; ODH bond unknown. Hauler registration is not an inspection credential. Not an endorsement.'},
               'record_count': len(recs), 'records': recs}
    (ROOT / 'data/haulers-richland-oh.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    rows = []
    for r in recs:
        if r['phone']:
            pc = f'<td class="phones"><a href="tel:+{e(r["phone"])}">{e(r["phone"])}</a></td>'
        else:
            pc = '<td class="phones unknown">unknown</td>'
        rows.append(f'<tr><td>{e(r["name"])}</td><td>{e(r["operator"])}</td><td>{e(r["address"])}</td>{pc}<td class="unknown">unknown</td><td class="unknown">unknown</td></tr>')
    tpl = (ROOT / 'oh/mahoning.html').read_text()
    head, rest = tpl.split('<main id="content" class="wide">', 1)
    _, foot = rest.split('</main>', 1)
    head = head.replace('Mahoning County OH Septage Haulers', 'Richland County OH Septage Haulers')
    head = re.sub(r'<meta name="description" content="[^"]*">',
        '<meta name="description" content="22 Richland County, Ohio (Mansfield) registered septage haulers from Richland Public Health\'s list updated 12 June 2026. Local registration plus ODH bond. Pumping is not an inspection.">'.replace("'", '&#x27;'), head)
    head = head.replace('oh/mahoning.html', 'oh/richland.html')
    foot = re.sub(r'Last updated [^<]*\(US/Pacific\)', 'Last updated 4 November 2026 (US/Pacific)', foot)
    main = f'''<main id="content" class="wide">
    <h1 class="page">Richland County, Ohio — registered septage haulers</h1>
    <p class="fold-cta"><a class="btn" href="#pumpers">See all 22 Richland County haulers</a></p>
    <p class="lede">Transcribed from Richland Public Health’s PDF <cite>Septage Haulers</cite> (footer 12 June 2026, 22 TOTAL). Companies that pump and haul septage in Richland County (Mansfield, Shelby, Ontario, Lexington, Bellville) must register with Richland Public Health. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 4 November 2026 (US/Pacific). Official file: <a href="{SOURCE_URL}">SEWAGE-HAULERS-06-12-2026.pdf</a>. Parent page: <a href="{PARENT_URL}">Richland Public Health Sewage Treatment Companies</a> (labeled “Registered Septage Haulers (Updated 06/12/2026)”). Verify statewide bonds via <a href="{ODH_URL}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Richland County septage-hauler registration only. Local REG # and ODH bond status are <strong>unknown</strong> on this PDF (no registration numbers printed).</p>
      <p>The PDF prints <strong>22 TOTAL</strong> and we list all 22 rows. Three rows print no phone (the two Oyster’s land-application rows for Matt and Chris Oyster, and John R Horning for Rick Bond); those are marked unknown. Spellings are as printed, including <code>MLLER</code>, <code>WEBBS</code>, <code>ADARIO</code>, and the truncated <code>DBA RELI</code> on the United Rentals row. Richland Public Health: 555 Lexington Ave, Mansfield, OH 44907, phone <a href="tel:+14197744500">1-419-774-4500</a>.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Pumping a tank is not an inspection. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="ashland.html">Ashland County haulers</a> · <a href="marion.html">Marion County haulers</a>.</p>
    </div>
    <div class="table-wrap" id="pumpers"><table>
      <caption>22 registered septage haulers from Richland Public Health, PDF dated 12 June 2026</caption>
      <thead><tr><th>Business</th><th>Operator</th><th>Address</th><th>Phone</th><th>Local REG #</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-richland-oh.json">data/haulers-richland-oh.json</a>. Archived PDF: <a href="../{ARCHIVE}">{ARCHIVE}</a>. Names, operators, phones, and addresses are as printed on the county PDF.</p>
  </main>'''
    (ROOT / 'oh/richland.html').write_text(head + main + foot)
    print('ok', len(recs))

if __name__ == '__main__':
    main()

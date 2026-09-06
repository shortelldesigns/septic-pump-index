#!/usr/bin/env python3
"""Build McLean County IL licensed septic pumpers JSON + HTML from county Health Dept PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://www.mcleancountyil.gov/DocumentCenter/View/23368/0601-30-Pumper-list-2026'
PARENT_URL = 'https://health.mcleancountyil.gov/1733/Septic-Systems-Contractor-Information'
IDPH_URL = 'https://dph.illinois.gov/'
DOC_DATE = '2026-05-12'
RETRIEVED = '2026-09-05'
ARCHIVE = 'data/sources/mclean-il-pumper-list-2026.pdf'

# Hand-verified from pdftotext -layout of 0601-30-Pumper-list-2026.pdf (Revised: May 12, 2026).
# List is licensed individuals (pumpers), not a firm-only roster. Do not invent fields.
RECORDS = [
    {
        'pumper': 'Fogle, Darrin',
        'business': 'Blue Springs, Inc.',
        'address': '9868 E 2100 N Road, Carlock, IL 61725',
        'phone_business': '(309) 825-2583',
        'phone_mobile': '(309) 825-2583',
        'notes': '',
    },
    {
        'pumper': 'Goembel, Keith',
        'business': 'Popejoy Plumbing, Heating & Electric, Inc.',
        'address': '203 S Tenth St., Fairbury, IL 61739',
        'phone_business': '(815) 692-4471',
        'phone_mobile': '(815) 848-0122',
        'notes': '',
    },
    {
        'pumper': 'Golliday, James',
        'business': 'Popejoy Plumbing, Heating & Electric, Inc.',
        'address': '203 S Tenth St., Fairbury, IL 61739',
        'phone_business': '(815) 692-4471',
        'phone_mobile': '(815) 822-6665',
        'notes': '',
    },
    {
        'pumper': 'Gulliford, David',
        'business': 'Illinois Portable Toilets',
        'address': '2903 Tatman Court, Urbana, IL 61802',
        'phone_business': '(217) 344-5004',
        'phone_mobile': '',
        'notes': '',
    },
    {
        'pumper': 'Hewitt, Joshua',
        'business': 'Midwest Pottyhouse, Inc',
        'address': 'P.O. Box 6627, Champaign, IL 61826',
        'phone_business': '(217) 356-5555',
        'phone_mobile': '217-530-5165',
        'notes': '',
    },
    {
        'pumper': 'Higgs, William R',
        'business': 'Wild Wood Camp Ground',
        'address': '28773 E. 900 N Road, Ellsworth, IL 61737',
        'phone_business': '(309) 724-8342',
        'phone_mobile': '',
        'notes': 'NOT FOR HIRE',
    },
    {
        'pumper': 'Lane, Dwight',
        'business': 'Blue Springs, Inc.',
        'address': '9868 E 2100 N Road, Carlock, IL 61725',
        'phone_business': '(309) 825-2583',
        'phone_mobile': '',
        'notes': '',
    },
    {
        'pumper': 'Killian, Steve',
        'business': 'Johnny on the Spot',
        'address': 'P.O. Box 131, Gibson City, IL 60936',
        'phone_business': '(217) 249-7706',
        'phone_mobile': '',
        'notes': '',
    },
    {
        'pumper': 'Lanham, Ryan',
        'business': 'Zeschke Environmental',
        'address': '2408 Greyhound Road, Bloomington, IL 61704',
        'phone_business': '(309) 808-1847',
        'phone_mobile': '(309) 531-7581',
        'notes': '',
    },
    {
        'pumper': 'McBrayer, Scott',
        'business': 'McBrayer Sanitary Service',
        'address': '29362 E. 1300 N Road, Ellsworth, IL 61737',
        'phone_business': '(309) 724-8417',
        'phone_mobile': '(309) 261-6076',
        'notes': '',
    },
    {
        'pumper': 'McBrayer, Steven',
        'business': 'McBrayer Sanitary Service',
        'address': '29362 E. 1300 N Road, Ellsworth, IL 61737',
        'phone_business': '(309) 533-9812',
        'phone_mobile': '(309) 533-9812',
        'notes': '',
    },
    {
        'pumper': 'Meiss, Aaron',
        'business': 'Popejoy Plumbing, Heating & Electric, Inc.',
        'address': '203 S Tenth St., Fairbury, IL 61739',
        'phone_business': '(815) 692-4471',
        'phone_mobile': '(815) 848-0574',
        'notes': '',
    },
    {
        'pumper': 'Nolen, Daniel',
        'business': 'Nolen Services, LLC',
        'address': '401 W. Birch Street, Stonington, IL 62567',
        'phone_business': '(217) 827-3621',
        'phone_mobile': '(217) 825-3850',
        'notes': '',
    },
    {
        'pumper': 'Nolen, Jeffrey',
        'business': 'Nolen Services, Inc.',
        'address': '401 W. Birch Street, Stonington, IL 62567',
        'phone_business': '(217) 325-4021',
        'phone_mobile': '(217) 827-3450',
        'notes': '',
    },
    {
        'pumper': 'Popejoy, Dustin',
        'business': 'Popejoy Plumbing, Heating & Electric, Inc.',
        'address': '203 S Tenth St., Fairbury, IL 61739',
        'phone_business': '(815) 692-4471',
        'phone_mobile': '(815) 848-4147',
        'notes': '',
    },
    {
        'pumper': 'Sheridan, John',
        'business': 'Popejoy Plumbing, Heating & Electric, Inc.',
        'address': '203 S Tenth St., Fairbury, IL 61739',
        'phone_business': '(815) 692-4471',
        'phone_mobile': '(815) 844-9747',
        'notes': '',
    },
    {
        'pumper': 'Zeschke, Cody',
        'business': 'Zeschke Septic',
        'address': '2408 Greyhound Road, Bloomington, IL 61704',
        'phone_business': '(309) 808-2776',
        'phone_mobile': '(309) 826-8283',
        'notes': '',
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


def e(s):
    return html.escape(str(s), quote=True)


def phone_cell(printed):
    printed = (printed or '').strip()
    if not printed:
        return '<td class="unknown">unknown</td>'
    digits = re.sub(r'\D', '', printed)
    pretty = fmt_phone(printed)
    if len(digits) == 10:
        return f'<td class="phones"><a href="tel:+1{digits}">{e(pretty)}</a></td>'
    if len(digits) == 11 and digits.startswith('1'):
        return f'<td class="phones"><a href="tel:+{digits}">{e(pretty)}</a></td>'
    return f'<td class="phones">{e(pretty)}</td>'


def main():
    assert len(RECORDS) == 17, len(RECORDS)
    # Spot-check PDF text archive still matches our hand list.
    txt = (ROOT / 'data/sources/mclean-il-pumper-list-2026.txt').read_text()
    assert 'Revised: May 12, 2026' in txt
    assert 'MCLEAN COUNTY HEALTH DEPARTMENT' in txt
    for r in RECORDS:
        assert r['pumper'].split(',')[0] in txt, r['pumper']
        assert r['business'].split(',')[0][:12] in txt or r['business'] in txt, r['business']

    records = []
    for r in RECORDS:
        records.append({
            'pumper': r['pumper'],
            'business': r['business'],
            'address': r['address'],
            'phone_business': fmt_phone(r['phone_business']) if r['phone_business'] else None,
            'phone_business_as_printed': r['phone_business'] or None,
            'phone_mobile': fmt_phone(r['phone_mobile']) if r['phone_mobile'] else None,
            'phone_mobile_as_printed': r['phone_mobile'] or None,
            'notes': r['notes'] or None,
            'role': 'McLean County Health Department licensed septic system pumper',
            'source_url': SOURCE_URL,
            'source_document_date': DOC_DATE,
            'retrieved': RETRIEVED,
        })

    payload = {
        'jurisdiction': 'McLean County, Illinois',
        'source': {
            'publisher': 'McLean County Health Department',
            'title': '2026 List of Septic System Pumpers Licensed by the McLean County Health Department',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'idph_url': IDPH_URL,
            'document_date': DOC_DATE,
            'document_date_as_printed': 'Revised: May 12, 2026',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from McLean County Health Department PDF revised May 12, 2026. '
                'The source lists licensed individuals (pumpers), not a firm-only roster. '
                'Higgs, William R is printed NOT FOR HIRE on the PDF. Emails and fax numbers '
                'were not transcribed into the table. A pumper license is not an installer credential. '
                'Appearance is not an endorsement. Confirm with the Health Department before you hire.'
            ),
        },
        'record_count': len(records),
        'for_hire_count': sum(1 for r in records if r['notes'] != 'NOT FOR HIRE'),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-mclean-il.json'
    out_json.write_text(json.dumps(payload, indent=2) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        note = e(r['notes']) if r['notes'] else ''
        note_td = f'<td><strong>{note}</strong></td>' if note else '<td></td>'
        rows.append(
            '<tr>'
            f'<td>{e(r["pumper"])}</td>'
            f'<td>{e(r["business"])}</td>'
            f'<td>{e(r["address"])}</td>'
            + phone_cell(r['phone_business_as_printed'] or '')
            + note_td
            + '</tr>'
        )

    n = len(records)
    for_hire = payload['for_hire_count']
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>McLean County IL Septic Pumpers | Septic Pump Index</title>
  <meta name="description" content="{n} McLean County, Illinois licensed septic system pumpers from the Health Department PDF revised 12 May 2026 ({for_hire} for hire; one marked NOT FOR HIRE). Pumping is not an inspection.">
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
    <h1 class="page">McLean County, Illinois — licensed septic system pumpers</h1>
    <p class="lede">Transcribed from McLean County Health Department’s PDF <cite>2026 List of Septic System Pumpers</cite>, revised 12 May 2026 (<code>0601-30-Pumper-list-2026</code>). The county licenses individuals who may pump septic systems. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 5 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">DocumentCenter/View/23368/0601-30-Pumper-list-2026</a>. Parent page: <a href="{e(PARENT_URL)}">Septic Systems Contractor Information</a>. Statewide context: <a href="{e(IDPH_URL)}">Illinois Department of Public Health</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>This is a list of <strong>licensed pumpers</strong> (people), not a firm-only roster. Several people can share one business name. Phone numbers shown are the <em>Business</em> line from the PDF; mobile and fax lines were not copied into the table.</p>
      <p><strong>Higgs, William R</strong> is printed <code>NOT FOR HIRE</code> on the source (Wild Wood Camp Ground). We keep that row so the transcription matches the PDF, but homeowners should not treat it as an available contractor.</p>
      <p>A pumper license is not an installer credential. McLean County publishes a separate licensed-installers PDF. Pumping a tank is not a full inspection. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} licensed septic system pumpers from McLean County Health Department, PDF revised 12 May 2026 ({for_hire} for hire)</caption>
      <thead><tr><th>Pumper</th><th>Business</th><th>Address</th><th>Business phone</th><th>Notes</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-mclean-il.json">data/haulers-mclean-il.json</a>. Archived PDF: <a href="../data/sources/{e(Path(ARCHIVE).name)}">data/sources/{e(Path(ARCHIVE).name)}</a>. Names, businesses, phones, and the NOT FOR HIRE flag are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 5 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'il/mclean.html'
    out_html.write_text(page)
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

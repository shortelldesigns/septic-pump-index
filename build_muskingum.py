#!/usr/bin/env python3
"""Build Muskingum County OH septage haulers JSON + HTML from ZMCHD 24 Mar 2026 PDF."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://www.zmchd.org/Media/Sewage-Haulers.pdf'
PARENT_URL = 'https://www.zmchd.org/Services/Sewage-Treatment-Systems/'
ODH_URL = 'https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS'
DOC_DATE = '2026-03-24'
RETRIEVED = '2026-09-20'
ARCHIVE = 'data/sources/muskingum-oh-2026-septage-haulers.pdf'
ARCHIVE_TXT = 'data/sources/muskingum-oh-2026-septage-haulers.txt'

# Hand-verified from pdftotext -layout of Sewage-Haulers.pdf
# (Zanesville-Muskingum County Health Department; title 2026 Septage Haulers;
# Expires 12/31/2026; footer DP 3/24/26; CreationDate 24 March 2026 PDT).
# Spellings kept as printed (curly apostrophes in Big Al’s / Jack’s;
# Ohio vs OH in city lines; Const truncation on Jack’s).
# Trailing * / ** role markers on the PDF are not part of the business name —
# documented in callout (PDF prints two different single-* legends).
RECORDS = [
    {'reg': '396', 'name': 'A & J Services, LLC', 'operator': 'John Moore', 'phone': '(740) 819-4405', 'address': '2920 Ridge Rd Zanesville, OH 43701'},
    {'reg': '450', 'name': 'Advanced Septic Service', 'operator': 'Robert Krouskoupf', 'phone': '(740) 819-0754', 'address': '1665 Winfield Circle Nashport, OH 43830'},
    {'reg': '354', 'name': 'Affordable Portables', 'operator': 'Drew Knoesel', 'phone': '(740) 366-1811', 'address': '1000 Keller Drive Heath, OH 43056'},
    {'reg': '361', 'name': 'ASK Services, LLC', 'operator': 'Anthony Kinkade', 'phone': '(740) 891-1010', 'address': '3170 East Pike Zanesville, OH 43701'},
    {'reg': '476', 'name': 'B & C Septic Pumping LLC', 'operator': 'Corey Jones', 'phone': '(740) 607-8807', 'address': '1640 Friendship Dr New Concord, OH 43762'},
    {'reg': '13', 'name': 'Big Al’s Septic Service LLC', 'operator': 'Don Wiseman', 'phone': '(740) 745-1358', 'address': '18600 Buck Hill Rd Frazeysburg, OH 43822'},
    {'reg': '4', 'name': 'Dave Mitchell Septic Service', 'operator': 'Dave Mitchell', 'phone': '(740) 432-3026', 'address': '64818 Haught Road Cambridge, Ohio 43725'},
    {'reg': '437', 'name': 'Eagle Eye Septic Solutions', 'operator': 'Samantha Winters', 'phone': '(740) 454-7867', 'address': '8015 Wonderland Rd Chandlersville, Ohio 43727'},
    {'reg': '378', 'name': 'Emerson Portables', 'operator': 'Lee Emerson', 'phone': '(740) 408-9555', 'address': '7215 Jones Road Nashport, OH 43830'},
    {'reg': '284', 'name': 'Jack’s Septic Tank Cleaning & Const', 'operator': 'Manuel Diaz', 'phone': '(740) 366-3255', 'address': '274 S 6th St Newark, OH 43055'},
    {'reg': '303', 'name': 'JMS Portajon LLC', 'operator': 'Michael Skjerven', 'phone': '(218) 791-4414', 'address': '2100 Mar Mar Ln Navarre, FL 32566'},
    {'reg': '374', 'name': 'Just Clean Cans LLC', 'operator': 'James McCance', 'phone': '(740) 255-0518', 'address': '345 Spring Valley Dr Zanesville, OH 43701'},
    {'reg': '323', 'name': 'King Trucking & Excavating LLC', 'operator': 'James King', 'phone': '(740) 404-7741', 'address': '8280 Canal Rd Frazeysburg, OH 43822'},
    {'reg': '394', 'name': 'Mayfield Septic Service', 'operator': 'Steven Lestock', 'phone': '(740) 452-6242', 'address': '55000 Spencer Rd Cumberland, Ohio 43732'},
    {'reg': '469', 'name': 'Pattison Aerator Repair', 'operator': 'Adam Pattison', 'phone': '(740) 432-5809', 'address': '65641 Cabin Hill Rd New Concord, OH 43762'},
    {'reg': '9', 'name': 'Pro Kleen Industrial Services', 'operator': 'Adam Black', 'phone': '(740) 689-1886', 'address': '1030 Mill Park Drive Lancaster, Ohio 43130'},
    {'reg': '475', 'name': 'Skelley Septic Services LLC', 'operator': 'Ben Skelley and Wes Carder', 'phone': '(330) 826-1112', 'address': '869 Olde Orchard Dr NE Bolivar, OH 44612'},
    {'reg': '447', 'name': 'United Septic Services', 'operator': 'Andrew Harper', 'phone': '(740) 607-3217', 'address': '2595 Virginia Ridge Road Philo, OH 43771'},
    {'reg': '11', 'name': 'Zemba Brothers', 'operator': 'Scott Zemba', 'phone': '(740) 452-1880', 'address': '3401 East Pike Zanesville, Ohio 43701'},
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
    assert len(RECORDS) == 19, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert '2026 Septage Haulers' in txt
    assert 'Expires 12/31/2026' in txt
    assert 'DP 3/24/26' in txt
    assert 'A & J Services, LLC' in txt
    assert 'Big Al' in txt
    assert 'Jack' in txt
    assert 'Zemba Brothers' in txt
    assert 'JMS Portajon LLC' in txt
    assert 'Skelley Septic Services LLC' in txt
    assert 'Navarre, FL 32566' in txt
    assert 'Cambridge, Ohio 43725' in txt
    for r in RECORDS:
        # Strip curly apostrophe variants for assert on ASCII-ish tokens
        token = r['name'].replace('\u2019', "'").split(',')[0][:18]
        assert token.replace("'", "")[:12] in txt.replace('\u2019', "'").replace("'", "") or r['name'].split()[0] in txt, r['name']
        assert r['reg'] in txt, r['reg']
        assert r['phone'] in txt, r['phone']
        op_token = r['operator'].split()[0]
        assert op_token in txt, r['operator']
        street = r['address'].split()[0]
        assert street in txt, r['address']

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
            'registration_number': r['reg'],
            'name': r['name'],
            'role': 'Zanesville-Muskingum County Health Department registered septage hauler',
            'operator': r['operator'],
            'address': r['address'],
            'phone': r['phone'] or None,
            'odh_bond': 'unknown',
        })

    payload = {
        'jurisdiction': 'Muskingum County, Ohio',
        'source': {
            'publisher': 'Zanesville-Muskingum County Health Department',
            'title': '2026 Septage Haulers (Sewage-Haulers.pdf)',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'odh_verify_url': ODH_URL,
            'document_date': DOC_DATE,
            'document_date_note': 'PDF footer DP 3/24/26; title 2026 Septage Haulers; Expires 12/31/2026; CreationDate 24 March 2026 PDT; linked from Sewage Treatment Systems',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from Zanesville-Muskingum County Health Department 2026 Septage Haulers PDF '
                '(Sewage-Haulers.pdf; footer DP 3/24/26; Expires 12/31/2026; 19 named haulers). '
                'Spellings kept as printed including curly apostrophes in Big Al’s / Jack’s, '
                'Jack’s … & Const truncation, and Ohio vs OH in city lines. '
                'Trailing * / ** markers on some PDF name lines indicate additional install/inspect roles; '
                'the PDF footer prints **Can install, inspect and pump and two different single-* legends '
                '(inspect and pump vs install and pump) — markers stripped from business names here; '
                'this page is the septage-hauler roster only. '
                'Local registration numbers are as printed. ODH statewide bond status is not on this PDF (marked unknown). '
                'A septage hauler registration is not a service-provider inspection credential. '
                'Appearance is not an endorsement. Verify with Zanesville-Muskingum County Health Department and ODH before you hire.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-muskingum-oh.json'
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        phone = r['phone'] or ''
        rows.append(
            '<tr>'
            f'<td>{e(r["registration_number"])}</td>'
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
  <title>Muskingum County OH Septage Haulers | Septic Pump Index</title>
  <meta name="description" content="{n} Muskingum County, Ohio registered septage haulers from Zanesville-Muskingum County Health Department 2026 Septage Haulers PDF dated 24 March 2026. Local registration plus ODH bond. Pumping is not an inspection.">
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
    <h1 class="page">Muskingum County, Ohio — registered septage haulers</h1>
    <p class="lede">Transcribed from Zanesville-Muskingum County Health Department’s PDF <cite>2026 Septage Haulers</cite> (<code>Sewage-Haulers.pdf</code>, footer 24 March 2026; expires 31 December 2026). Companies that haul septage in Muskingum County must register with the health department. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 20 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">Sewage-Haulers.pdf</a>. Parent page: <a href="{e(PARENT_URL)}">Sewage Treatment Systems</a>. Verify statewide bonds via <a href="{e(ODH_URL)}">ODH Information for Contractors</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>Ohio requires registration with <em>each</em> local health district (ORC 3718 / OAC 3701-29-03) plus a statewide surety bond at the Ohio Department of Health. This table is Muskingum County septage-hauler registration only. ODH bond status is <strong>unknown</strong> on this PDF.</p>
      <p>The PDF lists <strong>{n}</strong> named haulers (footer <code>DP 3/24/26</code>; expires 12/31/2026). Spellings are as printed (including curly apostrophes in <code>Big Al’s</code> / <code>Jack’s</code>, <code>Jack’s … &amp; Const</code> truncation, and <code>Ohio</code> vs <code>OH</code> in city lines). Registration numbers are the local ZMCHD numbers from the PDF. Some PDF name lines carry trailing <code>*</code> or <code>**</code> role markers (footer: <code>**</code> can install, inspect and pump; the PDF also prints two different single-<code>*</code> legends). Markers are not part of the business name here; this page is the septage-hauler roster only.</p>
      <p>A septage hauler registration is not a service-provider inspection credential. Point-of-sale inspections are a separate registration category in Ohio. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a> · <a href="coshocton.html">Coshocton County haulers</a> · <a href="licking.html">Licking County haulers</a>.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} registered septage haulers from Zanesville-Muskingum County Health Department, PDF dated 24 March 2026</caption>
      <thead><tr><th>Reg #</th><th>Business</th><th>Operator</th><th>Address</th><th>Phone</th><th>ODH bond</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-muskingum-oh.json">data/haulers-muskingum-oh.json</a>. Archived PDF: <a href="../{e(ARCHIVE)}">{e(ARCHIVE)}</a>. Names, registration numbers, operators, phones, and addresses are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 20 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'oh/muskingum.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

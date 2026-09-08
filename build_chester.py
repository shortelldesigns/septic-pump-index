#!/usr/bin/env python3
"""Build Chester County PA licensed liquid waste pumpers JSON + HTML."""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_URL = 'https://www.chesco.org/DocumentCenter/View/75806/Liquid-Waste-Pumpers'
PARENT_URL = 'https://www.chesco.org/983/Sewage-and-Water-Contractors'
SEWAGE_URL = 'https://www.chesco.org/365/Sewage-Water'
DEP_URL = 'https://www.pa.gov/services/dep/water/clean-water/register-a-residential-septage-hauler'
DOC_DATE = '2026-07-28'
RETRIEVED = '2026-09-07'
ARCHIVE = 'data/sources/chester-pa-liquid-waste-pumpers.pdf'
ARCHIVE_TXT = 'data/sources/chester-pa-liquid-waste-pumpers.txt'

# Hand-verified from pdftotext -layout of CCHD Liquid Waste Pumpers
# (Date last revised: 7-28-26). 58 rows. Keep odd spellings and phone
# formatting as printed (Plumsteaville; Ink`s backtick; mixed dashes).
# DEP transporter numbers are not on this county PDF.
RECORDS = [
    {'license': 'LWH-951', 'name': 'A-1 Sanitation Service Inc.', 'address': '1009 River RD, New Castle, DE 19720', 'phone': '302-322-1074'},
    {'license': 'LWH-2110', 'name': 'Ace Disposal Corp', 'address': 'PO Box 571, Plumsteaville, PA 18949', 'phone': '6106443685'},
    {'license': 'LWH-2086', 'name': 'Action Plumbing', 'address': '7 E Stow RD, Marlton, NJ 08053', 'phone': '856-985-9909'},
    {'license': 'LWH-1049', 'name': 'Arf Rental Services Inc', 'address': '181 Old Post RD, Southport, CT 06890', 'phone': '877-234-6545'},
    {'license': "LWH-2147", 'name': "Bailey's Septic Service, Inc.", 'address': '4224 Pottsville PK, Reading, PA 19605', 'phone': '6109291500'},
    {'license': 'LWH-2074', 'name': 'BobCat Septic Services', 'address': 'P.O. Box 57, Kelton, PA 19346', 'phone': '610-467-0248'},
    {'license': 'LWH-967', 'name': 'Bollinger Septic Services', 'address': '3811 Hay Creek RD, Birdsboro, PA 19508', 'phone': '610-286-7306'},
    {'license': 'LWH-2126', 'name': 'Brandywine Portables LLC', 'address': '816 PENNS GROVE RD, Lincoln University, PA 19352', 'phone': '6108690443'},
    {'license': 'LWH-949', 'name': 'Brandywine Septic Services Inc.', 'address': '816 Penns Grove RD, Lincoln University, PA 19352', 'phone': '610-869-0443'},
    {'license': 'LWH-954', 'name': 'C M Kristman Waste Removal', 'address': '1099 Cannery RD, Coatesville, PA 19320', 'phone': '610-347-0688'},
    {'license': 'LWH-2132', 'name': 'Carter & Son Lawncare, Inc.', 'address': '263 MOUNT OLIVET RD, Oxford, PA 19363', 'phone': '4846145320'},
    {'license': 'LWH-2127', 'name': 'Class A Septic Services', 'address': '329 Pleasant Valley RD, Ephrata, PA 17522', 'phone': '7173141229'},
    {'license': 'LWH-989', 'name': "Cook's Disposal Service, Inc.", 'address': '1851 Pottstown PK, Pottstown, PA 19465', 'phone': '610-469-1222'},
    {'license': 'LWH-2122', 'name': 'Cooper Septic LLC', 'address': '1920 Oldfield Point RD, Elkton, MD 21921', 'phone': '4109200096'},
    {'license': 'LWH-2035', 'name': 'Delaware Valley Septic, Sewer & Storm', 'address': '504 Eagle RD, Springfield, PA 19064', 'phone': '6109474800'},
    {'license': 'LWH-957', 'name': 'Eldredge Septic', 'address': '520 S Caln RD, Coatesville, PA 19320', 'phone': '610-918-8600'},
    {'license': 'LWH-956', 'name': 'Fins Environmental Service LLC', 'address': '691 Truce RD, Quarryville, PA 17566', 'phone': '717-284-5228'},
    {'license': 'LWH-901', 'name': 'Frank Sears Sanitation', 'address': '509 Lime Quarry RD, Gap, PA 17527', 'phone': '717-442-8609'},
    {'license': 'LWH-920', 'name': 'Gray Brothers Inc', 'address': '501 S Main ST, Spring City, PA 19475', 'phone': '610-644-2800'},
    {'license': 'LWH-2', 'name': 'Hickman Sanitation Service', 'address': '352 Snyder AV, West Chester, PA 19381', 'phone': '610-696-3060'},
    {'license': 'LWH-2146', 'name': 'Hoodz of Exton', 'address': '521 POTTSTOWN PK, Chester Springs, PA 19335', 'phone': '4848750777'},
    {'license': 'LWH-931', 'name': "Hooper's Disposal", 'address': '265 Lippitt RD, Honey Brook, PA 19344', 'phone': '610-942-3222'},
    {'license': 'LWH-908', 'name': 'Ink`s Disposal Service', 'address': '564 N Manor RD, Elverson, PA 19520', 'phone': '610-286-5488'},
    {'license': 'LWH-926', 'name': 'J Gallagher Septic & Waste Water Control', 'address': '1606 Embreeville RD, Coatesville, PA 19320', 'phone': '610-466-7500'},
    {'license': 'LWH-2136', 'name': 'J. Beaver Construction', 'address': '1640 Farmington AV, Pottstown, PA 19464', 'phone': '4845767136'},
    {'license': 'LWH-907', 'name': 'John B Seldomridge Jr. Inc.', 'address': '31 LANCHESTER RD, Narvon, PA 17555', 'phone': '610-273-3316'},
    {'license': 'LWH-2071', 'name': 'John Kline Septic Services, LLC', 'address': '3869 Old Harrisburg PK, Mount Joy, PA 17552', 'phone': '717-898-2333'},
    {'license': 'LWH-922', 'name': 'Kelly Phillips Septic Services', 'address': '139 Parkesburg RD, Coatesville, PA 19320', 'phone': '610-857-9263'},
    {'license': 'LWH-928', 'name': 'Kulp & Sons Septic Services LLC', 'address': '889 Farmington AV, Pottstown, PA 19464', 'phone': '610-948-4593'},
    {'license': 'LWH-2133', 'name': 'L & C Septic Pumping LLC', 'address': '2659 Geryville PK, Pennsburg, PA 18073', 'phone': '2673793629'},
    {'license': 'LWH-2031', 'name': 'Lander Septic Service LLC', 'address': '267 Red Pump RD, Nottingham, PA 19362', 'phone': '484-758-0870'},
    {'license': 'LWH-948', 'name': 'Levengood Septic Service', 'address': '287 Buckhead LA, Douglassville, PA 19518', 'phone': '610-689-0113'},
    {'license': 'LWH-1004', 'name': "Manny's Septic", 'address': 'PO Box 72831, Thorndale, PA 19372', 'phone': '610-755-2639'},
    {'license': 'LWH-976', 'name': 'Marks Septic Service Inc DBA Lonnie Stoltzfus Septic Service', 'address': '81 Horseshoe LA, Shillington, PA 19607', 'phone': '610-913-0707'},
    {'license': 'LWH-2143', 'name': 'Marquez Dumping Services LLC', 'address': '2680 Robert Fulton HW, Peach Bottom, PA 17563', 'phone': '4849881001'},
    {'license': 'LWH-915', 'name': 'McGovern Environmental', 'address': '920 S Bolmar ST, West Chester, PA 19382', 'phone': '610-458-9333'},
    {'license': 'LWH-966', 'name': 'National Construction Rentals', 'address': '6401 S Passyunk AV, Philadelphia, PA 19153', 'phone': '610-623-6860'},
    {'license': 'LWH-912', 'name': 'Old Mill Septic Services LLC', 'address': '113 Old Mill, Coatesville, PA 19320', 'phone': '484-880-5566'},
    {'license': 'LWH-959', 'name': 'Onsite Management Inc.', 'address': 'P.O. Box 2313, West Chester, PA 19380', 'phone': '610-430-3100'},
    {'license': 'LWH-986', 'name': 'Peters Septic', 'address': '117 Keys RD, Peach Bottom, PA 17563', 'phone': '717-786-1454'},
    {'license': 'LWH-953', 'name': 'Pierson Environmental Services, LLC', 'address': '195 Laurel Heights RD, Landenberg, PA 19350', 'phone': '610-274-8252'},
    {'license': 'LWH-2109', 'name': 'Port A Bowl Restroom Co.', 'address': 'PO Box 571, Plumsteaville, PA 18949', 'phone': '2157668164'},
    {'license': 'LWH-992', 'name': 'Predoc, Inc', 'address': '14 Chrisevyn LA, Phoenixville, PA 19460', 'phone': '610-935-8590'},
    {'license': 'LWH-923', 'name': 'Prettyman Services LLC', 'address': 'P O Box 26, Oxford, PA 19363', 'phone': '610-932-5270'},
    {'license': 'LWH-942', 'name': 'R & K Septic & Services Inc.', 'address': '1657 S Glenside RD, West Chester, PA 19380', 'phone': '610-486-6915'},
    {'license': 'LWH-1031', 'name': 'R.D. Excavating Co. Inc', 'address': 'PO Box 519, Glenmoore, PA 19343', 'phone': '610-942-4902'},
    {'license': 'LWH-2142', 'name': 'Rick Birney, Inc.', 'address': '110 Fox Chase DR, Elkton, MD 21921', 'phone': '4103987422'},
    {'license': 'LWH-2064', 'name': 'Septic Services, Inc.', 'address': "1237 W King's HW, Coatesville, PA 19320", 'phone': '610-547-1592'},
    {'license': 'LWH-1000', 'name': 'Septic Solutions', 'address': '310 Tick Hill RD, Kirkwood, PA 17536', 'phone': '7175290931'},
    {'license': 'LWH-962', 'name': 'Sharp Septic', 'address': '85 Esbenshade RD, Ronks, PA 17572', 'phone': '717-354-6147'},
    {'license': 'LWH-985', 'name': 'Snyder & Mylin Septic Services LLC', 'address': '1130 Lancaster PK, Drumore, PA 17518', 'phone': '717-284-0303'},
    {'license': 'LWH-2139', 'name': 'Sonco LLC', 'address': '2044 W Main ST, Ephrata, PA 17522', 'phone': '7177381917'},
    {'license': 'LWH-2141', 'name': 'Turd Burglar LLC', 'address': '16 Rando LA, Rising Sun, MD 21911', 'phone': '4432569019'},
    {'license': 'LWH-2102', 'name': 'Walters Portable Toilets', 'address': 'P.O. Box 340, Grantville, PA 17028', 'phone': '7174699440'},
    {'license': 'LWH-2103', 'name': 'Weaver Septic Services LLC', 'address': '670 W Girl Scout RD, Stevens, PA 17578', 'phone': '7177332339'},
    {'license': 'LWH-921', 'name': 'William P. McGovern Inc', 'address': '920 S Bolmar ST, West Chester, PA 19382', 'phone': '610-444-5797'},
    {'license': 'LWH-941', 'name': "Wind River Environmental LLC dba Kline's Services LLC", 'address': '5 Holland ST, Salunga, PA 17538', 'phone': '717-459-8033'},
    {'license': 'LWH-2092', 'name': 'Zoom Drain', 'address': '500 Davis DR, Plymouth Meeting, PA 19462', 'phone': '6106500555'},
]


def e(s):
    return html.escape(str(s), quote=True)


def phone_digits(s):
    return re.sub(r'\D', '', s or '')


def phone_cell(printed):
    digits = phone_digits(printed)
    if not digits:
        return '<td class="unknown">unknown</td>'
    return f'<td class="phones"><a href="tel:+1{digits}">{e(printed)}</a></td>'


def main():
    assert len(RECORDS) == 58, len(RECORDS)
    txt = (ROOT / ARCHIVE_TXT).read_text()
    assert 'Date last revised: 7-28-26' in txt
    assert 'Liquid Waste Pumpers' in txt
    assert 'Chester County Health Department' in txt
    for r in RECORDS:
        assert r['license'] in txt, r['license']
        # Names with backtick or apostrophe as on PDF
        assert r['name'] in txt, r['name']
        assert r['phone'] in txt, r['phone']
        # Address street portion before first comma
        street = r['address'].split(',')[0]
        assert street in txt, street

    records = []
    for r in RECORDS:
        records.append({
            'license_number': r['license'],
            'name': r['name'],
            'address': r['address'],
            'phone': r['phone'],
            'phone_digits': phone_digits(r['phone']),
            'role': 'Chester County PA licensed liquid waste pumper',
            'source_url': SOURCE_URL,
            'source_document_date': DOC_DATE,
            'retrieved': RETRIEVED,
        })

    payload = {
        'jurisdiction': 'Chester County, Pennsylvania',
        'source': {
            'publisher': 'Chester County Health Department',
            'title': 'Liquid Waste Pumpers',
            'url': SOURCE_URL,
            'parent_url': PARENT_URL,
            'sewage_program_url': SEWAGE_URL,
            'dep_url': DEP_URL,
            'document_date': DOC_DATE,
            'document_date_as_printed': 'Date last revised: 7-28-26',
            'retrieved': RETRIEVED,
            'archive': ARCHIVE,
            'limitations': (
                'Transcribed from the Chester County Health Department Liquid Waste Pumpers PDF '
                'last revised 7-28-26. CCHD license numbers (LWH-*) and phones as printed; '
                'odd spellings (Plumsteaville; Ink`s) kept as printed. DEP statewide transporter '
                'numbers are not on this county PDF. Appearance is not an endorsement. Confirm '
                'current licensure with CCHD before you hire. A liquid waste pumper license is '
                'not an inspection credential.'
            ),
        },
        'record_count': len(records),
        'records': records,
    }

    out_json = ROOT / 'data/haulers-chester-pa.json'
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print('wrote', out_json, 'count', len(records))

    rows = []
    for r in records:
        rows.append(
            '<tr>'
            f'<td>{e(r["license_number"])}</td>'
            f'<td>{e(r["name"])}</td>'
            f'<td>{e(r["address"])}</td>'
            + phone_cell(r['phone'])
            + '</tr>'
        )

    n = len(records)
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Chester County PA Septic Pumpers | Septic Pump Index</title>
  <meta name="description" content="{n} Chester County, Pennsylvania licensed liquid waste pumpers from the CCHD PDF last revised 28 July 2026. Pumping is not an inspection.">
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
    <h1 class="page">Chester County, Pennsylvania — licensed liquid waste pumpers</h1>
    <p class="lede">Transcribed from Chester County Health Department’s PDF <cite>Liquid Waste Pumpers</cite>, date last revised 28 July 2026. We list every CCHD Nr row on that roster. We did not add companies from business directories.</p>
    <p class="meta">Source retrieved 7 September 2026 (US/Pacific). Official file: <a href="{e(SOURCE_URL)}">Liquid Waste Pumpers</a>. Parent: <a href="{e(PARENT_URL)}">Licensed Contractors in Chester County</a>. Sewage program: <a href="{e(SEWAGE_URL)}">Sewage &amp; Water</a>. Statewide DEP registration: <a href="{e(DEP_URL)}">Register a Residential Septage Hauler</a>.</p>
    <div class="callout">
      <h2>How to read this table</h2>
      <p>CCHD licenses liquid waste pumpers under Chapter 504. The <strong>CCHD Nr</strong> column is the county license as printed (LWH-*). Phones and addresses are as printed — including odd spellings such as Plumsteaville and the backtick in Ink`s.</p>
      <p>Pennsylvania also requires DEP registration for residential septage haulers. DEP transporter numbers are <strong>not</strong> on this county PDF, so they are not invented here.</p>
      <p>A liquid waste pumper license is not a septic inspection credential. Pumping a tank is not a full inspection. <a href="../how-often-to-pump.html">How often to pump</a> · <a href="../inspection-before-sale.html">Inspection before sale</a>.</p>
      <p>The PDF says data is subject to change; call CCHD at 610-344-6688 with questions, and confirm current licensure before you hire.</p>
    </div>
    <div class="table-wrap"><table>
      <caption>{n} licensed liquid waste pumpers from CCHD PDF last revised 28 July 2026</caption>
      <thead><tr><th>CCHD Nr</th><th>Company</th><th>Address</th><th>Phone</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody></table></div>
    <p>Machine-readable copy: <a href="../data/haulers-chester-pa.json">data/haulers-chester-pa.json</a>. Archived PDF: <a href="../data/sources/{e(Path(ARCHIVE).name)}">data/sources/{e(Path(ARCHIVE).name)}</a>. Names, license numbers, addresses, and phones are as printed on the county PDF.</p>
  </main>
  <footer class="site">
    <div class="inner">
      <p class="byline"><strong>Septic Pump Index</strong> is a project by Shortell Designs. Last updated 7 September 2026 (US/Pacific).</p>
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
    out_html = ROOT / 'pa/chester.html'
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding='utf-8')
    print('wrote', out_html, len(page), 'bytes')


if __name__ == '__main__':
    main()

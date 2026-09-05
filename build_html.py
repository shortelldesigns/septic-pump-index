#!/usr/bin/env python3
"""Write static HTML pages from transcribed JSON. No invented rows."""
from __future__ import annotations

import json
from pathlib import Path

from html_common import ROOT, TAG, UPDATED, e, unknown_cell, wrap, table

DATA = ROOT / "data"


def load(name: str):
    return json.loads((DATA / name).read_text())


def td(val, unknown=True) -> str:
    if unknown:
        return unknown_cell(val)
    return f"<td>{e(val)}</td>"


def write_index(mt, nd, clp, clo, cld):
    main = f"""    <h1 class="page">{e(TAG)}</h1>
    <p class="lede">EPA’s septic-care page: inspect at least every three years (once a year for many alternative systems) and plan to pump a typical household tank every three to five years. This site transcribes who is actually licensed on the official lists we could fetch — Montana, North Dakota, and Clallam County, Washington.</p>
    <p class="meta">Directory first published 29 August 2026 (US/Pacific). EPA <cite>How to Care for Your Septic System</cite> last updated 17 August 2026; EPA frequent questions last updated 11 March 2026 (inspect every 1 to 3 years; pump every 3 to 5 years).</p>

    <div class="flow">
      <article>
        <span class="step">1. Inspect</span>
        <h2>Every 1–3 years (EPA)</h2>
        <p>EPA: a typical household system should be inspected at least every three years; alternative systems with pumps or electrical parts generally once a year. EPA’s frequent questions also say inspections should be done every 1 to 3 years. <a href="inspection.html">Inspection is not a pump</a>.</p>
      </article>
      <article>
        <span class="step">2. Pump</span>
        <h2>Every 3–5 years (EPA)</h2>
        <p>EPA: household septic tanks are typically pumped every three to five years. How often depends on household size, wastewater volume, solids, and tank size. <a href="when-to-pump.html">When to pump, with citations</a>.</p>
      </article>
      <article>
        <span class="step">3. Hire from a list</span>
        <h2>Then confirm the license</h2>
        <p>Names below come from state and county PDFs. Appearance is not an endorsement. <a href="verify.html">How to verify a license</a>.</p>
      </article>
    </div>

    <h2>Live directories</h2>
    <div class="cards two">
      <div class="card">
        <h3><a href="montana.html">Montana — {mt['pumper_count']} licensed pumpers</a></h3>
        <p>Montana DEQ <cite>2026 Licensed Montana Septic Pumpers</cite> as of 20 May 2026. License number, county, and company. Phone is not on that PDF.</p>
      </div>
      <div class="card">
        <h3><a href="north-dakota.html">North Dakota — {nd['pumper_count']} Class I/II pumpers</a></h3>
        <p>ND DEQ <cite>2026 Annual Active ND Sanitary Pumper List</cite>, licensed on or before 23 July 2026. {nd['class_i_count']} Class I and {nd['class_ii_count']} Class II. A sanitary-pumper permit is not an inspection credential.</p>
      </div>
      <div class="card">
        <h3><a href="clallam-county-wa.html">Clallam County, WA — {clp['pumper_count']} pumpers and {clo['inspector_count']} O&amp;M inspectors</a></h3>
        <p>County pumper PDF (printed 17 April 2026) plus the O&amp;M inspector PDF (printed 3 June 2026). The inspector PDF also names {cld['designer_count']} local designers for permit-related inspections. Clallam: a septic pumping is not an inspection.</p>
      </div>
    </div>

    <h2>Before you hire</h2>
    <ul>
      <li><a href="when-to-pump.html">When to pump</a> — EPA scum and sludge cutoffs, water use, drainfield care.</li>
      <li><a href="inspection.html">Sale / O&amp;M inspection vs a pump</a> — what EPA says an inspection checks, and when Clallam requires a designer.</li>
      <li><a href="verify.html">Verify a license</a> — MT DEQ, ND DEQ, Clallam County, then ask your own county.</li>
    </ul>

    <div class="callout">
      <h2>What this site will not do</h2>
      <p>We do not invent companies, phones, licenses, or counties. If a field is not on the official list, it is marked unknown. We do not rank pumpers. We do not treat a pump as an inspection. There are no live affiliate links and no click-to-call numbers on this version.</p>
    </div>"""
    (ROOT / "index.html").write_text(
        wrap(
            "Septic Pump Index — County-licensed septic pumpers and inspectors",
            TAG,
            "index.html",
            main,
        )
    )


def write_when_to_pump():
    main = """    <h1 class="page">When to pump a septic tank</h1>
    <p class="lede">EPA’s homeowner page is the source for the intervals on this site. Local rules can be stricter. A pump-out empties sludge and scum; it is not the same job as an operations-and-maintenance inspection.</p>
    <p class="meta">Primary source: U.S. EPA, <a href="https://www.epa.gov/septic/how-care-your-septic-system">How to Care for Your Septic System</a>, last updated 17 August 2026. Supporting: EPA frequent questions, last updated 11 March 2026; EPA <cite>Homebuyer’s Guide to Septic Systems</cite>, EPA-832-F-17-010, August 2017.</p>

    <h2>EPA intervals</h2>
    <ul>
      <li>Inspect at least every three years by a septic service professional. Alternative systems with electrical float switches, pumps, or mechanical components should be inspected more often, generally once a year. A service contract matters for those systems because they have mechanized parts. (How to Care, 17 August 2026.)</li>
      <li>Household septic tanks are typically pumped every three to five years. (How to Care.)</li>
      <li>EPA’s frequent questions, 11 March 2026: “In general, a septic tank should be inspected every 1 to 3 years and pumped every 3 to 5 years.”</li>
    </ul>
    <p>How to Care lists the major factors that influence how often to pump: household size, total wastewater generated, volume of solids in wastewater, and septic tank size.</p>

    <h2>When the tank is due, not the calendar</h2>
    <p>EPA (How to Care): when you call a septic service provider, that person will inspect for leaks and examine the scum and sludge layers. Your tank should be pumped if:</p>
    <ul>
      <li>the bottom of the scum layer is within six inches of the bottom of the outlet, or</li>
      <li>the top of the sludge layer is within 12 inches of the outlet, or</li>
      <li>more than 25 percent of the liquid depth is sludge and scum.</li>
    </ul>
    <p>EPA: write down the sludge and scum levels. Keep maintenance records. The service provider should note repairs and tank condition. If other repairs are recommended, hire a repair person soon.</p>
    <p>The T-shaped outlet is there to keep sludge and scum out of the drainfield. Pumping protects that outlet. It does not, by itself, evaluate the drainfield, distribution box, or electrical controls. <a href="inspection.html">Inspection vs pump</a>.</p>

    <h2>Garbage disposals and water use change the clock</h2>
    <p>EPA frequent questions: using an in-sink garbage disposal can mean more frequent pumping because food waste accumulates as scum and sludge. How to Care: eliminate or limit a garbage disposal; spread laundry through the week rather than doing it all in one day; fix leaks (a running toilet can add as much as 200 gallons a day).</p>

    <h2>What not to put in the tank</h2>
    <p>EPA: flush only human waste and toilet paper. Never flush grease, non-flushable wipes, feminine hygiene products, condoms, dental floss, diapers, cigarette butts, coffee grounds, cat litter, paper towels, pharmaceuticals, or household chemicals such as gasoline, oil, pesticides, antifreeze, and paint thinners. Pouring toxins can kill the organisms that treat waste.</p>

    <h2>Drainfield</h2>
    <p>EPA: do not park or drive on the drainfield; plant trees the appropriate distance away; keep roof drains, sump pumps, and other rainwater away from the drainfield. Excess water slows treatment.</p>

    <div class="callout">
      <h2>Use a licensed pumper</h2>
      <p>This site transcribes official lists for <a href="montana.html">Montana</a>, <a href="north-dakota.html">North Dakota</a>, and <a href="clallam-county-wa.html">Clallam County, Washington</a>. Elsewhere, <a href="verify.html">ask the county or state program</a>. We do not rank those names.</p>
    </div>

    <div class="cite">
      <h2>Sources</h2>
      <ol>
        <li>U.S. EPA, <a href="https://www.epa.gov/septic/how-care-your-septic-system">How to Care for Your Septic System</a>, last updated 17 August 2026.</li>
        <li>U.S. EPA, <a href="https://www.epa.gov/septic/frequent-questions-septic-systems">Frequent Questions on Septic Systems</a>, last updated 11 March 2026 (Maintaining / Inspecting).</li>
        <li>U.S. EPA, <cite>Homebuyer’s Guide to Septic Systems</cite>, EPA-832-F-17-010, August 2017, <a href="https://www.epa.gov/sites/default/files/2017-08/documents/170803-homebuyerssepticguide_508c.pdf">PDF</a>.</li>
      </ol>
    </div>"""
    (ROOT / "when-to-pump.html").write_text(
        wrap(
            "When to pump a septic tank — Septic Pump Index",
            "EPA intervals: inspect every 1 to 3 years, pump a typical household tank every 3 to 5 years.",
            "when-to-pump.html",
            main,
        )
    )


def write_inspection():
    main = """    <h1 class="page">Sale inspection and O&amp;M inspection are not a pump</h1>
    <p class="lede">A pump-out removes sludge and scum from the tank. An inspection evaluates whether the system is working — tank, baffles, drainfield, and, where they exist, pumps and alarms. Counties may also require a licensed designer for permits. Those are different jobs, sometimes different licenses.</p>
    <p class="meta">EPA How to Care last updated 17 August 2026; EPA frequent questions last updated 11 March 2026; EPA Homebuyer’s Guide, August 2017. Clallam County O&amp;M list printed 3 June 2026; Clallam system-status and inspection-summary pages retrieved 29 August 2026.</p>

    <div class="callout">
      <h2>Clallam County’s sentence, which other counties may also mean</h2>
      <p>The 2026 Clallam County O&amp;M provider PDF: “You must use a Clallam County licensed inspection provider to be counted as a qualified inspection. A septic pumper/septic pumping is NOT considered an inspection.” Clallam’s O&amp;M program page says the same in other words: simply pumping the tank — while important — is not adequate unless all system components are professionally evaluated as well.</p>
    </div>

    <h2>What EPA says an inspection checks</h2>
    <p>EPA frequent questions (Inspecting Septic Systems, 11 March 2026): inspections are not only for a real-estate transfer. “Septic system inspections should be done every 1 to 3 years for as long as you own your home.” In many states a system must be inspected when real estate transfers. EPA tells you to contact the local permitting authority for professional inspectors — EPA does not license them.</p>
    <p>EPA’s August 2017 Homebuyer’s Guide: have the system inspected by a septic system service provider before you purchase a home. Inspections may be required by local or state government or by a mortgage lender. The inspector will check:</p>
    <ul>
      <li>pumping and maintenance records;</li>
      <li>age of the system;</li>
      <li>sludge levels and scum thickness;</li>
      <li>signs of leakage (low water in the tank) and backup (staining above the outlet pipe);</li>
      <li>integrity of the tank, inlet, and outlet pipes;</li>
      <li>the drainfield for signs of failure such as standing water;</li>
      <li>the distribution box, to see that drain lines receive equal flow;</li>
      <li>available records for local function and location rules.</li>
    </ul>
    <p>EPA How to Care (servicing): the provider inspects for leaks and measures scum and sludge, then pumps when those layers hit the cutoffs on the <a href="when-to-pump.html">when-to-pump</a> page. Measuring layers can happen during an inspection visit; emptying the tank is the pump.</p>

    <h2>O&amp;M inspection (ongoing)</h2>
    <p>EPA How to Care: inspect at least every three years; alternative systems with pumps or electrical parts generally once a year. Washington state rules that Clallam implements (WAC 246-272A, cited on the county pages): a traditional gravity system at least once every three years; alternative systems (those with pumps) every year.</p>
    <p>Clallam’s O&amp;M page describes a professional inspection that includes tank leaks, baffles and baffle screen, scum and sludge, color and odor, backup stains, and — for pressurized systems — pump tank, floats, effluent pump, electrical controls, alarms, and a pressure test, plus drainfield mushy spots and the distribution box. Findings are reported to Environmental Health as a system status report.</p>
    <p>Some Clallam homeowners may inspect their own residential system after county training (Septics 201) if the county has a complete record on file. Proprietary devices, aerobic treatment units, biofilters, community/commercial systems, real-estate transfers, and government actions are called out as professional work. That is Clallam’s rule, not a national rule.</p>

    <h2>Sale / property-transfer inspection</h2>
    <p>EPA Homebuyer’s Guide: inspect before purchase; local government or a lender may require it. EPA frequent questions: in many states a system must be inspected with the transfer of real estate. EPA does not publish a 50-state mandate table; we do not invent one.</p>
    <p>Clallam County (System Status Reports page): as of 1 June 2010, at property transfer the owner shall provide the buyer a copy of a current system status report performed within 12 months of the transfer by a licensed septic system designer or licensed OSS maintenance provider, on file with Environmental Health, plus any available maintenance records. The county says a system status report evaluates condition at the time of inspection and does not guarantee future performance.</p>
    <p>Clallam also tells owners not to pump just before a system status report for a governmental action: a designer can tell more about how the system is functioning if the tank has not just been pumped.</p>

    <h2>When a designer is required (Clallam example)</h2>
    <p>The reverse of Clallam’s 2026 O&amp;M PDF: only septic designers can perform inspections for food-service permit/annual permitting, building permits, boundary line adjustments, lot combinations, land divisions, and conditional use permits. The PDF lists local designers who offer those inspections and states the list is not inclusive of all Washington State licensed septic designers.</p>
    <p>Clallam’s System Status Reports page: reports for governmental actions (building permits, land divisions or boundary line adjustments when an existing system is part of the proposal, conditional use, critical-areas compliance, food-service operating permits, commercial certificate of occupancy, change of use, and other actions the health officer deems appropriate) are inspections done by certified septic designers. Designers verify tank location, sludge and scum, working parts, drainfield function, and a reserve area if the as-built lacks one.</p>
    <p>That split — licensed O&amp;M provider for routine and many sale inspections; licensed designer for permit and land-use inspections — is what Clallam printed. Other counties write different rules. Ask yours. <a href="clallam-county-wa.html">Clallam pumpers, O&amp;M inspectors, and designers</a>.</p>

    <div class="callout">
      <h2>Do not hire from the wrong list</h2>
      <p>Montana’s and North Dakota’s 2026 PDFs are pumper licenses. They do not say those firms are inspectors. Clallam publishes pumpers and inspectors on separate PDFs. If your county only publishes haulers, that is not an inspector roster.</p>
    </div>

    <div class="cite">
      <h2>Sources</h2>
      <ol>
        <li>U.S. EPA, <a href="https://www.epa.gov/septic/how-care-your-septic-system">How to Care for Your Septic System</a>, last updated 17 August 2026.</li>
        <li>U.S. EPA, <a href="https://www.epa.gov/septic/frequent-questions-septic-systems">Frequent Questions on Septic Systems</a>, Inspecting / Maintaining, last updated 11 March 2026.</li>
        <li>U.S. EPA, <cite>Homebuyer’s Guide to Septic Systems</cite>, EPA-832-F-17-010, August 2017, <a href="https://www.epa.gov/sites/default/files/2017-08/documents/170803-homebuyerssepticguide_508c.pdf">PDF</a>.</li>
        <li>Clallam County, <a href="https://clallamcountywa.gov/DocumentCenter/View/4653/Septic-Maintenance-Providers-PDF">2026 Licensed Sewage System Inspection &amp; Maintenance Providers (O&amp;M)</a>, printed 6.03.26.</li>
        <li>Clallam County, <a href="https://clallamcountywa.gov/1463/Operations-and-Maintenance-OM-Program">Operations and Maintenance (O&amp;M) Program</a>; <a href="https://www.clallamcountywa.gov/485/Summary-of-Septic-System-Inspection-Requ">Summary of Septic System Inspection Requirements</a>; <a href="https://www.clallamcountywa.gov/499/Septic-System-Status-Reports">System Status Reports &amp; Sanitary Surveys</a>. Retrieved 29 August 2026.</li>
      </ol>
    </div>"""
    (ROOT / "inspection.html").write_text(
        wrap(
            "Inspection vs a pump — Septic Pump Index",
            "Sale and O&M inspections are not a pump. Clallam requires a designer for many permit inspections.",
            "inspection.html",
            main,
        )
    )


def write_montana(mt):
    rows = []
    for r in mt["pumpers"]:
        rows.append(
            [
                f"<td>{e(r['license_number'])}</td>",
                f"<td>{e(r['name'])}</td>",
                f"<td>{e(r['county'])}</td>",
                unknown_cell(r.get("phone")),
            ]
        )
    tbl = table(
        f"{mt['pumper_count']} pumpers from Montana DEQ, as of 20 May 2026 (one duplicate license line omitted)",
        ["License", "Company", "County", "Phone"],
        rows,
    )
    main = f"""    <h1 class="page">Montana licensed septic pumpers, 2026</h1>
    <p class="lede">Transcribed from Montana Department of Environmental Quality, <cite>2026 Licensed Montana Septic Pumpers As of May 20, 2026</cite>. We did not add companies from business directories.</p>
    <p class="meta">Official file retrieved 29 August 2026: <a href="https://deq.mt.gov/files/Land/SolidWaste/Documents/pumpers/2026%20licensed%20pumpers.pdf">2026 licensed pumpers PDF</a>. PDF created 20 May 2026 (UTC) by DEQ’s Oracle Reports. Program page: <a href="https://deq.mt.gov/twr/Programs/septic-tank">Septic Tank Pumper</a>. DEQ: licenses expire 31 December.</p>

    <div class="callout">
      <h2>How to read this table</h2>
      <p>The PDF columns are license number, county, and company. Phone and street address are <strong>unknown</strong> — they are not on this list. County “Out Of State” is printed on the source. License S-1181 (ROCKY MOUNTAIN SEPTIC SERVICES LLC) appears twice in a row on the PDF; it is listed once here.</p>
      <p>This is a pumper license list. DEQ does not, on this PDF, say these firms are inspectors. <a href="inspection.html">A pump is not an inspection</a>.</p>
    </div>

{tbl}
    <p>Machine-readable copy: <a href="data/montana-pumpers.json">data/montana-pumpers.json</a>. Every record includes this source URL. Confirm a current license with DEQ before you hire. <a href="verify.html">How to verify</a>.</p>"""
    (ROOT / "montana.html").write_text(
        wrap(
            "Montana licensed septic pumpers 2026 — Septic Pump Index",
            f"{mt['pumper_count']} Montana DEQ licensed septic pumpers as of 20 May 2026.",
            "montana.html",
            main,
            wide=True,
        )
    )


def write_nd(nd):
    rows = []
    for r in nd["pumpers"]:
        rows.append(
            [
                f"<td>{e(r['name'])}</td>",
                f"<td>{e(r['pumper_class'])}</td>",
                unknown_cell(r.get("county")),
                unknown_cell(r.get("phone")),
                f"<td>{e(r['permit_number'])}</td>",
                unknown_cell(r.get("permit_issuance_date")),
                unknown_cell(r.get("permit_expiration_date")),
                f"<td>{e(r.get('address'))}</td>",
            ]
        )
    tbl = table(
        f"{nd['pumper_count']} sanitary pumpers licensed on or before 23 July 2026 ({nd['class_i_count']} Class I, {nd['class_ii_count']} Class II)",
        ["Company", "Class", "County", "Phone", "Permit", "Issued", "Expires", "Address"],
        rows,
    )
    main = f"""    <h1 class="page">North Dakota Class I and Class II sanitary pumpers, 2026</h1>
    <p class="lede">Transcribed from North Dakota Department of Environmental Quality, <cite>2026 Annual Active ND Sanitary Pumper List</cite>. The PDF header: pumpers listed were licensed on or before 07/23/2026.</p>
    <p class="meta">Official file retrieved 29 August 2026: <a href="https://deq.nd.gov/publications/WQ/2_NDPDES/SepticPumper/rptBusnList.pdf">rptBusnList.pdf</a>. Excel metadata on the PDF: modified 23 July 2026 (UTC). Program page: <a href="https://deq.nd.gov/WQ/2_NDPDES_Permits/6_SepticPumper/sp.aspx">Septic Pumper Permits</a>. DEQ: permits expire 31 December.</p>

    <div class="callout">
      <h2>How to read this table</h2>
      <p>Class I and Class II are DEQ sanitary-pumper permit classes (equipment and land-application rules), not inspection credentials. Five rows have a blank county on the PDF (Minnesota street addresses); county is marked unknown. Phones that the PDF stored as 10-digit strings are shown with dashes; no digits were added. License-plate numbers are in the JSON only.</p>
      <p>A sanitary-pumper permit authorizes servicing septage structures. It is not, on this list, an O&amp;M or sale-inspection license. <a href="inspection.html">A pump is not an inspection</a>.</p>
    </div>

{tbl}
    <p>Machine-readable copy: <a href="data/north-dakota-pumpers.json">data/north-dakota-pumpers.json</a>. Every record includes this source URL. <a href="verify.html">How to verify</a>.</p>"""
    (ROOT / "north-dakota.html").write_text(
        wrap(
            "North Dakota Class I and Class II septic pumpers 2026 — Septic Pump Index",
            f"{nd['pumper_count']} ND DEQ sanitary pumpers licensed on or before 23 July 2026.",
            "north-dakota.html",
            main,
            wide=True,
        )
    )


def write_clallam(clp, clo, cld):
    p_rows = []
    for r in clp["pumpers"]:
        notes = r.get("notes") or r.get("scope")
        if notes == "unknown":
            notes = None
        p_rows.append(
            [
                f"<td>{e(r['name'])}</td>",
                unknown_cell(r.get("contact")),
                unknown_cell(r.get("city")),
                unknown_cell(r.get("phone")),
                unknown_cell(r.get("email")),
                unknown_cell(notes) if notes else "<td></td>",
            ]
        )
    p_tbl = table(
        f"{clp['pumper_count']} firms from the 2026 Clallam County licensed septic pumpers PDF (printed 17 April 2026)",
        ["Company", "Contact", "City", "Phone", "Email", "Notes on the PDF"],
        p_rows,
    )

    o_rows = []
    for r in clo["inspectors"]:
        o_rows.append(
            [
                f"<td>{e(r['name'])}</td>",
                f"<td>{e(r.get('inspectors'))}</td>",
                unknown_cell(r.get("city")),
                unknown_cell(r.get("phone")),
                unknown_cell(r.get("email")),
                f"<td>{e(r.get('address'))}</td>",
            ]
        )
    o_tbl = table(
        f"{clo['inspector_count']} licensed O&amp;M inspection and maintenance providers for routine or property-sale inspections only (printed 3 June 2026)",
        ["Company", "Named on the list", "City", "Phone", "Email", "Address"],
        o_rows,
    )

    d_rows = []
    for r in cld["designers"]:
        phone = r.get("phone")
        extra = r.get("phone_note")
        phone_cell = unknown_cell(phone)
        if extra:
            phone_cell = f"<td>{e(phone)} <span class=\"unknown\">({e(extra)})</span></td>"
        d_rows.append(
            [
                f"<td>{e(r['name'])}</td>",
                f"<td>{e(r.get('inspectors'))}</td>",
                unknown_cell(r.get("city")),
                phone_cell,
                unknown_cell(r.get("email")),
            ]
        )
    d_tbl = table(
        f"{cld['designer_count']} local state-licensed designers on the reverse of the O&amp;M PDF — not a complete statewide designer roster",
        ["Company", "Named on the list", "City", "Phone", "Email"],
        d_rows,
    )

    main = f"""    <h1 class="page">Clallam County, Washington — pumpers and inspectors</h1>
    <p class="lede">Two county PDFs. Pumpers and O&amp;M inspectors are separate licenses. The O&amp;M PDF says a septic pumping is not an inspection, and that only designers may do specified permit inspections.</p>
    <p class="meta">Retrieved 29 August 2026. Pumpers: <a href="https://clallamcountywa.gov/DocumentCenter/View/4655/Septic-Tank-Pumpers-PDF">Septic Tank Pumpers PDF</a> (printed 04.17.26). O&amp;M inspectors and local designers: <a href="https://clallamcountywa.gov/DocumentCenter/View/4653/Septic-Maintenance-Providers-PDF">Septic Maintenance Providers PDF</a> (printed 6.03.26). County: <a href="https://www.clallamcountywa.gov/1474/On-site-Septic-Professionals-Contacts-De">On-site Septic Professionals</a>.</p>

    <div class="callout">
      <h2>Use the list that matches the job</h2>
      <ul>
        <li>Pump-out — licensed pumper table.</li>
        <li>Routine O&amp;M or many property-sale system status reports — licensed inspection and maintenance provider table.</li>
        <li>Food-service permitting, building permits, boundary line adjustments, lot combinations, land divisions, conditional use — designer table. The PDF says only septic designers can perform those inspections.</li>
      </ul>
      <p>Phones are printed as text, not click-to-call. Confirm the current county PDF before you hire. Environmental Health (from the county O&amp;M page): 360-417-2506.</p>
    </div>

    <h2>Licensed pumpers and portable-toilet providers</h2>
    <p>Title on the PDF: 2026 Clallam County Licensed Septic Pumpers and Portable Toilet (Sani-Can) Providers. Bill’s Plumbing is labeled SANIKANS ONLY. Peninsula Drain &amp; Septic is labeled Septic Tanks only. Those notes are copied, not edited away. West Waste has no email on the PDF.</p>
{p_tbl}
    <p>JSON: <a href="data/clallam-pumpers.json">data/clallam-pumpers.json</a>.</p>

    <h2>O&amp;M inspectors (routine or property sale only)</h2>
    <p>Title on the PDF: 2026 Clallam County Licensed Sewage System Inspection &amp; Maintenance Providers (O&amp;M) for Routine or Property Sale Inspections ONLY. All ’N All Septic. has no ZIP on the PDF.</p>
{o_tbl}
    <p>JSON: <a href="data/clallam-om-inspectors.json">data/clallam-om-inspectors.json</a>.</p>

    <h2>Local designers for permit inspections</h2>
    <p>Reverse of the same O&amp;M PDF. The county: this local list is not inclusive of all Washington State licensed septic designers. Shold Excavating’s designer-side phone is transcribed as printed; the PDF text layer ends at 360-385-048.</p>
{d_tbl}
    <p>JSON: <a href="data/clallam-designers.json">data/clallam-designers.json</a>. More on when a designer is required: <a href="inspection.html">inspection vs pump</a>.</p>"""
    (ROOT / "clallam-county-wa.html").write_text(
        wrap(
            "Clallam County WA septic pumpers and O&M inspectors — Septic Pump Index",
            f"{clp['pumper_count']} licensed pumpers, {clo['inspector_count']} O&M inspectors, {cld['designer_count']} local designers from Clallam County 2026 PDFs.",
            "clallam-county-wa.html",
            main,
            wide=True,
        )
    )


def write_verify():
    main = """    <h1 class="page">How to check a septic pumper or inspector license</h1>
    <p class="lede">This site is a transcription of public lists, not a live license server. Lists go stale. Confirm with the agency that issued the credential before you hire.</p>
    <p class="meta">Agency pages and PDFs retrieved 29 August 2026 (US/Pacific).</p>

    <h2>Montana</h2>
    <p>DEQ licenses septic tank pumpers. The public list we transcribed is <a href="https://deq.mt.gov/files/Land/SolidWaste/Documents/pumpers/2026%20licensed%20pumpers.pdf">2026 Licensed Montana Septic Pumpers as of 20 May 2026</a>. Program: <a href="https://deq.mt.gov/twr/Programs/septic-tank">Septic Tank Pumper</a>.</p>
    <ul>
      <li>Match the company name and the S- license number on the current PDF — not only on this site.</li>
      <li>DEQ (program page): licenses expire 31 December. Renewal applications must be received no later than 31 January. Licensees have until 1 April to renew without a late fee.</li>
      <li>Contacts printed on that program page: Solid Waste Management Section Supervisor Fred Collins, 406-444-9879; Waste Management Specialist Lillian Kurzhal, 406-444-1808; Data Control Technician Andrea Staley, 406-444-3493. DEQ headquarters phone on the same page: 406-444-2544.</li>
    </ul>
    <p>That PDF is a pumper list. It is not an inspector roster.</p>

    <h2>North Dakota</h2>
    <p>DEQ issues yearly sanitary-pumper permits. The list we transcribed is <a href="https://deq.nd.gov/publications/WQ/2_NDPDES/SepticPumper/rptBusnList.pdf">2026 Annual Active ND Sanitary Pumper List</a> (licensed on or before 23 July 2026). Program: <a href="https://deq.nd.gov/WQ/2_NDPDES_Permits/6_SepticPumper/sp.aspx">Septic Pumper Permits</a>.</p>
    <ul>
      <li>Match company name and permit number (NDSP…) on the current PDF.</li>
      <li>DEQ (program page): all permits expire 31 December; renewal begins 1 January; deadline 1 March; later renewals pay new-applicant fees.</li>
      <li>Class I vs Class II on the list is a pumper classification, not an inspection license.</li>
      <li>Division of Water Quality switchboard on the DEQ site: 701-328-5150, deq@nd.gov. NDPDES permitting contacts on that staff table include Alexis Delzer, 701-328-5282, and Benjamin Westercamp, 701-328-6032 (the PDF author).</li>
    </ul>

    <h2>Clallam County, Washington</h2>
    <p>The county publishes separate PDFs. Use the one that matches the job.</p>
    <ul>
      <li>Pumpers: <a href="https://clallamcountywa.gov/DocumentCenter/View/4655/Septic-Tank-Pumpers-PDF">Septic Tank Pumpers PDF</a>.</li>
      <li>Routine / property-sale O&amp;M inspectors: <a href="https://clallamcountywa.gov/DocumentCenter/View/4653/Septic-Maintenance-Providers-PDF">Septic Maintenance Providers PDF</a>.</li>
      <li>Permit-related inspections: designers on the reverse of that O&amp;M PDF, which says the local list is not all Washington licensed designers.</li>
      <li>Professionals hub: <a href="https://www.clallamcountywa.gov/1474/On-site-Septic-Professionals-Contacts-De">On-site Septic Professionals</a>.</li>
      <li>Environmental Health, from the county O&amp;M page: 360-417-2506.</li>
    </ul>
    <p>The O&amp;M PDF: a septic pumper/septic pumping is not considered an inspection.</p>

    <h2>Ask your county</h2>
    <p>EPA does not license residential septic pumpers or inspectors. Frequent questions (11 March 2026): contact your local permitting authority (local health or environmental department) for professional inspectors. EPA How to Care (17 August 2026) describes what a service visit should include; it does not publish a national roster.</p>
    <p>If your county is not Montana, North Dakota, or Clallam, we do not invent a stand-in list. Ask:</p>
    <ul>
      <li>Who licenses pumpers here, and is there a current public list?</li>
      <li>Who may perform an O&amp;M inspection vs a real-estate inspection vs a permit/system-status inspection?</li>
      <li>Does a pump-out count as the required inspection? (In Clallam, no.)</li>
    </ul>
    <p>Then compare the name and credential number on the agency’s current file — not a screenshot of this site.</p>"""
    (ROOT / "verify.html").write_text(
        wrap(
            "How to verify a septic license — Septic Pump Index",
            "Check MT DEQ, ND DEQ, and Clallam County lists, then ask your own county. EPA does not license pumpers.",
            "verify.html",
            main,
        )
    )


def write_about(mt, nd, clp, clo, cld):
    main = f"""    <h1 class="page">About Septic Pump Index</h1>
    <p class="lede">A directory by Shortell Designs. We transcribe official state and county pumper and inspector lists. We do not invent records.</p>
    <p class="meta">First version published 29 August 2026 (US/Pacific).</p>

    <h2>What we are</h2>
    <p>Septic Pump Index helps a tank owner find a pumper or inspector who actually appears on a current official list, and to tell a pump from an inspection. It is not a government website, not a pumper, and not a real-estate inspector.</p>

    <h2>Methodology</h2>
    <ul>
      <li>Roster rows are transcribed from official PDFs. Each JSON record carries a <code>source_url</code> and document date.</li>
      <li>If a field is not on the source (Montana phones, five North Dakota counties, a Clallam ZIP), we write <strong>unknown</strong> or omit it and link the official file.</li>
      <li>We do not copy business-directory phones or “enrich” records from Google, Yelp, or company marketing sites.</li>
      <li>We do not attach affiliate tracking numbers, UTM codes, or call-tracking numbers to roster names.</li>
      <li>A pumper list is not converted into an inspector list. Clallam’s O&amp;M PDF is explicit that a pumping is not an inspection.</li>
      <li>Guidance pages quote or closely paraphrase EPA and the county pages cited, with dates.</li>
      <li>We do not rank companies, invent statistics, or unsourced prices.</li>
    </ul>
    <p>This version’s live rosters:</p>
    <ul>
      <li>Montana DEQ pumpers: {mt['pumper_count']} (as of 20 May 2026; one duplicate PDF line omitted).</li>
      <li>North Dakota DEQ Class I/II sanitary pumpers: {nd['pumper_count']} ({nd['class_i_count']} Class I, {nd['class_ii_count']} Class II), licensed on or before 23 July 2026.</li>
      <li>Clallam County pumpers: {clp['pumper_count']} (printed 17 April 2026); O&amp;M inspectors: {clo['inspector_count']}; local designers on the reverse of the O&amp;M PDF: {cld['designer_count']} (printed 3 June 2026).</li>
    </ul>
    <p>How to add a list: <a href="README.md">README.md</a>. What we fetched: <a href="SOURCES.md">SOURCES.md</a>.</p>

    <h2>Commission disclosure</h2>
    <p>Septic Pump Index is intended to become an income site. In later versions we may earn a commission if you buy a related product or service through a link. <strong>This version has no live affiliate links, no paid placements, and no click-to-call numbers.</strong> Roster names do not carry tracking numbers. Listings are not advertisements. Appearance on an official list is not an endorsement by DEQ, the county, or this site.</p>
    <p>If we add affiliate links later, they will be labeled on the page where they appear, and a commission will not decide which company is listed.</p>

    <h2>Contact</h2>
    <p>Byline: Shortell Designs. This static version does not yet publish an editorial email on the public pages; methodology questions belong in the repository documentation until a contact form is added.</p>"""
    (ROOT / "about.html").write_text(
        wrap(
            "About Septic Pump Index — methodology and disclosure",
            "Methodology, source dates, and commission disclosure. No tracking numbers on roster names.",
            "about.html",
            main,
        )
    )


def main():
    mt = load("montana-pumpers.json")
    nd = load("north-dakota-pumpers.json")
    clp = load("clallam-pumpers.json")
    clo = load("clallam-om-inspectors.json")
    cld = load("clallam-designers.json")
    write_index(mt, nd, clp, clo, cld)
    write_when_to_pump()
    write_inspection()
    write_montana(mt)
    write_nd(nd)
    write_clallam(clp, clo, cld)
    write_verify()
    write_about(mt, nd, clp, clo, cld)
    import shutil
    for stale in [
        "how-often-to-pump.html",
        "inspection-before-sale.html",
        "states.html",
        "warning-signs.html",
    ]:
        p = ROOT / stale
        if p.exists():
            p.unlink()
            print("removed", stale)
    for d in ("pa", "oh", "wi"):
        dp = ROOT / d
        if dp.exists():
            shutil.rmtree(dp)
            print("removed dir", d)
    for jf in DATA.glob("haulers-*.json"):
        jf.unlink()
        print("removed", jf.name)
    scripts = ROOT / "scripts"
    if scripts.exists():
        shutil.rmtree(scripts)
        print("removed scripts/")
    print("html written")


if __name__ == "__main__":
    main()

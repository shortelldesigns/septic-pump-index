# Septic Pump Index

Static first version of a U.S. directory to find a licensed septic pumper or inspector by county, plus how-to pages that cite EPA and university extension.

**Homepage line:** Find a licensed septic pumper or inspector in your county — before the tank backs up.

**Byline:** Stephen Shortell / Septic Pump Index (footer only on public HTML)

**Published:** 29 August 2026 (US/Pacific)

Intended GitHub Pages URL (you publish; this repo is the files only):
https://shortelldesigns.github.io/septic-pump-index/

Open `index.html` in a browser. All links are relative; no build step is required. `.nojekyll` is included so GitHub Pages will not process the site with Jekyll.

## Rules (do not break these)

- Never invent a company, phone number, license number, price, or county pumping/inspection requirement.
- If a field is not on the official source, write `unknown` or omit it and link the official tool.
- Do not rank “best septic company.” Do not clone marketplace copy.
- No live affiliate links or click-to-call (`tel:`) numbers in v1.
- Every listing record in `data/*.json` must include a `source_url`.
- Transcribe from official state/county license lists or health department pages you actually fetched.
- A pump is not an inspection. Do not present a pumper roster as an inspector roster.

## How to add a nightly county page

This is a file-based site. A “nightly page” is a new or refreshed HTML file plus, if the roster changed, an updated JSON file.

1. **Pick the official source.** Prefer a county health department, solid-waste authority, or state license roster (PDF, HTML table, or spreadsheet). EPA does not keep a national septic-contractor database. Start from the state agency:
   - Pennsylvania DEP residential septage hauler registration: https://www.pa.gov/services/dep/water/clean-water/register-a-residential-septage-hauler
   - Ohio Department of Health contractor/bond page: https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS (then the local health district’s registered-pumper list)
   - Wisconsin DNR septage business lookup: https://dnr.wisconsin.gov/topic/opcert/septageBusiness.html
   - Michigan EGLE Septage program: https://www.michigan.gov/egle/about/organization/drinking-water-and-environmental-health/septage

2. **Fetch and archive.** Download the source to `data/sources/` with `curl`. For PDFs run `pdftotext -layout`. Record the URL, HTTP status, document date, and retrieve date in `SOURCES.md`.

3. **Transcribe, do not enrich.** Copy name, address, phone, contact, and license number only as they appear. Do not fill gaps from Google or the company’s website. Mark missing fields `unknown`. Keep odd spellings that are on the PDF.

4. **Write JSON first.** Add `data/haulers-{county}-{st}.json` with a top-level `source` block (publisher, URL, document date, limitations) and one object per row, each with `source_url`. Follow `data/haulers-york-pa.json`.

5. **Generate the HTML page.** Follow `pa/york.html`, `oh/geauga.html`, or `wi/shawano.html`. Use `css/site.css`. Paths like `pa/lancaster.html` or `oh/geauga.html` are fine. Add the county to `states.html` and the homepage only when the table has real, sourced rows.

6. **Cite dates.** Use the document’s own date plus the retrieve date. Site “last updated” is the calendar day you publish, in US/Pacific.

7. **Do not present a stale statewide dump as current.** If a PDF footer says it was run years ago, log it in `SOURCES.md` and link the live lookup instead of transcribing it as today’s roster.

8. **Log failures.** If a fetch fails (TLS, 404, login wall), say so in `SOURCES.md` and on the state page. Do not substitute an unofficial directory.

## Layout

```
index.html                    homepage
states.html                   live vs coming soon
how-often-to-pump.html        EPA + Penn State Extension
inspection-before-sale.html   EPA homebuyer inspection checklist
warning-signs.html            EPA failure signs
about.html                    methodology + commission disclosure
pa/york.html                  York County, PA haulers
oh/geauga.html                Geauga County, OH pumpers
wi/shawano.html               Shawano County, WI pumpers + POWTS maintainers
montana.html                  Montana DEQ 2026 licensed pumpers
north-dakota.html             ND DEQ Class I/II pumpers
clallam-county-wa.html        Clallam County WA pumpers + O&M inspectors
css/site.css
data/haulers-york-pa.json
data/haulers-geauga-oh.json
data/haulers-shawano-wi.json
data/montana-pumpers.json
data/north-dakota-pumpers.json
data/clallam-*.json
data/sources/                 archived official files
SOURCES.md
RESULT.md
.nojekyll
```

## Local check

```
cd septic-pump-index
python3 -m http.server 8080
# open http://127.0.0.1:8080/
```

Or double-click `index.html`. Relative links work either way.

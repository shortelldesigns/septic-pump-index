# Septic Pump Index

Static first version of a U.S. directory of **county-licensed septic pumpers and inspectors**, transcribed from official state and county lists.

**Homepage line:** County-licensed septic pumpers and inspectors, transcribed from official state and county lists.

**Byline (footer only):** Stephen Shortell

**Published:** 29 August 2026 (US/Pacific)

Open `index.html` in a browser. All links are relative; no build step is required.

## Rules (do not break these)

- Never invent a company, phone number, license, county, or statistic.
- If a field is not on the official source, write `unknown` or omit it and link the source.
- A pump is not an inspection. Do not present a pumper roster as an inspector roster.
- Do not rank companies. Do not add CSIA (chimney) credentials.
- No live affiliate links, no click-to-call (`tel:`) links, and no tracking numbers on roster names.
- Every roster record in `data/*.json` must include a `source_url`.

## How to add a directory page

This is a file-based site. A new directory is an HTML file plus JSON.

1. **Pick the official source.** State environmental agency or county environmental health — a dated pumper PDF, inspector PDF, or license search that can be archived. EPA does not license residential pumpers.

2. **Fetch and archive.** Download to `data/sources/` with `curl`. For PDFs run `pdftotext -layout` (and table extraction when the PDF is a spreadsheet export). Record URL, HTTP status, document date, and retrieve date in `SOURCES.md`.

3. **Transcribe, do not enrich.** Copy name, license, county, phone, and address only as they appear. Do not fill gaps from Google or the company’s site. Mark missing fields `unknown`.

4. **Keep roles separate.** Pumpers, O&M inspectors, and designers go in separate JSON files and separate tables when the source separates them.

5. **Write JSON first.** One object per firm, each with `source_url` and `source_document_date`. Keep a top-level `source` block describing limitations.

6. **Generate the HTML page.** Follow `montana.html` (pumper list with unknown phones) or `clallam-county-wa.html` (two PDFs, three roles). Use `css/site.css`. Link the page from `index.html` only when the table has real, sourced rows.

7. **Cite dates.** Use the document’s own date plus the retrieve date. Site “last updated” is the calendar day you publish, in US/Pacific.

8. **Log failures.** If a fetch fails, say so in `SOURCES.md` and on the directory page. Do not substitute a stale unofficial list.

Rebuild JSON from the archived PDFs:

```
python3 -m venv /tmp/spi-venv && /tmp/spi-venv/bin/pip install pdfplumber
/tmp/spi-venv/bin/python3 build_json.py
python3 build_html.py
```

`build_json.py` needs `pdfplumber` only for the North Dakota spreadsheet-style PDF.

## Layout

```
index.html                 hub (EPA inspect 1–3 yrs / pump 3–5 yrs)
when-to-pump.html          EPA How to Care for Your Septic System
inspection.html            sale/O&M inspection vs a pump; when a designer is required
montana.html               MT DEQ 2026 licensed pumpers
north-dakota.html          ND DEQ 2026 Class I/II sanitary pumpers
clallam-county-wa.html     Clallam pumpers + O&M inspectors (+ local designers)
verify.html                how to check a license (MT / ND / Clallam + ask your county)
about.html                 methodology, source dates, commission disclosure
css/site.css
data/montana-pumpers.json
data/north-dakota-pumpers.json
data/clallam-pumpers.json
data/clallam-om-inspectors.json
data/clallam-designers.json
data/sources/              archived official files
SOURCES.md
RESULT.md
```

## Local check

```
cd septic-pump-index
python3 -m http.server 8080
# open http://127.0.0.1:8080/
```

Or open `index.html`. Relative links work either way.

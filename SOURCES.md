# Sources fetched for Septic Pump Index v1

Retrieve date: **29 August 2026** (US/Pacific; fetch ran 30 August 2026 UTC).

## Succeeded

| Source | URL | Document / page date | Notes |
| --- | --- | --- | --- |
| EPA How to Care for Your Septic System | https://www.epa.gov/septic/how-care-your-septic-system | Last updated 17 August 2026 | WebFetch. Inspect at least every 3 years; alternative systems generally once a year; household tanks typically pumped every 3 to 5 years. Scum/sludge cutoffs (6 in / 12 in / 25%). |
| EPA Frequent Questions on Septic Systems | https://www.epa.gov/septic/frequent-questions-septic-systems | Last updated 11 March 2026 | WebFetch. “Inspected every 1 to 3 years and pumped every 3 to 5 years.” Inspection checklist. Local permitting authority for inspectors. Real-estate inspections in many states. |
| EPA Homebuyer’s Guide to Septic Systems | https://www.epa.gov/sites/default/files/2017-08/documents/170803-homebuyerssepticguide_508c.pdf | EPA-832-F-17-010, August 2017 | curl + pdftotext. Inspect before purchase; may be required by local/state government or lender. What an inspector will check. Archived `data/sources/epa-homebuyers-guide-full-2017.pdf`. |
| EPA Homeowners Guide brochure (same series) | https://www.epa.gov/sites/default/files/2017-08/documents/170803-homebuyerssepticguidebrochurelayout_508c.pdf | August 2017 | curl + pdftotext. Two-page layout of the same homebuyer points. Archived `data/sources/epa-homebuyer-guide-2017.pdf`. |
| Montana DEQ 2026 licensed pumpers PDF | https://deq.mt.gov/files/Land/SolidWaste/Documents/pumpers/2026%20licensed%20pumpers.pdf | As of 20 May 2026 (PDF CreationDate 20 May 2026 06:20 UTC; Oracle Reports) | curl HTTP 200, 10 452 bytes, 6 pages. pdftotext -layout. 153 license lines, **152 unique** S- numbers (S-1181 duplicated). Columns: LIC #, county, company. No phones. Archived `data/sources/mt-2026-licensed-pumpers.pdf`. |
| Montana DEQ Septic Tank Pumper program | https://deq.mt.gov/twr/Programs/septic-tank | Retrieved 29 August 2026 | WebFetch. Licenses expire 31 December. Contacts: Fred Collins 406-444-9879; Lillian Kurzhal 406-444-1808; Andrea Staley 406-444-3493. |
| ND DEQ 2026 Annual Active Sanitary Pumper List | https://deq.nd.gov/publications/WQ/2_NDPDES/SepticPumper/rptBusnList.pdf | Licensed on or before 23 July 2026 (Excel ModDate 23 July 2026 16:43 UTC) | curl HTTP 200, 413 068 bytes, 7 pages. pdfplumber tables. **125** pumpers: 72 Class I, 53 Class II. 5 blank counties (MN street addresses). Archived `data/sources/nd-2026-class-i-ii.pdf`. |
| ND DEQ Septic Pumper Permits | https://deq.nd.gov/WQ/2_NDPDES_Permits/6_SepticPumper/sp.aspx | Retrieved 29 August 2026 | WebFetch. Permits expire 31 December; renewal 1 January–1 March. Staff table includes Alexis Delzer 701-328-5282 and Benjamin Westercamp 701-328-6032. |
| Clallam County licensed pumpers PDF | https://clallamcountywa.gov/DocumentCenter/View/4655/Septic-Tank-Pumpers-PDF | Printed 04.17.26 (Word CreationDate 26 June 2026 21:10 UTC) | curl HTTP 200, 149 843 bytes, 2 pages. pdftotext. **10** firms, including SANIKANS ONLY and Septic Tanks only notes as printed. Archived `data/sources/clallam-septic-tank-pumpers.pdf`. |
| Clallam County O&M inspectors PDF | https://clallamcountywa.gov/DocumentCenter/View/4653/Septic-Maintenance-Providers-PDF | Printed 6.03.26 (Acrobat CreationDate 3 June 2026 23:50 UTC) | curl HTTP 200, 152 079 bytes, 2 pages. pdftotext. Page 1: **11** O&M providers for routine or property-sale inspections only; “a septic pumper/septic pumping is NOT considered an inspection.” Page 2: **6** local designers for specified permit inspections; list is not all WA designers. Archived `data/sources/clallam-septic-maintenance-providers.pdf`. |
| Clallam O&M Program | https://clallamcountywa.gov/1463/Operations-and-Maintenance-OM-Program | Retrieved 29 August 2026 | WebFetch. Gravity inspect every 3 years; alternative every year. Pumping alone is not adequate. EH 360-417-2506. |
| Clallam Summary of Inspection Requirements | https://www.clallamcountywa.gov/485/Summary-of-Septic-System-Inspection-Requ | Retrieved 29 August 2026 | WebFetch. Professional inspection required for real estate or government action. DIY Septics 201 limits. |
| Clallam System Status Reports | https://www.clallamcountywa.gov/499/Septic-System-Status-Reports | Retrieved 29 August 2026 | WebFetch. Sale: current system status report within 12 months by licensed designer or OSS maintenance provider (as of 1 June 2010). Governmental actions: certified septic designers. Do not pump just before a governmental system status report. |
| Clallam On-site Professionals | https://www.clallamcountywa.gov/1474/On-site-Septic-Professionals-Contacts-De | Retrieved 29 August 2026 | WebFetch. Thin JS page; PDFs above are the lists. |

## Failed or incomplete

| Attempt | URL | What happened | What we did instead |
| --- | --- | --- | --- |
| EPA buying-or-selling HTML (guessed path) | https://www.epa.gov/septic/septic-systems-guidance-buying-or-selling-home | WebFetch 404 | Used the August 2017 Homebuyer’s Guide PDF still hosted on epa.gov, plus How to Care and frequent questions. |
| Montana phones / addresses | Same DEQ pumper PDF | Not columns on the PDF | Marked `unknown`. Did not scrape company websites. |
| ND Business County for 5 rows | Same ND list | Blank on the PDF (Minnesota addresses) | County `unknown`. Did not infer “out of state.” |
| Clallam All 'N All ZIP | O&M PDF | ZIP not printed | `unknown`. |
| Clallam Shold designer phone | Reverse of O&M PDF | Text layer ends at `360-385-048` | Transcribed as printed. Did not copy the extra digit from the O&M side of the same PDF. |
| Clallam West Waste email | Pumper PDF | No email line | `unknown`. |

## Not used as roster sources

- Previous-attempt York County PA, Geauga County OH, and Shawano County WI / Wisconsin DNR files (replaced by this locked brief).
- Third-party business directories.
- Company marketing sites used to fill missing phones.
- NOWRA member locator (named by EPA; not transcribed as a roster).

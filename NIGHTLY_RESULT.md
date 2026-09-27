# Nightly Septic Pump Index — 26 September 2026 (PT)

## Shipped
- **Page:** Ashland County, Ohio — registered septage haulers
- **Live URL:** https://shortelldesigns.github.io/septic-pump-index/oh/ashland.html
- **Firm count:** 25 named haulers (PDF prints 25 TOTAL; no local REG. #)
- **Commit:** `8c420ed75934d687f691313c7ff667a71b4b66b0` — *Add Ashland County OH registered septage haulers.*
- **Screenshot:** `/workspace/septic-pump-index/ashland-oh-page-screenshot.png`
- **Live HTTP 200:** verified (Pages briefly 404 then 200; distinctive names `A & B SEPTIC CLEANING` / `DOUBLEFLUSH SEPTIC SERVICES` / `JAKE'S JOHNS` / `SIDLE SANITATION SOLUTIONS,LLC DBA BUTLER SAN` / `UBER DROSS HOLDINGS LLC DBA RED BOX` present; Shortell Designs byline; no Stephen Shortell)

## Official source
- **PDF:** https://www.health-ashlandcounty-oh.gov/wp-content/uploads/2026/08/Haulers.pdf  
  (title **Septage Haulers**; footer **08/05/2026** / 5 August 2026; 25 TOTAL)
- **Parent (Sewage Treatment Systems):** https://www.health-ashlandcounty-oh.gov/services/sewage-treatment-systems/
- **Archive:** `data/sources/ashland-oh-2026-septage-haulers.pdf` (+ `.txt` via `pdftotext -layout`)
- **Fetch note:** plain `curl -L` returned `%PDF`. Linked from Sewage Treatment Systems as **2026 Septage Haulers** (prior night’s `Haulers-2026.PDF.pdf` guess was 404; correct path is `/wp-content/uploads/2026/08/Haulers.pdf`).

## Caveats
No local registration numbers on PDF. Spellings kept as printed (`BLAKE'S`; `BRENNER'S`; `BRENNY'S`; `BURNETT'S`; `DOUBLEFLUSH SEPTIC SERVICES` as one word; `JAKE'S JOHNS`; `SIDLE SANITATION SOLUTIONS,LLC DBA BUTLER SAN`; `UBER DROSS HOLDINGS LLC DBA RED BOX`; `P.O.BOX 391`; `ST. RT. 39`; `MT. GILEAD`). **ODH statewide bond marked unknown**. Pumping is not an inspection.

## Candidates skipped tonight
- Warren County OH: official HTML septage-hauler table live (40 firms) at warrencohealthoh.gov; page warns list may not be most up to date; preferred dated 2026 PDF — Ashland PDF won.
- Hamilton County OH: live Registered Septage Haulers PDF at cagis.hamilton-co.org (header “2026 …”; print stamp 9/27/2026); column wraps messy; Ashland cleaner dated PDF preferred.
- Richland County: page claims Registered Septage Haulers Updated 06/12/2026 but curl to richlandhealth.org failed (connection / empty).
- Montgomery County (phdmc.org): SiteGround captcha blocked plain curl.
- Wayne County: still only 2025 PDF (too old).
- Fairfield / Medina / Lorain / Miami: no public 2026 PDF (same as prior night).
- Stark: Cloudflare + known 2021 PDF too old.
- Greene: no dated 2026 PDF URL resolved.
- Franklin: only 2025 Service Providers PDF found.
- Allen: only 2025 Haulers PDF found.

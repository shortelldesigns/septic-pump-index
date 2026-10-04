# Nightly Septic Pump Index — 3 October 2026 (PT)

## Shipped
- **Page:** Adams County, Ohio — registered septage haulers
- **Live URL:** https://shortelldesigns.github.io/septic-pump-index/oh/adams.html
- **Firm count:** 10 named haulers (business, operator, address, phone; local REG # and ODH bond unknown)
- **Commit:** `9080825b355ea333783f9c478e09a6e1829875e6` — *Add Adams County OH registered septage haulers.*
- **Screenshot:** parent will capture after live confirmation
- **Live HTTP 200:** pending Pages deploy verification after push

## Official source
- **PDF:** https://www.adamscountyhealth.org/_files/ugd/4712a5_9ee0771923a34aae9b591c70da6841f6.pdf  
  (title **Septage Haulers**; HDIS; footer **03/16/2026**; **10 TOTAL**; CreationDate 16 March 2026 UTC; Adams County Health Department, 560 RICE DRIVE WEST UNION OH)
- **Parent (Septic Program):** https://www.adamscountyhealth.org/septic-program  
  (link text **Septage Hauler List**)
- **Archive:** `data/sources/adams-oh-2026-septage-haulers.pdf` (+ `.txt` via `pdftotext -layout`)
- **Document date:** 16 March 2026 (PDF footer 03/16/2026); retrieved 3 October 2026 (US/Pacific)
- **Fetch note:** Living official URL confirmed via parent Septic Program page HTML (`a href` to `4712a5_9ee0771923a34aae9b591c70da6841f6.pdf` as **Septage Hauler List**). Same parent also links separate Installer List and Service Provider List PDFs — those were not merged into the hauler table.

## Caveats
PDF prints **business, operator, address, and phone** (no local REG #). Local REG # and **ODH bond marked unknown**. Spellings kept as printed (`LITTLE'S SEPTIC SERVICE , INC` with space before comma; `R&A (PERTUSET) SEPTIC SOLUTIONS`; operator `RELIABLE ONSITE SERVCIES` misspelling; `LAUR FURLONG`). Pumping is not an inspection. Separate installer / service-provider lists on the parent page were not used.

## Candidates skipped tonight
- **Adams Installer List / Service Provider List PDFs:** separate credential categories — hauler list only shipped.
- **Brown County OH 2026 Registered Septic Haulers** and **Stark County OH 2026 HAULER LIST:** not needed — Adams PDF downloaded and transcribed successfully.
- Already-shipped OH counties (ashland, butler, clark, columbiana, coshocton, cuyahoga, darke, delaware, erie, geauga, lake, licking, marion, morgan, muskingum, portage, seneca, summit) — not duplicated.

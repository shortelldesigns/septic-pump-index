# Sources fetched for Septic Pump Index v1

Retrieve date: **29 August 2026** (US/Pacific; fetch ran 30 August 2026 UTC).

## Succeeded — used on PA / OH / WI listing pages

| Source | URL | Document / page date | Notes |
| --- | --- | --- | --- |
| York County Solid Waste Authority licensed septage haulers, posted by Windsor Township | https://windsortwp.com/wp-content/uploads/2026-Septage-Haulers.pdf | As of February 2026 | curl + pdftotext -layout. 43 haulers. Archived `data/sources/york-pa-2026-septage-haulers.pdf`. DEP transporter numbers not printed. |
| Bucks County Health Department approved sewage haulers | https://www.buckscounty.gov/DocumentCenter/View/16662/Approved-Sewage-Hauler-List-2024-2025 | Revised 7/07/2025 | Retrieved 3 September 2026 (US/Pacific). curl + pdftotext. 42 named firms. DEP transporter numbers not printed. Three Waste Management rows lack phone. Pennsburg ZIP printed as 1807. Archived `data/sources/bucks-pa-approved-sewage-haulers-2025-07-07.pdf`. Parent: https://www.buckscounty.gov/1122/Sewage-Hauler-Vehicles. |
| Chester County Health Department licensed liquid waste pumpers | https://www.chesco.org/DocumentCenter/View/75806/Liquid-Waste-Pumpers | Date last revised 7-28-26 | Retrieved 7 September 2026 (US/Pacific). curl + pdftotext -layout. 58 licensed pumpers. DEP transporter numbers not printed. Odd spellings (Plumsteaville; Ink`s) kept as printed. Archived `data/sources/chester-pa-liquid-waste-pumpers.pdf`. Parent: https://www.chesco.org/983/Sewage-and-Water-Contractors. |
| Geauga Public Health registered septic pumpers | https://gphohio.org/wp-content/uploads/sites/17/2026/07/Geauga-County-Registered-Pumpers-2026_722026.pdf | Updated 2 July 2026 | curl + pdftotext -layout. 30 pumpers. Archived `data/sources/geauga-oh-registered-pumpers-2026-07-02.pdf`. Contact person not on this list. |
| Lake County General Health District septage haulers | https://www.lcghd.org/wp-content/uploads/2026/03/HAULER-030326.pdf | Footer date 03/03/2026 | curl + pdftotext -layout. 26 named haulers (PDF footer prints 27 TOTAL; empty comma-only slot on page 1 omitted). Phone missing on PORTA BANDIT LLC. Archived `data/sources/lake-oh-hauler-2026-03-03.pdf`. Parent: https://www.lcghd.org/om-program-septic/. |
| Portage County Combined General Health District registered septage haulers | https://portagehealth.net/wp-content/uploads/2026/07/2026-REGISTERED-SEPTAGE-HAULERS-07.17.26.pdf | Footer date 17 July 2026 | Retrieved 4 September 2026 (US/Pacific). curl + pdftotext -layout. 43 named haulers (PDF prints 43 TOTAL). Two business names truncated on PDF kept as printed. Archived `data/sources/portage-oh-registered-septage-haulers-2026-07-17.pdf`. Parent: https://portagehealth.net/our-programs/environmental-public-health/waste-water/contactors-designers-soil-scientists/. |
| Columbiana County General Health District registered STS pumpers | https://www.columbiana-health.org/wp-content/uploads/2026-STS-Pumpers.pdf | PDF CreationDate 22 April 2026 | Retrieved 10 September 2026 (US/Pacific). curl + pdftotext -layout. 22 STS pumpers alphabetical by city. Spellings kept as printed (Willam Milner; Charlie Hoffman Septic Svcs.; N. Benton; Yo-town Kingsville). ODH bond unknown. Archived `data/sources/columbiana-oh-2026-sts-pumpers.pdf`. Parent: https://www.columbiana-health.org/sewage/. |
| Coshocton Public Health District registered contractors (haulers) | https://www.coshoctoncounty.net/health/wp-content/uploads/sites/16/2026/05/Septic-Haulers-Installers-Service-Providers-2026.pdf | PDF CreationDate 29 May 2026 | Retrieved 11 September 2026 (US/Pacific). curl + pdftotext -layout. Full PDF lists installers/haulers/service providers; page tabulates 17 Hauler-role firms only. Spellings kept as printed (Wondiland; Will M. & Patrick F.). ODH bond unknown. Archived `data/sources/coshocton-oh-2026-registered-contractors.pdf`. Parent: https://www.coshoctoncounty.net/health/private-sewage/. |
| Delaware Public Health District septage haulers | https://www.delawarehealth.org/wp-content/uploads/2026/07/HAULERS-JULY-2026.pdf | Footer date 21 July 2026 | Retrieved 12 September 2026 (US/Pacific). curl + pdftotext -layout. 36 haulers (PDF prints 36 TOTAL). Spellings kept as printed (CHUCKS…IN; UBERDROSS…REDBOX &; MASRYSVILLE; JEREMY HEAVEN). BLOODHOUND phone dashes → unknown. ODH bond unknown. Archived `data/sources/delaware-oh-2026-septage-haulers-07-21.pdf`. Parent: https://www.delawarehealth.org/sewage/. |
| Licking County Health Department septage haulers | https://lickingcohealth.org/wp-content/uploads/2026/02/sewage-treatment-haulers-02-12-2026.pdf | Footer 02/12/2026; CreationDate 12 February 2026 UTC | Retrieved 14 September 2026 (US/Pacific). curl + pdftotext -layout. 34 TOTAL named haulers. Spellings kept as printed (BANK SANITATION,LLC; truncated ERICSON ENVIRONMENTAL SERVI). TWO-TAC LLC phone unknown; OHIO CAST STONE phone printed as -614-444-2778. No reg numbers on PDF. ODH bond unknown. Archived `data/sources/licking-oh-2026-septage-haulers-02-12.pdf`. Parent: https://lickingcohealth.org/sewage/. |
| Marion Public Health registered septage haulers | https://marionpublichealth.org/wp-content/uploads/2026/06/Marion-County-Registered-Septage-Haulers-2026.06.16.pdf | Footer Updated: 6/16/2026 | Retrieved 13 September 2026 (US/Pacific). curl + pdftotext -layout. 17 named haulers. Spellings kept as printed (Underbross; Hanes Environmental Inc. as installer name). Business phone only (cells/emails omitted). ODH bond unknown. Archived `data/sources/marion-oh-2026-registered-haulers-06-16.pdf`. Parent: https://marionpublichealth.org/household-sewage-treatment-systems/. |
| Shawano County Planning and Development licensed pumpers / POWTS maintainers | https://www.co.shawano.wi.us/i_shawano/d/Planning_and_Development/licensed_pumpers.pdf | Updated 19 May 2026 | curl + pdftotext -layout. 17 pumpers + 4 POWTS maintainers (No Pumping). Archived `data/sources/shawano-wi-licensed-pumpers.pdf`. DNR license numbers not printed. |

## Succeeded — additional official rosters also shipped in v1

| Source | URL | Document / page date | Notes |
| --- | --- | --- | --- |
| Montana DEQ 2026 licensed septic pumpers | https://deq.mt.gov/files/Land/SolidWaste/Documents/pumpers/2026%20licensed%20pumpers.pdf | As of 20 May 2026 | 152 unique license numbers. Phone not on PDF. Archived `data/sources/mt-2026-licensed-pumpers.pdf`. |
| ND DEQ 2026 Annual Active ND Sanitary Pumper List | https://deq.nd.gov/publications/WQ/2_NDPDES/SepticPumper/rptBusnList.pdf | Licensed on or before 23 July 2026 | 125 Class I/II pumpers. Archived `data/sources/nd-2026-class-i-ii.pdf`. |
| Iowa DNR Licensed Septic Tank Cleaners (Pumpers) | https://www.iowadnr.gov/media/8587/download?inline= | PDF metadata 19 August 2026 | 223 license rows (220 unique license numbers; three numbers appear twice on the PDF for different firms). Archived `data/sources/ia-dnr-licensed-septic-tank-cleaners-2026-08-19.pdf`. Program: https://www.iowadnr.gov/environmental-protection/water-quality/private-sewage-disposal-and-septage/septic-tank-cleaning |
| Clallam County WA licensed septic pumpers | https://clallamcountywa.gov/DocumentCenter/View/4655/Septic-Tank-Pumpers-PDF | Printed 17 April 2026 | 10 pumpers. Archived `data/sources/clallam-septic-tank-pumpers.pdf`. |
| Clallam County WA septic maintenance providers | https://clallamcountywa.gov/DocumentCenter/View/4653/Septic-Maintenance-Providers-PDF | Printed 3 June 2026 | O&M inspectors (pumping is not an inspection). Archived `data/sources/clallam-septic-maintenance-providers.pdf`. |
| Benton County MN licensed SSTS designers/inspectors/installers/maintainers/service providers | https://www.bentoncountymn.gov/DocumentCenter/View/238 | PDF dated 5/6/2026 (CreationDate Wed May 6, 2026) | Retrieved 1 September 2026 (US/Pacific). 10 unique Maintainers (Pumpers) only — Designer/Installer/Inspector/Service Provider columns excluded. Parent: https://www.bentoncountymn.gov/228/Subsurface-Sewage-Treatment-Systems. Archived `data/sources/benton-mn-licensed-ssts-2026-05-06.pdf`. |
| McLean County Health Department licensed septic system pumpers | https://www.mcleancountyil.gov/DocumentCenter/View/23368/0601-30-Pumper-list-2026 | Revised 12 May 2026 | Retrieved 5 September 2026 (US/Pacific). curl + pdftotext -layout. 17 licensed individuals (16 for hire; Higgs, William R printed NOT FOR HIRE). Emails/fax not tabulated. Archived `data/sources/mclean-il-pumper-list-2026.pdf`. Parent: https://health.mcleancountyil.gov/1733/Septic-Systems-Contractor-Information. |
| Johnson County Department of Health and Environment licensed sanitary disposal contractors (sewage) | https://www.jocogov.org/sites/default/files/files/2026-08/2026%20Licensed%20Sanitary%20Disposal%20Contractors%20Lists.pdf | Footer updated 24 June 2026 | Retrieved 6 September 2026 (US/Pacific). curl + pdftotext -layout. 25 sewage contractors (grease-only and portable-toilet-only sections omitted). Addresses not on PDF. Archived `data/sources/johnson-ks-licensed-sanitary-disposal-contractors-2026.pdf`. Parent: https://www.jocogov.org/department/environment/septic-systems/pumper-installer-lists. |

## Succeeded — used on how-to pages (not as contractor lists)

| Source | URL | Document / page date | Notes |
| --- | --- | --- | --- |
| EPA How to Care for Your Septic System | https://www.epa.gov/septic/how-care-your-septic-system | Last updated 17 August 2026 | WebFetch. Inspect at least every 3 years; typical pump-out every 3–5 years; sludge/scum cutoffs. |
| EPA Frequent Questions on Septic Systems | https://www.epa.gov/septic/frequent-questions-septic-systems | Last updated 11 March 2026 | WebFetch. Inspect 1–3 years / pump 3–5 years; failure signs; inspection checklist. |
| EPA Resolving Septic System Malfunctions | https://www.epa.gov/septic/resolving-septic-system-malfunctions | Last updated 11 March 2026 | WebFetch. Failure causes; sewage-in-house cleanup. |
| EPA New Homebuyer’s Brochure and Guide | https://www.epa.gov/septic/new-homebuyers-brochure-and-guide-septic-systems | Page last updated 24 February 2026 | WebFetch of HTML index. |
| EPA New Homebuyer’s Guide PDF | https://www.epa.gov/sites/default/files/2017-08/documents/170803-homebuyerssepticguidebrochurelayout_508c.pdf | EPA-832-F-17-010, August 2017 | curl. Inspection checklist. Dollar estimates **not** copied. Archived `data/sources/epa-homebuyer-guide-2017.pdf`. |
| Penn State Extension, Septic Tank Pumping | https://extension.psu.edu/septic-tank-pumping | Updated 21 July 2023 | WebFetch. 2–3 year interval; sludge one-third of depth; additives not a substitute. |
| Penn State Extension, Septic System Basics | https://extension.psu.edu/septic-system-basics | Updated 16 September 2024 | WebFetch. 3–5 years or one-third solids; local rules often every 3 years. |
| Penn State Extension, Five Basic Practices | https://extension.psu.edu/five-basic-practices-to-protect-your-septic-system | Updated 16 October 2024 | WebFetch. Many PA communities require a schedule. |
| PA DEP, Register a Residential Septage Hauler | https://www.pa.gov/services/dep/water/clean-water/register-a-residential-septage-hauler | Retrieved 29 August 2026 | Statewide registration; 5-digit transporter number; links XLSX (see Failures). |
| Ohio Department of Health, Information for Contractors | https://odh.ohio.gov/know-our-programs/sewage-treatment-systems/INFORMATION-FOR-CONTRACTORS | Retrieved 29 August 2026 | Separate installer / service provider / septage hauler; $25,000 hauler bond. |
| Wisconsin DNR, Septage business license requirements | https://dnr.wisconsin.gov/topic/opcert/septageBusiness.html | Retrieved 29 August 2026 | NR 113 licensing; ELC database lookup. |
| Michigan EGLE Septage program | https://www.michigan.gov/egle/about/organization/drinking-water-and-environmental-health/septage | Retrieved 29 August 2026 | Part 117. No static roster transcribed. |

## Fetched but not used as a current roster

| Source | URL | Document date | Why not tabulated |
| --- | --- | --- | --- |
| Wisconsin DNR SeptageBusinessList.pdf | https://dnr.wisconsin.gov/sites/default/files/topic/OpCert/SeptageBusinessList.pdf | Report run on 30 June 2023 | Too old to present as a 2026 roster. DNR page says to use the ELC lookup / email for current lists. |

## Failed or incomplete

| Attempt | URL | What happened | What we did instead |
| --- | --- | --- | --- |
| PA DEP Active Residential Septage Haulers XLSX | https://files.dep.state.pa.us/Water/Biosolids/BiosolidsPortalFiles/Active_Septic_Hauler_Registration-April_2024.xlsx | curl TLS error `unexpected eof while reading` | Linked the registration page. Used the February 2026 York County list. |
| Michigan EGLE hauler-directory path | https://www.michigan.gov/egle/about/organization/drinking-water-and-environmental-health/septage/hauler-directory | HTTP 302 then 404 | Linked the parent Septage program page. No Michigan names. |
| Ohio Department of Health live bonded-hauler list | Linked from ODH contractor page | No dated static table retrieved | Linked ODH contractor page. Geauga bond field unknown. |

## Not used as listing sources

- Third-party contractor marketplaces.
- Company marketing sites used to fill missing phones.

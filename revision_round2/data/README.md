# Data files

All files in `processed/` are analysis-ready and UTF-8 encoded. Original source
documents are in `raw/`.

## `tunisia_physician_workforce.csv`

Annual stock of physicians in active practice, 2010–2024.

| Column | Description |
|---|---|
| `year` | Calendar year |
| `physicians_total` | Physicians in practice (public + private) |
| `public_sector` | Public-sector physicians |
| `private_sector` | Private practitioners |
| `definition` | Definition used |
| `source` | Source |
| `notes` | Data-quality notes |

The 2010 value is used only as an initial-condition anchor. The 2020 public
count contains an administrative discontinuity.

## `tunisia_registration_and_flows.csv`

Long-format table of registration counts, new registrations, emigration
proxies and destination-country stocks.

| Column | Description |
|---|---|
| `year` | Year or period |
| `indicator` | Indicator name |
| `value` | Value |
| `unit` | Unit |
| `definition` | Definition |
| `source` | Source |
| `status` | Observed, proxy, media-reported or indirect estimate |

## `population_tunisia.csv`

Population denominators, 2010–2040.

- 2024: INS census (RGPH 2024), 11,972,169.
- Other years: UN World Population Prospects 2024, rescaled to the 2024 census
  (factor 0.97516).

## Rebuilding the data

The processed CSVs were assembled by hand from the sources listed in each file.
The raw PDFs used for verification are in `raw/`. No scraping is required to
reproduce the analysis.

## Notes on definitions

- **Registered** physicians are those inscribed with the CNOM. This is not an
  active-practice count.
- **Practising** physicians are those recorded in the public payroll and the
  private-sector health map. This is the count modelled.
- **Emigration** is not directly observed. The CSV reports proxies, not a flow
  series.
- **Destination stocks** (France, Germany, OECD) are lower bounds because they
  exclude unregistered migrants and non-OECD destinations.

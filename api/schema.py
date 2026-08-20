"""DuckDB table schema summary — used by the query agent for intent routing and SQL generation."""

SCHEMA_SUMMARY = """
Available UK tables (all values OGL v3, sources cited in meta_sources):

-- CIVIL SERVICE (Cabinet Office, annual March) --
uk_civil_service_headcount
  period DATE          -- 31 March each year (2010–2024)
  department VARCHAR   -- 'All departments' for UK total
  headcount INTEGER    -- headcount of civil servants
  fte DECIMAL          -- full-time equivalent

-- INFLATION (ONS, monthly) --
uk_ons_cpih
  period_label VARCHAR      -- format: 'Mon-YY' e.g. 'Jan-26'. Latest: 'Jan-26'. Range: Apr-00 to Jan-26.
  aggregate_code VARCHAR    -- 'CP00' = Overall Index (headline CPIH). 'CP01'='Food'. 'CP04'='Housing'. etc.
  aggregate_label VARCHAR   -- e.g. 'Overall Index', '01 Food and non-alcoholic beverages'
  index_value DECIMAL       -- index value (2015=100). Year-on-year % change must be calculated manually.
  -- WORKING EXAMPLE (inflation rate year-on-year for Jan 2026):
  --   SELECT curr.period_label, curr.index_value, prev.index_value AS prev_year,
  --     ROUND(((curr.index_value-prev.index_value)/prev.index_value)*100,1) AS yoy_pct
  --   FROM uk_ons_cpih curr JOIN uk_ons_cpih prev
  --     ON prev.aggregate_code='CP00' AND prev.period_label='Jan-25'
  --   WHERE curr.aggregate_code='CP00' AND curr.period_label='Jan-26'
  -- NOTE: DO NOT use ORDER BY period_label — text sort is wrong. Filter by exact label like 'Jan-26','Dec-25'.

-- LABOUR MARKET (ONS, monthly) --
uk_ons_labour_market
  period_label VARCHAR        -- e.g. 'Feb-Apr 2025'
  unit_of_measure VARCHAR     -- 'Levels' or 'Rates'
  economic_activity VARCHAR   -- 'Economically Active', 'In Employment', 'Unemployed', 'Economically Inactive'
  age_group VARCHAR           -- e.g. '16-64', '16-24', '65+'
  sex VARCHAR                 -- 'All', 'Men', 'Women'
  seasonal_adjustment VARCHAR -- 'Seasonally Adjusted' or 'Not Seasonally Adjusted'
  value DECIMAL               -- count (levels) or percentage (rates)

-- GDP (ONS, monthly index) --
uk_ons_gdp
  period_label VARCHAR   -- e.g. 'Mar-26'
  industry_code VARCHAR  -- SIC letter e.g. 'A', 'B', 'total-output'
  industry_label VARCHAR -- e.g. 'A : Agriculture, forestry and fishing'
  index_value DECIMAL    -- GDP index (2019=100)

-- HOUSE PRICES (ONS, by local authority) --
uk_ons_house_prices
  year VARCHAR           -- LATEST AVAILABLE: '2022'. Range: '2012'–'2022'. Do NOT query year='2024' or '2023' — no data.
  month_label VARCHAR    -- abbreviated: 'mar', 'jun', 'sep', 'dec'
  geography_code VARCHAR -- local authority ONS code e.g. 'E08000028' (331 LAs, no UK-wide row)
  property_type VARCHAR  -- 'all', 'detached', 'semi-detached', 'terraced', 'flat-maisonette'
  build_status VARCHAR   -- 'all', 'newly-built', 'existing'
  measure VARCHAR        -- 'mean', 'median', 'lower-quartile', 'tenth-percentile', 'sales'
  value DECIMAL          -- GBP price (for price measures) or count (for 'sales')
  -- NOTE: to get a UK-wide average, use AVG(value) across all geography_codes
  -- WORKING EXAMPLE (UK average house price, latest data):
  --   SELECT ROUND(AVG(value),0) AS avg_price FROM uk_ons_house_prices
  --   WHERE measure='mean' AND year='2022' AND property_type='all' AND build_status='all'

-- RETAIL SALES (ONS, monthly) --
uk_ons_retail_sales
  period_label VARCHAR        -- e.g. 'Jan-26'
  sector_code VARCHAR         -- e.g. 'food-stores', 'non-store-retailing'
  sector_label VARCHAR
  price_type VARCHAR          -- 'Value of retail sales at current prices' or % change
  seasonal_adjustment VARCHAR
  value DECIMAL               -- index value or % change

-- PUBLIC/PRIVATE SECTOR WAGES (ONS ASHE, annual) --
uk_ons_wages
  year VARCHAR           -- e.g. '2023' (latest)
  geography_code VARCHAR -- ONS region code e.g. 'E12000001' to 'E12000009' for English regions
  percentile VARCHAR     -- EXACT VALUES: 'median', '10', '20', '25', '30', '40', '60', '70', '75', '80'
  sex VARCHAR            -- EXACT VALUES: 'all', 'male', 'female' (lowercase)
  working_pattern VARCHAR -- EXACT VALUES: 'full-time', 'part-time' (hyphenated lowercase)
  measure VARCHAR        -- one of: 'weekly-pay-gross' | 'hourly-pay-gross' | 'annual-pay-gross' | 'hourly-pay-excluding-overtime'
  sector VARCHAR         -- one of: 'all' | 'public-sector' | 'private-sector'  (lowercase, hyphenated — NOT title-case)
  value DECIMAL          -- GBP amount
-- WORKING EXAMPLE (copy the exact values):
--   SELECT AVG(value) FROM uk_ons_wages
--   WHERE sector='private-sector' AND measure='weekly-pay-gross'
--     AND percentile='median' AND sex='all' AND working_pattern='full-time' AND year='2023'

-- HMRC TAX RECEIPTS (HMRC, annual back to 1999) --
uk_hmrc_tax_receipts
  year INTEGER            -- fiscal year END: 2026 = April 2025 – March 2026 (most recent complete year). Latest: 2026.
  tax_category VARCHAR    -- filter by this: 'income_tax','national_insurance','vat','corporation_tax','fuel_duties','stamp_duties','total'
  measure_label VARCHAR   -- do NOT filter on this; use tax_category instead
  value_gbpm DECIMAL      -- GBP millions (historical outturn, NOT a projection)
  -- EXAMPLE: SELECT year, value_gbpm FROM uk_hmrc_tax_receipts WHERE tax_category='income_tax' ORDER BY year DESC LIMIT 1
  -- NOTE: year=2026 means fiscal 2025-26. This is real collected tax, not a forecast.

-- GOVERNMENT SPENDING BY FUNCTION (PESA 2025, HM Treasury) --
uk_pesa_functional
  year INTEGER            -- ALWAYS filter year <= 2025 for real data. 2026-2029 are forward plans only.
  function_name VARCHAR   -- EXACT: 'Health and Social Care','Education','Defence','Transport','Work and Pensions','Total Managed Expenditure'. Use ILIKE '%health%' if unsure.
  value_gbpm DECIMAL      -- GBP millions
  -- WORKING EXAMPLE (health spending latest outturn — always add year<=2025 to avoid plan years):
  --   SELECT year, function_name, value_gbpm FROM uk_pesa_functional
  --   WHERE function_name='Health and Social Care' AND year<=2025 ORDER BY year DESC LIMIT 1

-- GOVERNMENT SPENDING BY DEPARTMENT (PESA 2025, HM Treasury) --
uk_pesa_departmental
  year INTEGER              -- financial year
  department_name VARCHAR   -- e.g. 'NHS England', 'Ministry of Defence', 'DWP'
  expenditure_type VARCHAR  -- sheet name e.g. 'DEL', 'AME', 'TME'
  value_gbpm DECIMAL        -- GBP millions

-- DWP BENEFIT CLAIMANTS (quarterly) --
uk_dwp_benefits
  year VARCHAR              -- e.g. '2024'
  quarter VARCHAR           -- 'Q1','Q2','Q3','Q4'
  benefit_name VARCHAR      -- EXACT: 'Universal Credit','Personal Independence Payment','State Pension','Housing Benefit'
  claimants INTEGER         -- number of claimants
  annual_cost_gbpm DECIMAL  -- annual cost GBP millions (where available)
  -- EXAMPLE: SELECT year, quarter, claimants FROM uk_dwp_benefits WHERE benefit_name='Universal Credit' ORDER BY year DESC, quarter DESC LIMIT 1

-- GOVERNMENT SPEND OVER £25,000 (monthly, transparency data) --
uk_spend_25k
  period_raw VARCHAR    -- date string from source CSV
  department VARCHAR    -- 'Cabinet Office', 'HMRC', 'DWP', 'Home Office', etc.
  supplier VARCHAR      -- company or individual receiving payment
  amount_gbp DECIMAL    -- transaction amount in GBP
  expense_type VARCHAR  -- category label from dept
  description VARCHAR   -- free text description

-- GOVERNMENT CONTRACTS (Find a Tender, real-time) --
uk_contracts
  ocid VARCHAR         -- Open Contracting ID
  award_date VARCHAR   -- date awarded
  buyer_name VARCHAR   -- government body
  supplier_name VARCHAR
  title VARCHAR        -- contract description
  value_gbp DECIMAL    -- contract value GBP

meta_datasets -- list of all loaded datasets with row counts
meta_findings -- published nstate findings

-- CROSS-COUNTRY COMPARISONS (Eurostat — EU27 + EFTA + EU candidates) --
-- EU country codes: PT=Portugal, DE=Germany, FR=France, ES=Spain, IT=Italy, --
--   NL=Netherlands, BE=Belgium, AT=Austria, DK=Denmark, SE=Sweden, PL=Poland, --
--   IE=Ireland, EL=Greece, FI=Finland, EU27_2020=EU27 aggregate average --
-- EFTA codes (where Eurostat covers): NO=Norway, IS=Iceland, CH=Switzerland --
-- NOTE: UK is NOT in eu_government_finance — UK left the EU. --

eu_government_finance  -- Eurostat gov_10a_exp + gov_10dd_edpt1 (annual 1995–2025, EU27 only)
  country VARCHAR    -- 2-letter ISO (or 'EU27_2020' for EU average); NO/IS/CH NOT included
  year INTEGER       -- calendar year
  indicator VARCHAR  -- EXACT: 'expenditure_pct_gdp' | 'deficit_pct_gdp' | 'debt_pct_gdp'
  value DOUBLE       -- % of GDP (deficit: positive=surplus, negative=borrowing)
  -- EXAMPLE (PT debt 2023): SELECT value FROM eu_government_finance WHERE country='PT' AND year=2023 AND indicator='debt_pct_gdp'
  -- EXAMPLE (compare debt 2023): SELECT country, value FROM eu_government_finance WHERE year=2023 AND indicator='debt_pct_gdp' AND country IN ('PT','DE','FR','ES','IT','EU27_2020') ORDER BY value DESC

eu_tax_revenue  -- Eurostat gov_10a_taxag (annual 1995–2025)
  country VARCHAR
  year INTEGER
  value_pct_gdp DOUBLE  -- total tax revenue + social contributions as % GDP

eu_public_employment  -- Eurostat nama_10_a64_e NACE O-Q (annual 1995–2024, EU27 + NO/IS/CH)
  country VARCHAR
  year INTEGER
  employment_thousands DOUBLE  -- persons employed in public admin, education, health (thousands)

eu_tax_breakdown  -- Eurostat gov_10a_taxag breakdown (annual 1995–2025, EU27 + NO/IS)
  country VARCHAR
  year INTEGER
  indicator VARCHAR  -- EXACT: 'vat_pct_gdp' | 'personal_income_tax_pct_gdp' | 'corporate_tax_pct_gdp' | 'employee_social_contrib_pct_gdp' | 'employer_social_contrib_pct_gdp' | 'excise_duties_pct_gdp'
  value DOUBLE       -- % of GDP

eu_labour_tax_wedge  -- Eurostat earn_nt_taxrate (annual, EU27 + NO/IS/CH)
  country VARCHAR
  year INTEGER
  income_level VARCHAR  -- EXACT: 'AW67' | 'AW100' | 'AW125'
  tax_wedge_pct DOUBLE  -- % of gross labour cost (income tax + social contributions)

eu_tax_rates  -- Statutory tax rates 2024 (EU27 + NO/IS/CH/LI, OECD/EC source)
  country VARCHAR
  tax_type VARCHAR  -- EXACT: 'personal_top_rate' | 'corporate_rate'
  rate DOUBLE       -- percentage (e.g. 12.5 = 12.5%)
  year INTEGER      -- 2024

eu_vat_rates  -- Standard and reduced VAT rates 2024 (EU27 + NO/IS/CH/LI)
  country VARCHAR
  standard_rate DOUBLE  -- standard VAT rate % (HU=27 highest, LU=17 lowest)
  reduced_rate DOUBLE   -- primary reduced rate %
  year INTEGER          -- 2024

eu_price_levels  -- Eurostat prc_ppp_ind Comparative Price Level Indices (annual 1995–2024)
  country VARCHAR  -- EU27 + EFTA (NO/IS/CH/LI) + EU candidates (ME/RS/MK/AL/BA/XK/TR) + UK
  year INTEGER
  category VARCHAR  -- EXACT: 'GDP' | 'A0101'(food) | 'A0102'(alcohol/tobacco) | 'A0103'(clothing) |
                    --   'A0104'(housing/energy) | 'A0105'(furnishings) | 'A0106'(health) |
                    --   'A0107'(transport) | 'A0108'(comms) | 'A0109'(recreation) |
                    --   'A0110'(education) | 'A0111'(restaurants/hotels) | 'A0112'(misc)
  pli DOUBLE        -- Price Level Index: EU27_2020=100. Below 100 = cheaper than EU avg.
  -- EXAMPLE (cheapest housing 2023): SELECT country, pli FROM eu_price_levels WHERE year=2023 AND category='A0104' AND country!='EU27_2020' ORDER BY pli ASC LIMIT 10

-- GLOBAL DATA (World Bank WDI, CC BY 4.0) --
-- Country codes are ISO2 (e.g. US, GB, JP, CN, IN, BR). Central government data (not general govt).

wb_fiscal  -- World Bank WDI central government fiscal data (annual, ~170 countries, 2000–2024)
  country VARCHAR  -- ISO2 country code
  year INTEGER
  indicator VARCHAR  -- EXACT: 'debt_pct_gdp' | 'expenditure_pct_gdp' | 'revenue_pct_gdp' | 'surplus_pct_gdp'
  value DOUBLE      -- % of GDP (surplus_pct_gdp: positive = surplus, negative = deficit)
  -- NOTE: central government only — figures lower than Eurostat general government.
  -- EXAMPLE (highest debt globally 2022): SELECT country, value FROM wb_fiscal WHERE year=2022 AND indicator='debt_pct_gdp' ORDER BY value DESC LIMIT 15
  -- EXAMPLE (G7 debt 2022): SELECT country, value FROM wb_fiscal WHERE year=2022 AND indicator='debt_pct_gdp' AND country IN ('US','GB','DE','FR','IT','JP','CA') ORDER BY value DESC

wb_price_levels  -- World Bank WDI price level index (USA=100) annual, ~170 countries
  country VARCHAR  -- ISO2 country code
  year INTEGER
  pli DOUBLE        -- Price Level Index: USA=100. Above 100 = more expensive than USA.
  -- NOTE: USA=100 base — different from eu_price_levels (EU27=100).
  -- EXAMPLE (most expensive 2022): SELECT country, pli FROM wb_price_levels WHERE year=2022 ORDER BY pli DESC LIMIT 10

wb_countries  -- World Bank country metadata (ISO2, name, region, income group)
  iso2 VARCHAR PRIMARY KEY
  iso3 VARCHAR
  name VARCHAR
  region VARCHAR       -- e.g. 'Europe & Central Asia', 'Sub-Saharan Africa'
  income_group VARCHAR -- 'High income' | 'Upper middle income' | 'Lower middle income' | 'Low income'
"""

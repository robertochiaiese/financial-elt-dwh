# Data Catalog

---

## core.dim_dates

### Overview
A conformed and enriched calendar dimension providing granular date attributes, analytical labels, fiscal information, and integer-based flags.

### Primary Key
- **date_id** (INTEGER)

---

### Columns

#### Identifiers
| Column | Type | Description |
|--------|------|-------------|
| date_id | INTEGER | Unique key for each date. |
| date | DATE | Actual date (YYYY-MM-DD). |

#### Calendar Attributes
| Column | Type | Description |
|--------|------|-------------|
| calendar_year | INTEGER | Year number. |
| calendar_month | INTEGER | Month (1–12). |
| calendar_day | INTEGER | Day of month. |
| calendar_week | INTEGER | ISO week number. |
| calendar_week_start_date_id | INTEGER | Start-of-week date key. |
| calendar_week_end_date_id | INTEGER | End-of-week date key. |
| calendar_day_in_week | INTEGER | Day index in week (1–7). |
| calendar_day_in_month | INTEGER | Day index in month. |
| calendar_number_of_days_in_month | INTEGER | Total days in month. |
| calendar_number_of_days_in_quarter | INTEGER | Total days in quarter. |

#### Derived Metrics
| Column | Type | Description |
|--------|------|-------------|
| day_of_year | INTEGER | Day number in the year (1–365/366). |
| quarter_of_year | INTEGER | Quarter number (1–4). |

#### Labels
| Column | Type | Description |
|--------|------|-------------|
| year_month | STRING | Year–month label (YYYY-MM). |
| year_quarter | STRING | Year–quarter label (YYYYQ#). |
| day_long_name | STRING | Full weekday name. |
| month_long_name | STRING | Full month name. |

#### Flags (INTEGER: 1 = TRUE, 0 = FALSE)
| Column | Type | Description |
|--------|------|-------------|
| is_weekend | INTEGER | Weekend flag. |
| is_month_start | INTEGER | First day of month flag. |
| is_month_end | INTEGER | Last day of month flag. |

#### Fiscal Attributes
| Column | Type | Description |
|--------|------|-------------|
| fiscal_week | INTEGER | Fiscal week number. |
| fiscal_month | INTEGER | Fiscal month. |
| fiscal_year | INTEGER | Fiscal year. |

---

## core.fact_daily_prices

### Overview
A daily fact table with price metrics, volatility indicators, and rolling technical analytics.

### Primary Key
- **prices_id** (INTEGER)

---

### Columns

#### Keys
| Column | Type | Description |
|--------|------|-------------|
| prices_id | INTEGER | Surrogate key generated via ROW_NUMBER(). |
| date_id | INTEGER | Foreign key to core.dim_dates. |

#### Price Metrics
| Column | Type | Description |
|--------|------|-------------|
| open_price | DECIMAL | Opening price of the day. |
| high_price | DECIMAL | Intraday maximum price. |
| low_price | DECIMAL | Intraday minimum price. |
| close_price | DECIMAL | Closing price of the day. |
| trading_volume | BIGINT | Trading volume for the day. |

#### Derived Price Metrics
| Column | Type | Description |
|--------|------|-------------|
| daily_price_change_pct | DECIMAL | Percentage change: (close - open) / open * 100. |
| price_range | DECIMAL | Intraday range: high - low. |
| price_range_pct | DECIMAL | Percentage range relative to open. |

#### Technical Indicators
| Column | Type | Description |
|--------|------|-------------|
| sma_7days | DECIMAL | 7-day simple moving average of closing price. |
| volume_ratio | DECIMAL | Volume / 20-day average volume. |

#### Adjustment Metrics
| Column | Type | Description |
|--------|------|-------------|
| adjustment_difference | DECIMAL | Currently always 0 (placeholder for adjustments). |

#### Price Trend
| Column | Type | Description |
|--------|------|-------------|
| price_trend | STRING | Trend label: bullish, bearish, neutral. |

---


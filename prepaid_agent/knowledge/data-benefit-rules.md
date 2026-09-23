---
category: plan_rule
plan_type: ALL
version: "1"
status: active
---
# Data Benefit Rules

## Data Type Field

The data_type field specifies how data allowance is delivered in a plan. Two data_type values are allowed: PER_DAY (daily allowance that renews each day) and TOTAL (single allowance for the entire validity period). DATA, COMBO, and UNLIMITED plan types include data benefits. VOICE plans do not include data and must not have a data_type field.

## Data GB per Day (PER_DAY Type)

When data_type is set to PER_DAY, the data_gb field specifies the daily data allowance in gigabytes. PER_DAY data ranges from 0.5 GB to 5 GB per day. Valid values include 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, and 5 GB per day. This allowance resets every calendar day during the plan validity period.

## Data GB Total (TOTAL Type)

When data_type is set to TOTAL, the data_gb field specifies the total data allowance in gigabytes for the entire validity period. TOTAL data ranges from 1 GB to 300 GB for the entire plan duration. Valid values range continuously from 1 to 300 GB. This allowance does not reset; once consumed, no additional data is available until the plan validity expires.

## Data Required in DATA, COMBO, and UNLIMITED Plans

DATA plan type requires both data_type and data_gb fields; these are mandatory. COMBO plan type requires both data_type and data_gb fields; these are mandatory. UNLIMITED plan type requires a data_gb field (PER_DAY type only), specifying the daily FUP limit. VOICE plan type must not include data_type or data_gb fields.

## Validation of Data Benefits

When creating plans with data benefits, data_type must be either PER_DAY or TOTAL. If data_type is PER_DAY, data_gb must be between 0.5 and 5. If data_type is TOTAL, data_gb must be between 1 and 300. Plans lacking valid data specifications will be rejected.

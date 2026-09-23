---
category: plan_rule
plan_type: ALL
version: "1"
status: active
---
# Validity Rules

## Validity Days Range

Every prepaid plan (DATA, VOICE, COMBO, UNLIMITED) must have a validity_days field with a value between 1 and 365 days inclusive. Validity periods shorter than 1 day are not allowed. Validity periods longer than 365 days are not allowed. For example, 1 day, 28 days, 84 days, 180 days, and 365 days are all valid validity periods.

## Validity Requirements for All Plan Types

The validity_days parameter is a mandatory field for all plan types. No plan can be created without specifying a validity period. The validity period applies uniformly across DATA, VOICE, COMBO, and UNLIMITED plan types. Different plan types may use the same validity_days values; for example, 28-day validity is common across all plan types.

## Common Validity Periods in Market

While any value from 1-365 days is allowed, common validity periods in the Indian market are 1, 7, 14, 28, 30, 56, 60, 84, 90, 180, 365 days. Plans can be designed with any validity within the 1-365 range based on market demand and user preferences, not limited to these common periods.

## Validation of Validity Period

When creating a plan, the validity_days value is validated to ensure it falls within the 1-365 range. Invalid values such as 0 days, 366 days, 400 days, or negative numbers will be rejected. The validity_days field must be a positive integer within the specified range.

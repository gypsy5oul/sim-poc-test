---
category: plan_type_def
plan_type: COMBO
version: "1"
status: active
---
# Combo Plans

## What is a Combo Plan

A COMBO plan is a prepaid plan that provides both data and voice benefits in a single offering. COMBO plans are designed for users who need to use both data and calling as part of their regular usage. They combine data allowance with voice minutes into one recharging unit with a single validity period and price point.

## Required Fields for Combo Plans

A COMBO plan must include the following fields: plan_type (COMBO), validity_days (1-365), price (₹10-₹5000), data_type (PER_DAY or TOTAL), data_gb (depends on data_type), and voice (either "UNLIMITED" or minutes from 1-10000). The data_type determines whether the data allowance is per day or total for the validity period. Each COMBO plan requires a single plan_type, validity_days, and price to function.

## Optional Fields for Combo Plans

SMS benefits may be optionally included in COMBO plans via the sms_per_day field (0-100 SMS messages per day). If SMS is not needed, this field can be omitted. Other fields specific to only DATA or VOICE plan types must not be included in COMBO plans.

## Example Combo Plan

A typical COMBO plan in the Indian market: plan_type COMBO, validity_days 28, price ₹299, data_type PER_DAY, data_gb 2 GB per day, voice UNLIMITED, and sms_per_day 100. Another example: validity_days 84, price ₹599, data_type TOTAL, data_gb 12 GB total, voice 600 minutes, sms_per_day 50. Both follow COMBO plan requirements and serve different user segments.

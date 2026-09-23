---
category: plan_type_def
plan_type: DATA
version: "1"
status: active
---
# Data Plans

## What is a Data Plan

A DATA plan is a prepaid plan that provides mobile internet access as the primary benefit. DATA plans are designed for users who require data connectivity for web browsing, applications, and online services without calling requirements. DATA plans focus entirely on data allowance without voice calling.

## Required Fields for Data Plans

A DATA plan must include the following fields: plan_type (DATA), validity_days (1-365), price (₹10-₹5000), data_type (PER_DAY or TOTAL), and data_gb (depends on data_type). The data_type determines whether data allowance resets daily (PER_DAY) or is available as a total for the entire validity period (TOTAL). Each DATA plan requires a single plan_type, validity_days, and price.

## Optional Fields for Data Plans

SMS benefits may be optionally included in DATA plans via the sms_per_day field (0-100 SMS messages per day). If SMS is not needed, this field can be omitted. Voice calling is not supported in DATA plans. DATA plans must not include voice or voice-related fields.

## Example Data Plans

A typical DATA plan in the Indian market: plan_type DATA, validity_days 28, price ₹149, data_type PER_DAY, data_gb 1.5 GB per day. Another example: validity_days 365, price ₹1499, data_type TOTAL, data_gb 100 GB total. A third example: validity_days 84, price ₹399, data_type PER_DAY, data_gb 3 GB per day, sms_per_day 10. These plans serve users whose primary need is data access.

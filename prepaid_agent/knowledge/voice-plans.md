---
category: plan_type_def
plan_type: VOICE
version: "1"
status: active
---
# Voice Plans

## What is a Voice Plan

A VOICE plan is a prepaid plan that provides voice calling minutes as the primary benefit. VOICE plans are designed for users who need calling capabilities for communication without data requirements. VOICE plans offer either unlimited calling or a specific minute allocation within the validity period.

## Required Fields for Voice Plans

A VOICE plan must include the following fields: plan_type (VOICE), validity_days (1-365), price (₹10-₹5000), and voice (either "UNLIMITED" or a specific minute count from 1-10000). The voice field determines the calling allowance for the validity period. Each VOICE plan requires a single plan_type, validity_days, and price to function.

## Optional Fields for Voice Plans

SMS benefits may be optionally included in VOICE plans via the sms_per_day field (0-100 SMS messages per day). If SMS is not needed, this field can be omitted. Data access is not supported in VOICE plans. VOICE plans must not include data or data-related fields like data_type or data_gb.

## Example Voice Plans

A typical VOICE plan in the Indian market: plan_type VOICE, validity_days 28, price ₹99, voice UNLIMITED. Another example: validity_days 56, price ₹179, voice 1200 minutes, sms_per_day 50. A third example: validity_days 365, price ₹999, voice UNLIMITED, sms_per_day 100. These plans serve users whose primary need is calling without data access.

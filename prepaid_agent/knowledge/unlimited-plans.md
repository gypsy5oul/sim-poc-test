---
category: plan_type_def
plan_type: UNLIMITED
version: "1"
status: active
---
# Unlimited Plans

## What is an Unlimited Plan

An UNLIMITED plan is a prepaid plan that offers unlimited voice calling combined with daily data access subject to a fair-usage limit. UNLIMITED plans are designed for users who want unrestricted calling without worrying about minute limits, while maintaining reasonable data usage boundaries through daily fair-usage caps.

## Required Fields for Unlimited Plans

An UNLIMITED plan must include the following fields: plan_type (UNLIMITED), validity_days (1-365), price (₹10-₹5000), and data_gb (0.5-5 GB per day, the daily Fair-Usage Policy limit). The voice field is automatically set to "UNLIMITED" and data_type is automatically set to "PER_DAY" when creating UNLIMITED plans. Each UNLIMITED plan requires a single plan_type, validity_days, and price.

## Daily Fair-Usage Policy (FUP)

The data_gb field in UNLIMITED plans specifies the daily Fair-Usage Policy (FUP) limit. Users have unlimited data consumption in a day, but speeds are throttled after crossing the FUP limit for that day. The FUP allowance resets every day during the validity period. For example, an UNLIMITED plan with data_gb 2 allows 2 GB of high-speed data daily, with throttled speeds beyond that limit each day.

## Optional Fields for Unlimited Plans

SMS benefits may be optionally included in UNLIMITED plans via the sms_per_day field (0-100 SMS messages per day). If SMS is not needed, this field can be omitted. Other plan type-specific fields must not be included in UNLIMITED plans.

## Example Unlimited Plans

A typical UNLIMITED plan in the Indian market: plan_type UNLIMITED, validity_days 28, price ₹449, data_gb 2 (daily FUP), voice UNLIMITED (automatic), sms_per_day 100. Another example: validity_days 84, price ₹1099, data_gb 3 (daily FUP), voice UNLIMITED (automatic). These plans serve users wanting unlimited calling with daily data boundaries.

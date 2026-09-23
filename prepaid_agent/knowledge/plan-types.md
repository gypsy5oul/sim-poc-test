---
category: plan_type_def
plan_type: ALL
version: "1"
status: active
---
# Plan Types Overview

## DATA Plans

DATA plans provide mobile data as the primary benefit. A DATA plan requires a data_type (PER_DAY or TOTAL) and a data_gb allocation. Voice calling is not included in DATA plans. SMS benefits are optional. DATA plans are ideal for users whose primary need is internet access without calling requirements.

## VOICE Plans

VOICE plans provide voice calling minutes as the primary benefit. A VOICE plan requires a voice field specifying either "UNLIMITED" or a minute limit from 1 to 10000 minutes. Data access is not included in VOICE plans. SMS benefits are optional. VOICE plans serve users whose primary need is calling without data.

## COMBO Plans

COMBO plans combine data and voice benefits in a single plan. A COMBO plan requires data_type (PER_DAY or TOTAL), data_gb allocation, and a voice field. The voice field can be "UNLIMITED" or a specific minute limit. SMS benefits are optional. COMBO plans suit users who need both data and calling.

## UNLIMITED Plans

UNLIMITED plans offer unlimited voice calling and daily data with a fair-usage cap. An UNLIMITED plan requires a data_gb field which sets the daily Fair-Usage Policy (FUP) limit. Voice is always set to "UNLIMITED" and data_type is always "PER_DAY" automatically. These plans are for users who want unlimited calling with structured daily data allowance.

## Choosing a Plan Type

Select DATA for users wanting primarily internet access. Choose VOICE for users who call frequently without data needs. Pick COMBO for balanced data and calling requirements. Select UNLIMITED for users wanting unlimited calling with daily data caps. All plans require plan_type, validity_days (1-365 days), and price (₹10-₹5000).

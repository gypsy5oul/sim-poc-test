---
category: plan_rule
plan_type: ALL
version: "1"
status: active
---
# Pricing Rules

## Price Range for All Plans

Every prepaid plan (DATA, VOICE, COMBO, UNLIMITED) must have a price field specified in Indian Rupees (₹) with a value between ₹10 and ₹5000 inclusive. The minimum price is ₹10. The maximum price is ₹5000. Prices outside this range are not allowed for any plan type.

## Price as Mandatory Field

The price parameter is a mandatory field for all plan types. No plan can be created without specifying a price. The price field applies uniformly across DATA, VOICE, COMBO, and UNLIMITED plan types. Each plan has a single price for its validity period regardless of plan type.

## Price Specification

Prices must be specified in Indian Rupees and must be whole numbers within the ₹10 to ₹5000 range. Fractional prices (e.g., ₹99.50) are not allowed; prices must be integer amounts. For example, ₹10, ₹99, ₹299, ₹599, ₹1499, ₹3999, and ₹5000 are valid prices.

## Validation of Price

When creating a plan, the price value is validated to ensure it falls within the ₹10 to ₹5000 range. Invalid values such as ₹5, ₹9, ₹5001, or negative prices will be rejected. The price field must be a positive integer within the specified range.

---
category: plan_rule
plan_type: ALL
version: "1"
status: active
---
# SMS Rules

## SMS as Optional Benefit

The sms_per_day field is an optional benefit that can be added to any plan type (DATA, VOICE, COMBO, UNLIMITED). If SMS is not required, this field may be omitted from the plan definition. When included, sms_per_day specifies the number of SMS messages allowed per calendar day.

## SMS Per Day Range

The sms_per_day field, when included, must be a value between 0 and 100 messages per day inclusive. A value of 0 means no SMS benefit is provided. Valid values include 0, 10, 20, 25, 50, 75, and 100 SMS per day. This allowance resets every calendar day during the plan validity period. The SMS allowance applies uniformly across all plan types.

## SMS in Different Plan Types

DATA plans may optionally include sms_per_day. VOICE plans may optionally include sms_per_day. COMBO plans may optionally include sms_per_day. UNLIMITED plans may optionally include sms_per_day. The sms_per_day field is treated the same way regardless of plan type when present.

## Daily SMS Reset

When sms_per_day is specified, the SMS allowance resets every calendar day throughout the plan validity period. For example, a plan with sms_per_day 50 allows 50 SMS messages on day 1, then 50 SMS messages on day 2, and so on. Unused SMS from one day do not carry over to the next day.

## Validation of SMS Benefits

When the sms_per_day field is included in a plan, its value must be a number between 0 and 100. Invalid values such as -1, 101, or non-numeric entries will be rejected. Omitting sms_per_day is allowed; it indicates no SMS benefit is included in the plan.

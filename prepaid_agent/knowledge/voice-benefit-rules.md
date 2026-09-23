---
category: plan_rule
plan_type: ALL
version: "1"
status: active
---
# Voice Benefit Rules

## Voice Benefit Specification

The voice field specifies calling allowance in a plan. Two voice formats are allowed: the string "UNLIMITED" for unlimited calling, or a numeric value representing a minute limit from 1 to 10000 minutes. VOICE, COMBO, and UNLIMITED plan types include voice benefits. DATA plans do not include voice and must not have a voice field.

## Unlimited Voice

When voice is set to "UNLIMITED", the plan provides unlimited calling during the validity period without minute restrictions. COMBO plans can include "UNLIMITED" voice. UNLIMITED plan type automatically has voice set to "UNLIMITED". Users with unlimited voice can call without consuming minute balances.

## Limited Voice Minutes

When voice is specified as a numeric value, it must be between 1 and 10000 minutes inclusive. Valid voice minute values include 100, 300, 500, 600, 1000, 1200, 2000, 5000, and 10000 minutes, or any integer within this range. These minutes are available during the plan validity period for outgoing calls. Once minutes are consumed, no further calling is available unless the plan is recharged.

## Voice Required in VOICE, COMBO, and UNLIMITED Plans

VOICE plan type requires a voice field; this is mandatory. COMBO plan type requires a voice field (either "UNLIMITED" or 1-10000 minutes); this is mandatory. UNLIMITED plan type automatically has voice set to "UNLIMITED"; no manual specification is needed. DATA plan type must not include a voice field.

## Validation of Voice Benefits

When creating plans with voice benefits, voice must either be the string "UNLIMITED" or a numeric value from 1 to 10000. Invalid values such as 0 minutes, 10001 minutes, negative numbers, or non-numeric strings will be rejected. Plans lacking valid voice specifications will be rejected.

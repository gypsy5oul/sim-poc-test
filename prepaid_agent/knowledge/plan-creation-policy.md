---
category: policy
plan_type: ALL
version: "1"
status: active
---
# Plan Creation Policy

## Plan Creation Workflow Overview

The plan creation process follows a structured workflow: collect required fields from user input, validate all fields against backend rules, summarize the complete plan details, obtain explicit user confirmation, and provisioning of the plan only after confirmed acceptance. The workflow applies to all plan types (DATA, VOICE, COMBO, UNLIMITED).

## Step 1: Collect Required Fields

Gather all mandatory fields based on the plan type being created. All plan types require: plan_type, validity_days, and price. Additional required fields depend on plan_type: DATA requires data_type and data_gb; VOICE requires voice; COMBO requires data_type, data_gb, and voice; UNLIMITED requires data_gb. Ask the user for each required field clearly. Optional fields like sms_per_day can be offered or left empty.

## Step 2: Validate All Fields

Validate each field against the backend hard rules: plan_type must be DATA, VOICE, COMBO, or UNLIMITED; validity_days must be 1-365; price must be ₹10-₹5000; data_type must be PER_DAY or TOTAL; data_gb must meet type-specific ranges; voice must be "UNLIMITED" or 1-10000 minutes; sms_per_day must be 0-100. Reject invalid entries and ask the user to correct them before proceeding.

## Step 3: Summarize Plan Details

Present a complete summary of all plan details to the user for review before confirmation. The summary must include plan_type, validity_days, price, all data fields (if applicable), voice field (if applicable), and SMS field (if included). Format the summary clearly so the user can verify each detail.

## Step 4: Explicit User Confirmation

Request explicit user confirmation before plan provisioning. The confirmation must be unambiguous (e.g., "yes" or "confirm"). Do not assume consent. The user may request corrections at this stage; corrections are allowed and the modified plan summary should be presented again for re-confirmation.

## Step 5: Plan Provisioning

Only after receiving explicit user confirmation, provision the plan. The system automatically assigns a plan ID in the format PP-XXXX (where XXXX is a unique identifier). The new plan is automatically set with status ACTIVE. Plan creation is complete and the plan ID is provided to the user.

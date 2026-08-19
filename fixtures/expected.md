---
id: "sample"
name: "Sample"
group: IMMD
url: "/Sample"
---

# Direct Read

- MCGDATA.T_SOURCE
- REPORTING.CUSTOMER

# Direct Write

- REPORTING.T_TARGET

# Calls

- MCGDATA.PKG.CUSTOM_FUNC
- REPORTING.PKG.PROC_LOAD

# CTE / Logical Relations

- ACTIVE_ITEMS
  - Reads: MCGDATA.T_SOURCE
  - Consumers: OUTER_QUERY


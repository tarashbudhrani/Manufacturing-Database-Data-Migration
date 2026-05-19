 🏭 ManufactureOps DB

> A production-grade SQL database that turns messy flat-file factory data into a fully normalized, trigger-enforced operational system — built for real manufacturing environments.

🎯 What This Does
📦 TracksRaw materials, machines, production orders, quality checks🔄 CleansMessy flat-file data → normalized tables via ETL⚡ Enforces4 business rules automatically via SQL triggers🚨 AlertsLow stock, failed QC, and schedule conflicts — in real time

## 📐 Architecture

```
SUPPLIERS ──────────────────────┐
                                ▼
RAWMATERIALS ──────► MATERIALINVENTORY ──────► PRODUCTIOMATERIALUSAGE
                                                          ▲
CUSTOMERS ────────────────────────────────────────────────┤
                                ▼                         │
MACHINES ────────► PRODUCTIONORDERS ──────────────────────┘
                                ▼
EMPLOYEES ────────► QUALITYCHECKS
                                ▼
                    MaterialLowStockLog  ◄── auto-alert trigger
```

---

## 🗂️ Tables at a Glance

| Table | What it stores |
|---|---|
| `SUPPLIERS` | Vendors who supply raw materials |
| `CUSTOMERS` | Clients who place production orders |
| `RAWMATERIALS` | Material catalog (name + grade) |
| `MACHINES` | Factory machines across Plant 1 & Plant 2 |
| `MATERIALINVENTORY` | Received batches with live stock levels |
| `PRODUCTIONORDERS` | Work orders — linked to customer, machine, schedule |
| `PRODUCTIOMATERIALUSAGE` | Which batches were consumed per order |
| `EMPLOYEES` | Inspectors and floor staff |
| `QUALITYCHECKS` | Pass / Fail results per production order |
| `MaterialLowStockLog` | Auto-logged alerts when stock drops below threshold |


<img width="1333" height="826" alt="image" src="https://github.com/user-attachments/assets/670502e6-ea18-4703-82a2-eae5940601c8" />



**Key cleaning steps:**

- Supplier name variants (`"Steel Corp Ltd"`, `"SteelCorp"`) → unified name
- Unit variants (`"KILOGRAM"`, `"KGS"`, `"kg"`) → `KG`
- Date formats mixed (`dd-mm-yyyy` and `mm-dd-yyyy`) → handled with `TRY_CONVERT` + `COALESCE`
- Quantities with `$` signs and commas → cast cleanly to `DECIMAL`
- Machine names with `P1-` / `P2-` prefixes → plant ID extracted, prefix stripped

---

What was cleaned:
ProblemFixSupplier name variants ("Steel Corp Ltd", "SteelCorp")Unified via CASE WHEN LIKEUnit variants ("KILOGRAM", "KGS", "kg")Mapped to KGMixed date formats (dd-mm-yyyy / mm-dd-yyyy)TRY_CONVERT + COALESCEQuantities with $ signs and commasStripped → cast to DECIMALMachine names with P1- / P2- prefixesPlant ID extracted, prefix stripped

⚡ Triggers
#TriggerFires onWhat happens1Quality fail flagINSERT → QUALITYCHECKSSets order → Rework Required2Inventory deductionINSERT / UPDATE → PRODUCTIOMATERIALUSAGEDeducts stock · rolls back if negative3Schedule conflict guardINSERT / UPDATE → PRODUCTIONORDERSBlocks overlapping machine bookings4Low stock alertINSERT / UPDATE → MATERIALINVENTORYLogs alert if stock < 500 units

🔐 Constraints
RuleDetailOrder status9 valid values (Scheduled, In Progress, Completed, etc.)Date sequenceOrderDate ≤ ScheduledStart ≤ ScheduledEnd — DB-level CHECKMaterial uniquenessUnique per (MaterialName, MaterialGrade)Unit valuesKG · M · PCS · FT · SQ_FT · LBSReferential integrityFull FK chain across all 9 tables

🛠️ Stack
SQL Server · T-SQL · SSMS

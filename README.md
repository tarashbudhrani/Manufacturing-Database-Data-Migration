# 🏭 ManufactureOps DB

> Cleaned 10,000+ rows of messy factory data into a fully normalized SQL Server database — with live inventory tracking, machine scheduling, and automated quality alerts.

---

## 🎯 What This Does

| | |
|---|---|
| 📦 **Tracks** | Raw materials, machines, production orders, quality checks |
| 🔄 **Cleans** | Messy flat-file data → normalized tables via ETL |
| ⚡ **Enforces** | 4 business rules automatically via SQL triggers |
| 🚨 **Alerts** | Low stock, failed QC, and schedule conflicts — in real time |

---

## ✅ Key Wins

- Eliminated data chaos across 10,000+ records by building a full ETL pipeline from a single dirty flat file into 9 normalized tables
- Blocked material over-consumption by writing a rollback trigger that stops any usage insert pushing stock below zero
- Prevented 100% of machine double-bookings by enforcing schedule conflict checks at the database level, not the app layer
- Cut manual QC escalation to zero by auto-flagging production orders as `Rework Required` the moment an inspector logs a failure

---

## 📐 ER Diagram

<img width="1315" height="822" alt="image" src="https://github.com/user-attachments/assets/5462130a-a8d8-432c-bed5-8fde23574258" />


---

## 🗂️ Tables

| Table | What it stores |
|---|---|
| `SUPPLIERS` | Vendors who supply raw materials |
| `CUSTOMERS` | Clients who place production orders |
| `RAWMATERIALS` | Material catalog — name + grade |
| `MACHINES` | Factory machines across Plant 1 and Plant 2 |
| `MATERIALINVENTORY` | Received batches with live stock levels |
| `PRODUCTIONORDERS` | Work orders linked to customer, machine, and schedule |
| `PRODUCTIOMATERIALUSAGE` | Which batches were consumed per order |
| `EMPLOYEES` | Inspectors and floor staff |
| `QUALITYCHECKS` | Pass / Fail results per production order |
| `MaterialLowStockLog` | Auto-logged alerts when stock drops below threshold |

---

## ⚙️ ETL — How the Data Was Cleaned

Raw data arrived as a single flat file `ABC_10000` — inconsistent names, mixed date formats, and dirty quantities. It was loaded into a staging table `DUMMY`, cleaned, then inserted into normalized tables.

```
ABC_10000  (raw flat file)
     │
     ▼
  DUMMY  (staging)
     │
     ├── Clean supplier names    →  SUPPLIERS
     ├── Normalize units         →  MATERIALINVENTORY
     ├── Fix date formats        →  PRODUCTIONORDERS
     ├── Strip machine prefixes  →  MACHINES
     └── Resolve foreign keys    →  all tables
```

| Problem | Fix |
|---|---|
| Supplier name variants — `"Steel Corp Ltd"`, `"SteelCorp"` | Unified via `CASE WHEN LIKE` |
| Unit variants — `"KILOGRAM"`, `"KGS"`, `"kg"` | Mapped to `KG` |
| Mixed date formats — `dd-mm-yyyy` and `mm-dd-yyyy` | `TRY_CONVERT` + `COALESCE` |
| Quantities with `$` signs and commas | Stripped then cast to `DECIMAL` |
| Machine names with `P1-` / `P2-` prefixes | Plant ID extracted, prefix stripped |

---

## ⚡ Triggers

| # | Trigger | Fires on | What happens |
|---|---|---|---|
| 1 | Quality fail flag | `INSERT` on QUALITYCHECKS | Sets order status → `Rework Required` |
| 2 | Inventory deduction | `INSERT / UPDATE` on PRODUCTIOMATERIALUSAGE | Deducts stock — rolls back if negative |
| 3 | Schedule conflict guard | `INSERT / UPDATE` on PRODUCTIONORDERS | Blocks overlapping machine bookings |
| 4 | Low stock alert | `INSERT / UPDATE` on MATERIALINVENTORY | Logs alert when stock drops below 500 units |

---

## 🔐 Constraints

| Rule | Detail |
|---|---|
| Order status | 9 valid values — `Scheduled`, `In Progress`, `Completed`, `On Hold`, `Cancelled`, `Rework Required`, `Quoted`, `Pending Materials`, `Rework Complete` |
| Date sequence | `OrderDate ≤ ScheduledStart ≤ ScheduledEnd` enforced via DB-level `CHECK` |
| Material uniqueness | Unique per `(MaterialName, MaterialGrade)` combination |
| Unit values | Restricted to `KG` · `M` · `PCS` · `FT` · `SQ_FT` · `LBS` |
| Referential integrity | Full FK chain across all 9 tables |

---

## 🛠️ Stack

`SQL Server` &nbsp;·&nbsp; `T-SQL` &nbsp;·&nbsp; `SSMS`

---


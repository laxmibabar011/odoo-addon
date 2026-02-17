# 📊 Real-Time Sales Margin Dashboard (Odoo)

## 📌 Project Overview
**Real-Time Sales Margin Dashboard** is a custom Odoo module that enhances the standard Sales module by introducing real-time profitability analysis. 

It transforms a standard Sale Order into a financial decision-making dashboard, helping businesses monitor profitability before confirming quotations by calculating and displaying:
- **Cost of Goods Sold (COGS)**
- **Landed Cost**
- **Configurable Overhead**
- **Net Margin** (per line and per order)

---

## 🚀 Key Features

### 🔹 1. Line-Level Margin Calculation
Each sale order line automatically computes:
- **COGS**: Fetched directly from product cost.
- **Landed Cost**: Manual per-line entry for specific shipping/handling costs.
- **Overhead Cost**: Rule-based or global fallback.
- **Margin Value**: Net profit per line.

> **Formula Used:**
> `Total Cost = (COGS + Landed Cost + Overhead) × Quantity`
> `Margin = Revenue – Total Cost`

### 🔹 2. Order-Level Profit Dashboard
A dedicated banner inside the Sale Order form displays:
- ✅ Total Revenue
- ✅ Total COGS
- ✅ Total Overhead
- ✅ **Net Margin** (Highlighted KPI)

Includes quick actions:
- **Recompute Margins** button
- **Detailed Breakdown** button for deep-dive analysis.

### 🔹 3. Configurable Overhead Rules
Manage overheads with precision using the new `sale.overhead.rule` model:
- **Category-based rules**: Apply different costs to different product groups.
- **Flexible Types**: Choose between *Percentage of COGS* or *Fixed amount per unit*.
- **Control**: Active/Inactive toggles and Sales Manager-only access.
- **Global Fallback**: Automatically uses a global percentage if no specific rule is found.

### 🔹 4. Margin Breakdown Wizard
An interactive popup wizard for transparency:
- Aggregate totals overview.
- Line-by-line margin details.
- Expandable cost breakdown (COGS, Landed, Overhead).
- Visual profit/loss highlighting for quick identification.

### 🔹 5. Role-Based Security
| Role | Access Level |
| :--- | :--- |
| **Sales Manager** | Full control over overhead configuration |
| **Sales User** | Read-only access to overhead rules |
| **Internal User** | Access to margin breakdown wizard |

---

## ⚙️ Installation
1. Copy the module folder into your Odoo **addons** directory.
2. Restart your Odoo server.
3. Enable **Developer Mode**.
4. Navigate to **Apps** -> **Update Apps List**.
5. Search for "Real-Time Sales Margin Dashboard" and click **Install**.

---

## 🔧 Configuration & Usage

### Step 1: Configure Overhead Rules
Go to **Real-Time Margin Dashboard** → **Overhead Configuration** and create rules:
- Select a **Product Category**.
- Choose **Overhead Type** (Percentage or Fixed).
- Enter the value and **Activate** the rule.

### Step 2: Create Sale Order
1. Create a new quotation and add products.
2. Enter **Landed Cost** per line if applicable.
3. Review calculations in the dashboard banner.
4. Click **Analysis Breakdown** for a detailed cost view.

### 🔄 Manual Recalculation
If product costs or overhead rules change after the order is created, click the **Recompute Margins** button in the Sale Order header.

---

## 🏗 Technical Highlights
- **Inheritance**: Extends `sale.order` and `sale.order.line` without breaking core logic.
- **Reactive**: Uses `@api.depends` for instant UI updates.
- **Persistence**: Implements `TransientModel` for the analysis wizard.
- **Settings**: Uses `ir.config_parameter` for global fallback configuration.
- **UI/UX**: Upgrade-safe XML view inheritance via XPath and professional Bootstrap styling.
- **Security**: Strict access control via `ir.model.access.csv`.


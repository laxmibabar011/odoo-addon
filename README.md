📊 Real-Time Sales Margin Dashboard (Odoo)

A powerful Odoo module that enhances the Sales module with real-time profitability analysis, configurable overhead allocation, and detailed margin breakdown visualization.

This module transforms the standard Sale Order into a financial decision-making dashboard.

🚀 Business Problem

Standard Odoo Sales provides revenue tracking but does not offer:

Real-time COGS visibility

Configurable overhead allocation

Landed cost inclusion per line

Line-level profitability insights

Financial breakdown visualization

This module solves that by introducing:

✔ Real-time margin computation
✔ Category-based overhead rules
✔ Configurable overhead logic
✔ Interactive profitability dashboard
✔ Detailed cost breakdown wizard

🏗️ Architecture Overview

The module extends:

sale.order

sale.order.line

It introduces:

Configurable overhead rule model

Transient wizard models for financial breakdown

Custom dashboard UI components

Role-based access control

The design follows:

Clean inheritance (no core modification)

Modular compute methods

Configuration-driven logic

Upgrade-safe view inheritance

✨ Key Features
📌 1. Line-Level Margin Calculation

Each sale order line calculates:

COGS (from product standard price)

Landed Cost (manual per line)

Overhead Cost (configurable)

Final Margin

Formula:

Total Cost = (COGS + Landed + Overhead) × Quantity
Margin = Revenue – Total Cost

📌 2. Order-Level Profitability Dashboard

Inside Sale Order form:

Total Revenue

Total COGS

Total Overhead

Net Margin (highlighted)

Manual Recompute Button

Breakdown Analysis Button

This acts as a live financial KPI banner.

📌 3. Configurable Overhead Rules

New model: sale.overhead.rule

Supports:

Category-based rules

Percentage of COGS

Fixed amount per unit

Active toggle

Manager-controlled access

Fallback to global system parameter if no category rule exists.

📌 4. Margin Breakdown Wizard

Popup provides:

Aggregate totals

Line-by-line profitability

Cost component breakdown

Visual profit/loss highlighting

Nested expandable cost structure

Designed for finance transparency.

📌 5. Role-Based Security
Role	Overhead Rules	Wizard Access
Sales Manager	Full Access	Full
Sales User	Read Only	Full
Internal User	N/A	Full

Ensures financial configuration integrity.

🖥️ UI Enhancements

Financial KPI banner in Sale Order

Conditional margin coloring

Monetary widgets

Clean Bootstrap styling

Optional column visibility

Structured menu segregation

📂 Module Structure
real_time_margin_dashboard/
│
├── models/
│   ├── sale_order.py
│   ├── overhead_rule.py
│   ├── margin_wizard.py
│
├── views/
│   ├── sale_order_views.xml
│   ├── overhead_rule_views.xml
│   ├── wizard_views.xml
│
├── security/
│   ├── ir.model.access.csv
│
├── __manifest__.py
└── README.md

⚙️ Installation

Place module inside your Odoo addons directory.

Update app list.

Install module from Apps menu.

Configure overhead rules from:

Real-Time Margin Dashboard → Overhead Configuration

🔄 How It Works

User creates quotation.

Product COGS is fetched from standard_price.

User enters optional landed cost.

Overhead is calculated:

Category rule → If exists

Otherwise → Global percentage fallback

Margin computed dynamically.

Dashboard updates instantly.

Manual recompute available if product costs change.

🧠 Technical Highlights

Uses @api.depends for reactive computation

Uses TransientModel for wizard isolation

Uses ir.config_parameter for fallback configuration

Uses view inheritance via XPath (upgrade-safe)

Uses conditional invisibility and decoration attributes

Follows Odoo security best practices

📊 Business Impact

Real-time profitability insight

Faster pricing decisions

Prevents loss-making quotations

Improves sales margin control

Financial transparency for management
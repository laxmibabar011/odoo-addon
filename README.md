# Real-Time Margin Dashboard (Odoo 19 Addon)

## Overview
This Odoo module provides an architectural solution for sales margin tracking with a detailed cost breakdown. It allows managers to view real-time COGS (Cost of Goods Sold) and overhead calculations directly within Sales Orders.

## Features
- **Smart Margin Card**: Integrated directly into the Sales Order view.
- **Real-time Calculations**: Instant COGS and Overhead calculation.
- **Cost Breakdown Popup**: Detailed visibility into how margins are derived.
- **Portal Visibility**: Specifically designed for manager-level access.

## Technical Details
- **Odoo Version**: 19.0
- **Category**: Sales
- **Dependencies**: 
  - `sale_management`
  - `stock_account`
  - `stock_landed_costs`
  - `account`

## Installation
1. Copy the `my_assignment` folder into your Odoo `custom_addons` directory.
2. Restart your Odoo server.
3. Enable **Developer Mode**.
4. Go to **Apps** -> **Update Apps List**.
5. Search for "Real-Time Margin Dashboard" and click **Install**.

## Usage
Once installed, navigate to any Sales Order to see the Margin Card and cost breakdown features.

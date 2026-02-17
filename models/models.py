# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    cogs_price = fields.Float(string='COGS', compute='_compute_margin_fields', store=False)
    landed_cost = fields.Float(string='Landed Cost', default=0.0, help="Manual entry for landed costs (freight, customs, etc.)")
    overhead_cost = fields.Float(string='Overhead Cost', compute='_compute_margin_fields', store=False)
    margin_value = fields.Float(string='Margin Value', compute='_compute_margin_fields', store=False)

    @api.depends('product_id', 'product_id.standard_price', 'product_id.product_tmpl_id.standard_price', 'product_uom_qty', 'price_subtotal', 'landed_cost')
    def _compute_margin_fields(self):
        for line in self:
            if not line.product_id:
                line.cogs_price = 0.0
                line.overhead_cost = 0.0
                line.margin_value = 0.0
                continue
                
            # Base cost is standard_price (Cost Price)
            # Use standard_price from product, which is related to template
            line.cogs_price = line.product_id.standard_price
            
            # Get overhead based on configuration
            overhead_cost = line._get_overhead_cost()
            line.overhead_cost = overhead_cost
            
            # Total Cost per unit = COGS + Landed + Overhead
            total_cost_unit = line.cogs_price + line.landed_cost + line.overhead_cost
            
            # Total Cost for the line quantity
            total_cost = total_cost_unit * line.product_uom_qty
            
            # Margin = Price Subtotal - Total Cost
            line.margin_value = line.price_subtotal - total_cost

    def _get_overhead_cost(self):
        """Calculate overhead based on rules and configuration"""
        self.ensure_one()

        # 1. Check for Category-specific rule
        if self.product_id.categ_id:
            rule = self.env['sale.overhead.rule'].search([
                ('category_id', '=', self.product_id.categ_id.id),
            ], limit=1)
            
            if rule:
                return self._calculate_rule_amount(rule)
        
        # 2. Fallback to system parameter
        overhead_percent = float(self.env['ir.config_parameter'].sudo().get_param('margin.overhead_percent', default=5.0))
        return self.cogs_price * (overhead_percent / 100.0)

    def _calculate_rule_amount(self, rule):
        if rule.overhead_type == 'fixed':
            return rule.overhead_fixed_amount
        else:  # percentage
            return self.cogs_price * (rule.overhead_percent / 100.0)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_cogs = fields.Float(string='Total COGS', compute='_compute_total_margin', store=False)
    total_overhead = fields.Float(string='Total Overhead', compute='_compute_total_margin', store=False)
    net_margin = fields.Float(string='Net Margin', compute='_compute_total_margin', store=False)

    @api.depends('order_line.margin_value', 'order_line.cogs_price', 'order_line.overhead_cost', 
                 'order_line.product_uom_qty', 'order_line.product_id.standard_price', 'order_line.product_id.product_tmpl_id.standard_price')
    def _compute_total_margin(self):
        for order in self:
            total_cogs = 0.0
            total_overhead = 0.0
            net_margin = 0.0
            
            for line in order.order_line:
                total_cogs += line.cogs_price * line.product_uom_qty
                total_overhead += line.overhead_cost * line.product_uom_qty
                net_margin += line.margin_value
            
            order.total_cogs = total_cogs
            order.total_overhead = total_overhead
            order.net_margin = net_margin

    def action_recompute_margins(self):
        """Manual button to force recomputation of all margin fields"""
        self.ensure_one()
        # Force recomputation by invalidating cache
        self.env.invalidate_all() # Ensure fresh read
        self.order_line.invalidate_recordset(['cogs_price', 'overhead_cost', 'margin_value'])
        self.invalidate_recordset(['total_cogs', 'total_overhead', 'net_margin'])
        # Trigger recomputation
        for line in self.order_line:
            line._compute_margin_fields()
        self._compute_total_margin()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Margins Recomputed',
                'message': 'All margin values have been recalculated based on current product costs.',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_open_margin_breakdown(self):
        self.ensure_one()
        lines = []
        for line in self.order_line:
            # Create cost details for expandable view
            cost_details = []
            
            # Add COGS detail
            if line.cogs_price:
                cost_details.append((0, 0, {
                    'name': 'Base COGS',
                    'cost_type': 'cogs',
                    'amount': line.cogs_price * line.product_uom_qty,
                }))
            
            # Add Landed Cost detail (placeholder for breakdown)
            if line.landed_cost:
                cost_details.append((0, 0, {
                    'name': 'Landed Cost (Freight, Customs, etc.)',
                    'cost_type': 'landed',
                    'amount': line.landed_cost * line.product_uom_qty,
                }))
            
            # Add Overhead detail
            if line.overhead_cost:
                cost_details.append((0, 0, {
                    'name': 'Overhead (Allocated)',
                    'cost_type': 'overhead',
                    'amount': line.overhead_cost * line.product_uom_qty,
                }))
            
            lines.append((0, 0, {
                'product_id': line.product_id.id,
                'quantity': line.product_uom_qty,
                'price_unit': line.price_unit,
                'price_subtotal': line.price_subtotal,
                'cogs_price': line.cogs_price,
                'landed_cost': line.landed_cost,
                'overhead_cost': line.overhead_cost,
                'margin_value': line.margin_value,
                'cost_detail_ids': cost_details,
            }))
        
        wizard = self.env['sale.margin.breakdown.wizard'].create({
            'order_id': self.id,
            'line_ids': lines,
        })
        
        return {
            'name': 'Margin Breakdown',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.margin.breakdown.wizard',
            'res_id': wizard.id, 
            'view_mode': 'form',
            'target': 'new',
        }

class SaleMarginBreakdownWizard(models.TransientModel):
    _name = 'sale.margin.breakdown.wizard'
    _description = 'Sale Margin Breakdown Wizard'

    order_id = fields.Many2one('sale.order', string='Sale Order', required=True, readonly=True)
    line_ids = fields.One2many('sale.margin.breakdown.line', 'wizard_id', string='Breakdown Lines', readonly=True)
    
    # Aggregate fields
    total_quantity = fields.Float(string='Total Quantity', compute='_compute_totals')
    total_revenue = fields.Float(string='Total Revenue', compute='_compute_totals')
    total_cogs = fields.Float(string='Total COGS', compute='_compute_totals')
    total_landed = fields.Float(string='Total Landed Cost', compute='_compute_totals')
    total_overhead = fields.Float(string='Total Overhead', compute='_compute_totals')
    total_margin = fields.Float(string='Total Margin', compute='_compute_totals')

    @api.depends('line_ids.quantity', 'line_ids.price_subtotal', 'line_ids.cogs_price', 
                 'line_ids.landed_cost', 'line_ids.overhead_cost', 'line_ids.margin_value')
    def _compute_totals(self):
        for wizard in self:
            wizard.total_quantity = sum(wizard.line_ids.mapped('quantity'))
            wizard.total_revenue = sum(wizard.line_ids.mapped('price_subtotal'))
            wizard.total_cogs = sum(line.cogs_price * line.quantity for line in wizard.line_ids)
            wizard.total_landed = sum(line.landed_cost * line.quantity for line in wizard.line_ids)
            wizard.total_overhead = sum(line.overhead_cost * line.quantity for line in wizard.line_ids)
            wizard.total_margin = sum(wizard.line_ids.mapped('margin_value'))

class SaleMarginBreakdownLine(models.TransientModel):
    _name = 'sale.margin.breakdown.line'
    _description = 'Sale Margin Breakdown Line'

    wizard_id = fields.Many2one('sale.margin.breakdown.wizard', string='Wizard')
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    quantity = fields.Float(string='Quantity', readonly=True)
    price_unit = fields.Float(string='Unit Price', readonly=True)
    price_subtotal = fields.Float(string='Subtotal', readonly=True)
    cogs_price = fields.Float(string='COGS/Unit', readonly=True)
    landed_cost = fields.Float(string='Landed Cost/Unit', readonly=True)
    overhead_cost = fields.Float(string='Overhead/Unit', readonly=True)
    margin_value = fields.Float(string='Margin', readonly=True)
    cost_detail_ids = fields.One2many('sale.margin.cost.detail', 'breakdown_line_id', string='Cost Details')

class SaleMarginCostDetail(models.TransientModel):
    _name = 'sale.margin.cost.detail'
    _description = 'Margin Cost Detail'

    breakdown_line_id = fields.Many2one('sale.margin.breakdown.line', string='Breakdown Line')
    name = fields.Char(string='Description', required=True)
    cost_type = fields.Selection([
        ('cogs', 'COGS'),
        ('landed', 'Landed Cost'),
        ('overhead', 'Overhead'),
    ], string='Type')
    amount = fields.Float(string='Amount')

class SaleOverheadRule(models.Model):
    _name = 'sale.overhead.rule'
    _description = 'Overhead Configuration Rule'

    name = fields.Char(string='Rule Name', required=True)
    category_id = fields.Many2one('product.category', string='Product Category') # Made optional
    
    overhead_type = fields.Selection([
        ('percentage', 'Percentage of COGS'),
        ('fixed', 'Fixed Amount per Unit'),
    ], string='Overhead Type', default='percentage', required=True)
    overhead_percent = fields.Float(string='Overhead %', default=5.0)
    overhead_fixed_amount = fields.Float(string='Fixed Amount')
    active = fields.Boolean(default=True)

from odoo import models, fields
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    quotation_file = fields.Binary(string="Upload File")
    quotation_filename = fields.Char(string="File Name")
    def action_create_purchase_order(self):
        for order in self:

            po_lines = []
            vendor = False

            for line in order.order_line:
                product = line.product_id

                # Skip services
                if product.type != 'product':
                    continue

                qty_available = product.free_qty
                required_qty = line.product_uom_qty

                if qty_available < required_qty:

                    supplier = product.seller_ids[:1]
                    if not supplier:
                        raise UserError(f"No vendor defined for {product.name}")

                    vendor = supplier.name

                    po_lines.append((0, 0, {
                        'product_id': product.id,
                        'name': product.name,
                        'product_qty': required_qty - qty_available,
                        'price_unit': supplier.price or product.standard_price,
                        'date_planned': fields.Datetime.now(),
                    }))

            if not po_lines:
                raise UserError("All products are in stock.")

            if not vendor:
                raise UserError("No vendor found.")

            po = self.env['purchase.order'].create({
                'partner_id': vendor.id,
                'origin': order.name,
                'order_line': po_lines,
            })

            return {
                'type': 'ir.actions.act_window',
                'name': 'Purchase Order',
                'res_model': 'purchase.order',
                'view_mode': 'form',
                'res_id': po.id,
            }
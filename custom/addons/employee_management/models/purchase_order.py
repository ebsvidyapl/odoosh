from odoo import models, fields
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    lead_time = fields.Integer(string='Lead Time (Days)')
    def button_confirm(self):
        for order in self:
            for line in order.order_line:
                if not line.product_id.seller_ids:
                    raise UserError(
                        f"No vendor defined for product: {line.product_id.name}"
                    )
        return super().button_confirm()
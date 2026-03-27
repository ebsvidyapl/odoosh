from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    quotation_file = fields.Binary(string="Upload File")
    quotation_filename = fields.Char(string="File Name")
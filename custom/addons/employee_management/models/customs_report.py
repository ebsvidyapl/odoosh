from odoo import models

class CustomsReport(models.AbstractModel):
    _name = 'report.customs_management.report_customs'
    _description = 'Customs Report'

    def _get_report_values(self, docids, data=None):
        records = self.env['stock.landed.cost'].browse(docids)

        return {
            'docs': records,
        }
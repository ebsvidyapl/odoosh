def _get_report_values(self, docids, data=None):

    print("DOCIDS:", docids)

    docs = self.env['stock.landed.cost'].browse(docids)

    print("DOCS:", docs)

    lines = []

    for cost in docs:
        print("COST:", cost.name)

        for line in cost.valuation_adjustment_lines:
            print("LINE FOUND")

            product = line.product_id or line.move_id.product_id

            if not product:
                continue

            lines.append({
                'product': product.name,
            })

    print("LINES:", lines)

    return {
        'docs': docs,
        'lines': lines,
    }
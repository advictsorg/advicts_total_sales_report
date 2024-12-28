from odoo import models


class TotalSaleXlsx(models.AbstractModel):
    _name = 'report.advicts_total_sales_report.total_sales_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, report):
        style = workbook.add_format({
            'bold': True,
            'bg_color': '#c9c5c5',
            'border': 1,  # 1 is for a thin border
            'valign': 'vcenter',
            'align': 'center'
        })
        style_data = workbook.add_format({
            'border': 1,  # 1 is for a thin border
            'valign': 'vcenter',
            'align': 'center',
        })
        style_data_row = workbook.add_format({
            'border': 1,  # 1 is for a thin border
            'valign': 'vcenter',
            'bg_color': '#EEEEEE',
            'align': 'center'
        })

        title = 'Salesperson Sales & Payments Report'

        report_name = title
        sheet = workbook.add_worksheet(report_name[:31])
        sheet.merge_range("A1:D1", title, style)
        sheet.write(1, 0, 'From', style)
        sheet.write(1, 1, data['start_date'], style)
        sheet.write(1, 2, 'To', style)
        sheet.write(1, 3, data['end_date'], style)

        sheet.write(3, 0, '#', style)
        sheet.write(3, 1, 'Name', style)
        sheet.write(3, 2, 'Sales', style)
        sheet.write(3, 3, 'Payments', style)
        row = 4
        count = 0
        for line in data['data']:
            row += 1
            count += 1
            sheet.write(row, 0, count, style_data)
            sheet.write(row, 1, line['salesperson'], style_data)
            sheet.write(row, 2, line['sales_amount'], style_data)
            sheet.write(row, 3, line['payment_amount'], style_data)

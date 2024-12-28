from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class ReportWizard(models.TransientModel):
    _name = "total.sales.report"
    _description = "Total Sales & Payments Report"

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date', required=True, default=fields.Date.today())
    user_ids = fields.Many2many('res.users', string='Salespersons', domain=[('share', '=', False)])
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        if self.start_date and self.start_date > self.end_date:
            raise ValidationError(_('Start Date must be before End Date'))

    def _get_report_data(self):
        domain = [
            ('move_type', 'in', ['out_invoice', 'out_refund', 'in_payment']),
            ('state', '=', 'posted'),
            ('company_id', '=', self.company_id.id),
        ]
        if self.start_date:
            domain.append(('date', '>=', self.start_date))
        domain.append(('date', '<=', self.end_date))

        moves = self.env['account.move'].search(domain)

        company_currency = self.company_id.currency_id
        report_data = {}

        for move in moves:

            salesperson = move.partner_id.user_id

            if not salesperson or (self.user_ids and salesperson not in self.user_ids):
                continue

            user_id = salesperson.id
            if user_id not in report_data:
                report_data[user_id] = {
                    'salesperson': salesperson.name,
                    'sales_amount': 0,
                    'payment_amount': 0,
                }

            # Convert amount to company currency if needed
            amount = move.amount_total_signed
            if move.currency_id != company_currency:
                amount = move.currency_id._convert(
                    amount,
                    company_currency,
                    self.company_id,
                    move.date or fields.Date.today()
                )

            if move.move_type in ['out_invoice', 'out_refund']:
                report_data[user_id]['sales_amount'] += amount
            elif move.move_type == 'in_payment':
                report_data[user_id]['payment_amount'] += amount
        report_data_list = [
            {
                'salesperson': data['salesperson'],
                'sales_amount': round(data['sales_amount'], 2),
                'payment_amount': round(data['payment_amount'], 2),
            }
            for data in report_data.values()
        ]
        return {
            'data': report_data_list,
            'start_date': self.start_date or '',
            'end_date': self.end_date,
            'company_currency': company_currency.symbol,
        }

    def action_print_pdf_report(self):
        report_data = self._get_report_data()
        return self.env.ref('advicts_total_sales_report.total_sales_report_action').report_action(self,
                                                                                                  data=report_data)

    def action_print_xlsx_report(self):
        report_data = self._get_report_data()
        return self.env.ref('advicts_total_sales_report.total_sales_report_action_xlsx').report_action(self,
                                                                                                       data=report_data)

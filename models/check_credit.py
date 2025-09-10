from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta


class account_move_check_credit(models.Model):
    _inherit = ['account.move']

    notification_message = fields.Char(string="Mensajes", readonly=True)
    credito = fields.Float(string="Credito")
    estado_partner = fields.Selection([('active','Activo'),('deudor','Cliente Moroso'),('tope','Excede Credito')], string="Estado", default='active', readonly=True)

    @api.onchange('partner_id')
    def _check_partner_status(self):
        if self.partner_id:
            Invoice = self.env['account.move']
            nuevo = Invoice.search_count([
                ('partner_id', '=', self.partner_id.id),
                ('move_type', '=', 'out_invoice'),
                ('payment_state', '=', 'not_paid')
            ])
            if nuevo > 0:
                # Bloqueo por facturas vencidas según time_limit (por defecto 90 días)
                limit_days = self.partner_id.time_limit or 90
                date_limit = fields.Date.today() - relativedelta(days=limit_days)
                overdue_limit = Invoice.search_count([
                    ('partner_id', '=', self.partner_id.id),
                    ('move_type', '=', 'out_invoice'),
                    ('payment_state', '=', 'not_paid'),
                    ('invoice_date_due', '<=', date_limit),
                ])
                if overdue_limit > 0:
                    message = _("Este cliente tiene facturas vencidas por más de %s días.") % limit_days
                    self.notification_message = message
                    self.estado_partner = 'deudor'
                    self.state = 'cancel'
                    return {
                        'warning': {
                            'title': _('Aviso'),
                            'message': message,
                        }
                    }

                pre_total = Invoice.search_count([  # Revisa facturas por vencer
                    ('partner_id', '=', self.partner_id.id),
                    ('move_type', '=', 'out_invoice'),
                    ('payment_state', '=', 'not_paid'),
                    ('invoice_date_due', '<', fields.Date.today())
                ])
                vencido = Invoice.search([  # Revisa facturas por vencidas
                    ('partner_id', '=', self.partner_id.id),
                    ('move_type', '=', 'out_invoice'),
                    ('payment_state', '=', 'not_paid')
                ])
                total_deuda = sum(factura.amount_total for factura in vencido)
                if total_deuda > self.partner_id.credit_limit:
                    message = _("Este cliente sobrepasó su credito.")
                    self.notification_message = message
                    self.estado_partner = 'tope'  # Cambiar el estado
                    self.state = 'cancel'
                    return {
                        'warning': {
                            'title': _('Aviso'),
                            'message': message,
                        }
                    }
                if pre_total > 0:
                    message = _("Este cliente tiene facturas vencidas.")
                    self.notification_message = message
                    self.estado_partner = 'deudor'  # Cambiar el estado a "Deudor"
                    return {
                        'warning': {
                            'title': _('Aviso'),
                            'message': message,
                        }
                    }
                else:
                    self.estado_partner = 'active'  # Restaurar el estado a "Activo" si no hay facturas vencidas

        self.notification_message = False


class sale_order_check_credit(models.Model):
    _inherit = ['sale.order']

    notification_message = fields.Char(string="Mensajes", readonly=True)
    credito = fields.Float(string="Credito")
    estado_partner = fields.Selection([('active','Activo'),('deudor','Cliente Moroso'),('tope','Excede Credito')], string="Estado", default='active', readonly=True)

    @api.onchange('partner_id')
    def _check_partner_status(self):
        if self.partner_id:
            Invoice = self.env['account.move']
            nuevo = Invoice.search_count([
                ('partner_id', '=', self.partner_id.id),
                ('move_type', '=', 'out_invoice'),
                ('payment_state', '=', 'not_paid')
            ])
            if nuevo > 0:
                # Bloqueo por facturas vencidas según time_limit (por defecto 90 días)
                limit_days = self.partner_id.time_limit or 90
                date_limit = fields.Date.today() - relativedelta(days=limit_days)
                overdue_limit = Invoice.search_count([
                    ('partner_id', '=', self.partner_id.id),
                    ('move_type', '=', 'out_invoice'),
                    ('payment_state', '=', 'not_paid'),
                    ('invoice_date_due', '<=', date_limit),
                ])
                if overdue_limit > 0:
                    message = _("Este cliente tiene facturas vencidas por más de %s días.") % limit_days
                    self.notification_message = message
                    self.estado_partner = 'deudor'
                    self.state = 'cancel'
                    return {
                        'warning': {
                            'title': _('Aviso'),
                            'message': message,
                        }
                    }

                pre_total = Invoice.search_count([  # Revisa facturas por vencer
                    ('partner_id', '=', self.partner_id.id),
                    ('move_type', '=', 'out_invoice'),
                    ('payment_state', '=', 'not_paid'),
                    ('invoice_date_due', '<', fields.Date.today())
                ])
                vencido = Invoice.search([  # Revisa facturas por vencidas
                    ('partner_id', '=', self.partner_id.id),
                    ('move_type', '=', 'out_invoice'),
                    ('payment_state', '=', 'not_paid')
                ])
                total_deuda = sum(factura.amount_total for factura in vencido)
                if total_deuda > self.partner_id.credit_limit:
                    message = _("Este cliente sobrepasó su credito.")
                    self.notification_message = message
                    self.estado_partner = 'tope'  # Cambiar el estado
                    self.state = 'cancel'
                    return {
                        'warning': {
                            'title': _('Aviso'),
                            'message': message,
                        }
                    }
                if pre_total > 0:
                    message = _("Este cliente tiene facturas vencidas.")
                    self.notification_message = message
                    self.estado_partner = 'deudor'  # Cambiar el estado a "Deudor"
                    return {
                        'warning': {
                            'title': _('Aviso'),
                            'message': message,
                        }
                    }
                else:
                    self.estado_partner = 'active'  # Restaurar el estado a "Activo" si no hay facturas vencidas

        self.notification_message = False

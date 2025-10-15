from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta


class account_move_check_credit(models.Model):
    _inherit = ['account.move']

    notification_message = fields.Char(string="Mensajes", readonly=True)
    credito = fields.Float(string="Credito")
    estado_partner = fields.Selection([
        ('active', 'Activo'),
        ('deudor', 'Cliente Moroso'),
        ('tope', 'Excede Credito')
    ], string="Estado", default='active', readonly=True)

    @api.onchange('partner_id')
    def _check_partner_status(self):
        if not self.partner_id:
            self.notification_message = False
            return

        Invoice = self.env['account.move']
        Payment = self.env['account.payment']

        # --- 1. Bloqueo por facturas vencidas ---
        nuevo = Invoice.search_count([
            ('partner_id', '=', self.partner_id.id),
            ('move_type', '=', 'out_invoice'),
            ('payment_state', '=', 'not_paid')
        ])
        if nuevo > 0:
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
                return {'warning': {'title': _('Aviso'), 'message': message}}

        pre_total = Invoice.search_count([
            ('partner_id', '=', self.partner_id.id),
            ('move_type', '=', 'out_invoice'),
            ('payment_state', '=', 'not_paid'),
            ('invoice_date_due', '<', fields.Date.today())
        ])
        vencido = Invoice.search([
            ('partner_id', '=', self.partner_id.id),
            ('move_type', '=', 'out_invoice'),
            ('payment_state', '=', 'not_paid')
        ])
        total_deuda = sum(factura.amount_total for factura in vencido)
        if total_deuda > self.partner_id.credit_limit:
            message = _("Este cliente sobrepasó su crédito.")
            self.notification_message = message
            self.estado_partner = 'tope'
            self.state = 'cancel'
            return {'warning': {'title': _('Aviso'), 'message': message}}

        if pre_total > 0:
            message = _("Este cliente tiene facturas vencidas.")
            self.notification_message = message
            self.estado_partner = 'deudor'
            return {'warning': {'title': _('Aviso'), 'message': message}}

        # --- 2. Bloqueo por cheques no cobrados vencidos ---
        cheque_limit = fields.Date.today() - relativedelta(days=7)
        cheques_vencidos = Payment.search_count([
            ('partner_id', '=', self.partner_id.id),
            ('payment_method_line_id.name', 'ilike', 'cheque'),
            ('estado_cheque', '=', 'no_cobrado'),
            ('fecha_cobro', '<=', cheque_limit),
        ])
        if cheques_vencidos > 0:
            message = _("Este cliente tiene cheques no cobrados con más de 7 días desde la fecha de cobro.")
            self.notification_message = message
            self.estado_partner = 'deudor'
            self.state = 'cancel'
            return {'warning': {'title': _('Aviso'), 'message': message}}

        self.estado_partner = 'active'
        self.notification_message = False


class sale_order_check_credit(models.Model):
    _inherit = ['sale.order']

    notification_message = fields.Char(string="Mensajes", readonly=True)
    credito = fields.Float(string="Credito")
    estado_partner = fields.Selection([
        ('active', 'Activo'),
        ('deudor', 'Cliente Moroso'),
        ('tope', 'Excede Credito')
    ], string="Estado", default='active', readonly=True)

    @api.onchange('partner_id')
    def _check_partner_status(self):
        if not self.partner_id:
            self.notification_message = False
            return

        Invoice = self.env['account.move']
        Payment = self.env['account.payment']

        # --- 1. Bloqueo por facturas vencidas ---
        nuevo = Invoice.search_count([
            ('partner_id', '=', self.partner_id.id),
            ('move_type', '=', 'out_invoice'),
            ('payment_state', '=', 'not_paid')
        ])
        if nuevo > 0:
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
                return {'warning': {'title': _('Aviso'), 'message': message}}

        pre_total = Invoice.search_count([
            ('partner_id', '=', self.partner_id.id),
            ('move_type', '=', 'out_invoice'),
            ('payment_state', '=', 'not_paid'),
            ('invoice_date_due', '<', fields.Date.today())
        ])
        vencido = Invoice.search([
            ('partner_id', '=', self.partner_id.id),
            ('move_type', '=', 'out_invoice'),
            ('payment_state', '=', 'not_paid')
        ])
        total_deuda = sum(factura.amount_total for factura in vencido)
        if total_deuda > self.partner_id.credit_limit:
            message = _("Este cliente sobrepasó su crédito.")
            self.notification_message = message
            self.estado_partner = 'tope'
            self.state = 'cancel'
            return {'warning': {'title': _('Aviso'), 'message': message}}

        if pre_total > 0:
            message = _("Este cliente tiene facturas vencidas.")
            self.notification_message = message
            self.estado_partner = 'deudor'
            return {'warning': {'title': _('Aviso'), 'message': message}}

        # --- 2. Bloqueo por cheques no cobrados vencidos ---
        cheque_limit = fields.Date.today() - relativedelta(days=7)
        cheques_vencidos = Payment.search_count([
            ('partner_id', '=', self.partner_id.id),
            ('payment_method_line_id.name', 'ilike', 'cheque'),
            ('estado_cheque', '=', 'no_cobrado'),
            ('fecha_cobro', '<=', cheque_limit),
        ])
        if cheques_vencidos > 0:
            message = _("Este cliente tiene cheques no cobrados con más de 7 días desde la fecha de cobro.")
            self.notification_message = message
            self.estado_partner = 'deudor'
            self.state = 'cancel'
            return {'warning': {'title': _('Aviso'), 'message': message}}

        self.estado_partner = 'active'
        self.notification_message = False

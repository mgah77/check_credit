from odoo import models, fields, api, _


class Add_credit(models.Model):
    _inherit = ['account.move']

    notification_message = fields.Char(string="Mensajes", readonly=True)
    credito = fields.Float(string="Credito")
    estado_partner = fields.Selection([('active','Activo'),('deudor','Cliente Moroso'),('tope','Excede Credito')], string="Estado", default='active', readonly=True)

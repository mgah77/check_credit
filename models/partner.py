from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    time_limit = fields.Integer(string='Tiempo para pago en dias', default=False)
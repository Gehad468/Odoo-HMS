from odoo import models, fields
class HMSDepartment(models.Model):
    _name = 'hms.department'

    name = fields.Char()
    is_opened = fields.Boolean()
    capacity = fields.Integer()
    patient_ids=fields.One2many('hms.patient','department_id' )

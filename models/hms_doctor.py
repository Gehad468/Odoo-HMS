from odoo import models, fields
class HMSDoctor(models.Model):
    _name = 'hms.doctors'
    _rec_name = 'firstName'

    firstName = fields.Char(required=True)
    lastName = fields.Char(required=True)
    image = fields.Binary('image')




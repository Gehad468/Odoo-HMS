from odoo import models, fields ,api
from odoo.exceptions import UserError
from odoo.exceptions import  ValidationError

class HMSCustomer(models.Model):
    _inherit= 'res.partner'
    related_patient_id=fields.Many2one('hms.patient')



    def unlink(self):
        if self.related_patient_id:
            raise UserError("You can't delete this patient")
        super().unlink()


    @api.constrains('related_patient_id')
    def _check_related_patient(self):
        for rec in self:
            if rec.related_patient_id:
                existing_customer = self.env['res.partner'].search(
                    [('related_patient_id', '=', rec.related_patient_id.id), ('id', '!=', rec.id)], limit=1)
                if existing_customer:
                    raise ValidationError("Patient is already linked to another customer")

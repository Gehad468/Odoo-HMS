from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import  ValidationError
import re
from datetime import datetime

class PatientLogHistory(models.Model):
    _name = 'hms.patient.log.history'
    _description = 'Patient Log History'

    patient_id = fields.Many2one('hms.patient', string='Patient')
    description = fields.Text()


class HMSPatient(models.Model):
    _name = 'hms.patient'
    _rec_name = 'firstName'

    firstName = fields.Char(required=True)
    lastName = fields.Char(required=True)
    email = fields.Char(string='Email', required=True, unique=True)
    date_birth = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    address = fields.Text()
    age = fields.Integer(compute='_compute_age', store=True)
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string='State', default='undetermined')
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ])
    pcr = fields.Boolean()
    image = fields.Image('Image')
    department_id = fields.Many2one('hms.department')
    doctor = fields.Many2many('hms.doctors', string='Doctors')
    department_capacity = fields.Integer(related='department_id.capacity')
    logs_history = fields.One2many('hms.patient.log.history', 'patient_id')

    def Change_State(self):
        if self.state == 'undetermined':
            self.state = 'good'
        elif self.state == 'good':
            self.state = 'fair'
        elif self.state == 'fair':
            self.state = 'serious'
        else:
            self.state = 'undetermined'

    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'Email must be unique!')
    ]

    @api.constrains('email')
    def check_email(self):
        for rec in self:
            if rec.email and not re.match(r"[^@]+@[^@]+\.[^@]+", rec.email):
                raise ValidationError("Invalid email format")

    @api.depends('date_birth')
    def _compute_age(self):
        today = datetime.today().date()
        for patient in self:
            if patient.date_birth:
                d = relativedelta(today, patient.date_birth)
                patient.age = d.years
            else:
                patient.age = 32

    @api.onchange('age')
    def warning_mess(self):
        for rec in self:
            if rec.age and rec.age < 30 and not rec.pcr:
                rec.pcr = True
                return {
                    'warning': {
                        'title': 'Age Changed',
                        'message': 'PCR has been checked'
                    }
                }

    @api.onchange('state')
    def create_log_history_record(self):
        for rec in self:
            if rec.state:
                vals = {
                    'description': f'State changed to {rec.state}',
                    'patient_id': rec.id
                }
                self.env['hms.patient.log.history'].create(vals)

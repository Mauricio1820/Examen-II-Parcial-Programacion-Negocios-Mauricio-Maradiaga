from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    prestamo_equipo_ids = fields.One2many(
        "unicah.prestamo.equipo", "solicitante_id", string="Préstamos de equipo"
    )
    prestamo_equipo_count = fields.Integer(
        string="Préstamos", compute="_compute_prestamo_equipo_count"
    )

    @api.depends("prestamo_equipo_ids")
    def _compute_prestamo_equipo_count(self):
        for partner in self:
            partner.prestamo_equipo_count = len(partner.prestamo_equipo_ids)

    def action_ver_prestamos_equipo(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Préstamos de equipo",
            "res_model": "unicah.prestamo.equipo",
            "view_mode": "list,form",
            "domain": [("solicitante_id", "=", self.id)],
            "context": {"default_solicitante_id": self.id},
        }

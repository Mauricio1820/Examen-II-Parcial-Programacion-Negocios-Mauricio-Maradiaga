from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class PrestamoEquipo(models.Model):
    _name = "unicah.prestamo.equipo"
    _description = "Préstamo de equipo universitario"
    _rec_name = "nombre_equipo"
    _order = "fecha_prestamo desc, id desc"

    nombre_equipo = fields.Char(string="Equipo / código de inventario", required=True)
    solicitante_id = fields.Many2one(
        "res.partner", string="Solicitante", required=True, ondelete="restrict", index=True
    )
    fecha_prestamo = fields.Date(
        string="Fecha de préstamo", required=True, default=fields.Date.context_today
    )
    fecha_devolucion_prevista = fields.Date(
        string="Devolución prevista",
        required=True,
        default=lambda self: fields.Date.context_today(self) + timedelta(days=7),
    )
    fecha_devolucion_real = fields.Date(
        string="Devolución real", readonly=True, copy=False
    )
    estado = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("prestado", "En préstamo"),
            ("devuelto", "Devuelto"),
        ],
        string="Estado",
        required=True,
        default="borrador",
        readonly=True,
        copy=False,
    )
    dias_prestamo = fields.Integer(
        string="Días autorizados", compute="_compute_dias_prestamo", store=True
    )
    observaciones = fields.Text(string="Observaciones")

    @api.depends("fecha_prestamo", "fecha_devolucion_prevista")
    def _compute_dias_prestamo(self):
        for prestamo in self:
            if prestamo.fecha_prestamo and prestamo.fecha_devolucion_prevista:
                prestamo.dias_prestamo = max(
                    (prestamo.fecha_devolucion_prevista - prestamo.fecha_prestamo).days + 1,
                    0,
                )
            else:
                prestamo.dias_prestamo = 0

    @api.constrains(
        "fecha_prestamo", "fecha_devolucion_prevista", "fecha_devolucion_real", "estado"
    )
    def _check_fechas(self):
        for prestamo in self:
            if (
                prestamo.fecha_prestamo
                and prestamo.fecha_devolucion_prevista
                and prestamo.fecha_devolucion_prevista < prestamo.fecha_prestamo
            ):
                raise ValidationError(
                    "La devolución prevista no puede ser anterior al préstamo."
                )
            if (
                prestamo.fecha_devolucion_real
                and prestamo.fecha_prestamo
                and prestamo.fecha_devolucion_real < prestamo.fecha_prestamo
            ):
                raise ValidationError(
                    "La devolución real no puede ser anterior al préstamo."
                )
            if prestamo.estado == "devuelto" and not prestamo.fecha_devolucion_real:
                raise ValidationError("Un préstamo devuelto debe registrar su fecha de devolución.")
            if prestamo.fecha_devolucion_real and prestamo.estado != "devuelto":
                raise ValidationError(
                    "La fecha de devolución real solo corresponde a un préstamo devuelto."
                )

    def action_entregar(self):
        for prestamo in self:
            if prestamo.estado != "borrador":
                raise UserError("Solo se puede entregar un préstamo en borrador.")
            if prestamo.fecha_prestamo > fields.Date.context_today(prestamo):
                raise UserError("No puede entregar el equipo antes de la fecha de préstamo.")
        self.write({"estado": "prestado"})
        return True

    def action_devolver(self):
        for prestamo in self:
            if prestamo.estado != "prestado":
                raise UserError("Solo se puede devolver un equipo que está en préstamo.")
        self.write(
            {"estado": "devuelto", "fecha_devolucion_real": fields.Date.context_today(self)}
        )
        return True

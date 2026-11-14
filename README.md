# Examen II Parcial - Programación de Negocios

**Nombre:** Mauricio Maradiaga  
**Número de cuenta:** 0801200605500  
**Versión:** Odoo 20.0 Community

El proyecto está separado del código de Odoo y de los ejercicios anteriores. Esta carpeta es la raíz del repositorio del examen.

## Módulos

- `tienda_unicah`: datos universitarios de los clientes, convenios de descuento y su aplicación en ventas.
- `unicah_prestamo_equipos`: propuesta propia para gestionar préstamos de equipo universitario.

## Instalación

Agregar la ruta absoluta de esta carpeta al final de `addons_path` en la configuración propia de Odoo. Con el entorno Python de Odoo activo, ejecutar desde la instalación principal:

```powershell
python odoo-bin -c odoo.conf -i tienda_unicah,unicah_prestamo_equipos --stop-after-init
python odoo-bin -c odoo.conf
```

Para aplicar cambios, detener Odoo con Ctrl+C y actualizar los módulos:

```powershell
python odoo-bin -c odoo.conf -u tienda_unicah,unicah_prestamo_equipos --stop-after-init
python odoo-bin -c odoo.conf
```

No se incluyen el código base de Odoo, la base de datos ni las credenciales del entorno.

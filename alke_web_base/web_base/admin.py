from django.contrib import admin
from .models import Usuario, Contacto, Transaccion

admin.site.register(Usuario)
admin.site.register(Contacto)
admin.site.register(Transaccion)
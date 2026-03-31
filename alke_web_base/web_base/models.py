from django.db import models


class Usuario(models.Model):
    nombre      = models.CharField(max_length=100)
    correo      = models.EmailField(unique=True)
    password    = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=20, default='123456789')
    saldo       = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ultimo_acceso = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.nombre} ({self.correo})'

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Contacto(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='contactos'
    )
    nombre  = models.CharField(max_length=100)
    cbu     = models.CharField(max_length=22, blank=True)
    alias   = models.CharField(max_length=22, blank=True)
    banco   = models.CharField(max_length=50, blank=True)
    correo  = models.EmailField(blank=True)

    def __str__(self):
        return f'{self.nombre} — {self.alias}'

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'


class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('deposito', 'Depósito'),
        ('envio',    'Envío'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='transacciones'
    )
    tipo    = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto   = models.DecimalField(max_digits=12, decimal_places=2)
    detalle = models.CharField(max_length=200, blank=True)
    fecha   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tipo} ${self.monto} — {self.fecha.strftime("%d/%m/%Y")}'

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-fecha']
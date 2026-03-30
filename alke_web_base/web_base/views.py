from django.shortcuts import render, redirect
from .models import Usuario, Contacto, Transaccion


# ── Login ──
def login_view(request):
    error = None

    if request.method == 'POST':
        correo   = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(correo=correo, password=password)
            request.session['usuario_id'] = usuario.id
            return redirect('menu')
        except Usuario.DoesNotExist:
            error = 'Correo o contraseña incorrectos.'

    return render(request, 'login.html', {'error': error})


# ── Menú principal ──
def menu_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)
    context = {
        'nombre_usuario':  usuario.nombre,
        'saldo_actual':    usuario.saldo,
        'numero_cuenta':   usuario.numero_cuenta,
    }
    return render(request, 'menu.html', context)


# ── Depositar ──
def deposit_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        monto = int(request.POST.get('monto', 0))
        if monto > 0:
            # Actualizar saldo con ORM
            usuario.saldo += monto
            usuario.save()

            # Crear transacción con ORM
            Transaccion.objects.create(
                usuario = usuario,
                tipo    = 'deposito',
                monto   = monto,
                detalle = 'Depósito en cuenta'
            )
        return redirect('menu')

    context = {'saldo_actual': usuario.saldo}
    return render(request, 'deposit.html', context)


# ── Agregar contacto ──
def add_contact_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    if request.method == 'POST':
        usuario = Usuario.objects.get(id=usuario_id)
        nombre  = request.POST.get('nombre', '').strip()
        cbu     = request.POST.get('cbu', '').strip()
        alias   = request.POST.get('alias', '').strip()
        banco   = request.POST.get('banco', '').strip()
        correo  = request.POST.get('correo', '').strip()

        if nombre:
            # Crear contacto con ORM
            Contacto.objects.create(
                usuario = usuario,
                nombre  = nombre,
                cbu     = cbu,
                alias   = alias,
                banco   = banco,
                correo  = correo
            )

    return redirect('send_money')


# ── Enviar Dinero ──
def send_money_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario   = Usuario.objects.get(id=usuario_id)
    # Leer contactos con ORM
    contactos = Contacto.objects.filter(usuario=usuario)
    error     = None

    if request.method == 'POST':
        monto         = int(request.POST.get('monto', 0))
        contacto_nombre = request.POST.get('contacto', '').strip()

        if not contacto_nombre:
            error = 'Debes seleccionar un contacto.'
        elif monto <= 0:
            error = 'El monto debe ser mayor a 0.'
        elif monto > usuario.saldo:
            error = 'Saldo insuficiente.'
        else:
            # Actualizar saldo con ORM
            usuario.saldo -= monto
            usuario.save()

            # Crear transacción con ORM
            Transaccion.objects.create(
                usuario = usuario,
                tipo    = 'envio',
                monto   = monto,
                detalle = f'Enviado a {contacto_nombre}'
            )
            return redirect('menu')

    context = {
        'saldo_actual': usuario.saldo,
        'contactos':    contactos,
        'error':        error
    }
    return render(request, 'sendmoney.html', context)

# ── Eliminar contacto ──
def delete_contact_view(request, contacto_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    try:
        contacto = Contacto.objects.get(id=contacto_id, usuario_id=usuario_id)
        contacto.delete()
    except Contacto.DoesNotExist:
        pass

    return redirect('send_money')

# ── Transacciones ──
def transactions_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario      = Usuario.objects.get(id=usuario_id)
    # Leer transacciones con ORM ordenadas por fecha
    transacciones = Transaccion.objects.filter(usuario=usuario)

    # Formatear para el template
    movimientos = []
    for t in transacciones:
        signo = '+' if t.tipo == 'deposito' else '-'
        movimientos.append({
            'fecha':   t.fecha.strftime('%d/%m/%Y %H:%M'),
            'tipo':    t.get_tipo_display(),
            'detalle': t.detalle,
            'monto':   f'{signo}${int(t.monto):,}'.replace(',', '.')
        })

    context = {'movimientos': movimientos}
    return render(request, 'transactions.html', context)
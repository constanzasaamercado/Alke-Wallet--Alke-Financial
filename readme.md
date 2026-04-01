# Alke Wallet 💳

Aplicación web de billetera digital desarrollada con **Python** y **Django** como proyecto del **Módulo 7 — Integración con Bases de Datos** del curso de Desarrollo de Aplicaciones Web con Python Django, para la empresa fintech **Alke Financial**.

---

## Descripción

Alke Wallet es una simulación de billetera digital que permite a los usuarios registrarse, gestionar su cuenta, depositar dinero, enviar transferencias a contactos y consultar el historial de movimientos. Los datos se persisten en una base de datos relacional SQLite mediante el ORM de Django, garantizando integridad y consistencia de la información.

---

## Objetivo del proyecto

Desarrollar una aplicación web funcional que permita almacenar, consultar y gestionar información persistente mediante el uso del ORM de Django, aplicando migraciones y operaciones CRUD, garantizando la integridad y consistencia de los datos.

---

## Funcionalidades

| Módulo | Descripción |
|---|---|
| **Registro** | Creación de cuenta con generación automática de número de cuenta |
| **Login** | Autenticación de usuario con correo y contraseña |
| **Menú principal** | Vista del saldo actual, número de cuenta y último acceso |
| **Depositar** | Incrementa el saldo de la cuenta y registra el movimiento en la BD |
| **Transferencias** | Envío de dinero a contactos con validación de saldo |
| **Agregar contacto** | Alta de nuevos destinatarios (nombre, CBU, alias, banco, correo) |
| **Eliminar contacto** | Baja de contactos con confirmación visual |
| **Movimientos** | Historial cronológico de depósitos y envíos desde la BD |
| **Último acceso** | Registro dinámico de la última sesión iniciada |

---

## Modelos de datos y relaciones

### `Usuario`
| Campo | Tipo | Descripción |
|---|---|---|
| `nombre` | CharField | Nombre completo |
| `correo` | EmailField (unique) | Correo electrónico |
| `password` | CharField | Contraseña |
| `numero_cuenta` | CharField | Número de cuenta generado automáticamente |
| `saldo` | DecimalField | Saldo disponible |
| `ultimo_acceso` | DateTimeField | Fecha y hora del último login |

### `Contacto`
| Campo | Tipo | Descripción |
|---|---|---|
| `usuario` | ForeignKey → Usuario | Relación con el usuario dueño |
| `nombre` | CharField | Nombre del contacto |
| `cbu` | CharField | CBU bancario |
| `alias` | CharField | Alias de transferencia |
| `banco` | CharField | Nombre del banco |
| `correo` | EmailField | Correo del contacto |

### `Transaccion`
| Campo | Tipo | Descripción |
|---|---|---|
| `usuario` | ForeignKey → Usuario | Relación con el usuario que realizó la operación |
| `tipo` | CharField (choices) | `deposito` o `envio` |
| `monto` | DecimalField | Monto de la operación |
| `detalle` | CharField | Descripción de la operación |
| `fecha` | DateTimeField (auto) | Fecha y hora de la transacción |

### Relaciones
- `Usuario` → `Contacto`: **uno a muchos** (`related_name='contactos'`)
- `Usuario` → `Transaccion`: **uno a muchos** (`related_name='transacciones'`)

---

## Operaciones CRUD implementadas

| Operación | Descripción | Vista |
|---|---|---|
| **Create** | Registro de usuario nuevo | `register_view` |
| **Create** | Depósito → nueva transacción | `deposit_view` |
| **Create** | Agregar contacto | `add_contact_view` |
| **Create** | Envío → nueva transacción | `send_money_view` |
| **Read** | Login: buscar usuario por correo y contraseña | `login_view` |
| **Read** | Listar contactos del usuario | `send_money_view` |
| **Read** | Listar transacciones del usuario | `transactions_view` |
| **Update** | Actualizar saldo al depositar o enviar | `deposit_view` / `send_money_view` |
| **Update** | Registrar último acceso | `login_view` |
| **Delete** | Eliminar contacto | `delete_contact_view` |

---

## Migraciones

```bash
# Generar migraciones a partir de los modelos
python manage.py makemigrations

# Aplicar migraciones a la base de datos
python manage.py migrate

---


#Tecnologías

Python 3.14
Django 6.0.3
SQLite 3 (base de datos por defecto)
Bootstrap 5.3 (UI y componentes)
Bootstrap Icons (iconografía)
HTML5 / CSS3 / JavaScript

# Estructura del proyecto

alke_web_base/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── alke_solutions/              # Configuración principal del proyecto
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── web_base/                    # Aplicación principal
│   ├── models.py                # Modelos: Usuario, Contacto, Transaccion
│   ├── views.py                 # Lógica de todas las vistas (CRUD con ORM)
│   ├── urls.py                  # Rutas de la aplicación
│   ├── admin.py
│   ├── migrations/              # Migraciones generadas
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── register.html
│       ├── menu.html
│       ├── deposit.html
│       ├── sendmoney.html
│       └── transactions.html
├── static/
│   ├── css/
│   │   ├── styles.css
│   │   ├── menu.css
│   │   ├── deposit.css
│   │   └── transactions.css
│   ├── javascript/
│   │   ├── login.js
│   │   ├── menu.js
│   │   ├── deposit.js
│   │   ├── sendmoney.js
│   │   ├── transactions.js
│   │   └── utils.js
│   └── recursos/
│       └── Logo-Alke-Wallet.svg
└── env/                         # Entorno virtual Python

## Instalación y ejecución

1. Clonar el repositorio
git clone <url-del-repositorio>
cd alke_web_base

2. Crear y activar el entorno virtual

python -m venv env

# Windows
env\Scripts\activate

# macOS / Linux
source env/bin/activate

3. Instalar dependencias

pip install django==6.0.3

4. Aplicar migraciones

python manage.py makemigrations
python manage.py migrate

5. (Opcional) Crear datos de prueba desde el shell

python manage.py shell

from web_base.models import Usuario
Usuario.objects.create(
    nombre='Usuario Demo',
    correo='demo@alkewallet.com',
    password='12345',
    numero_cuenta='000123456789',
    saldo=50000
)

6. Iniciar el servidor de desarrollo

python manage.py runserver

La aplicación estará disponible en http://127.0.0.1:8000/

---

## Rutas disponibles

| URL | Vista | Descripción |
|---|---|---|
| `/` | `login_view` | Inicio de sesión |
| `/register/` | `register_view` | Registro de nuevo usuario |
| `/menu/` | `menu_view` | Panel principal |
| `/deposit/` | `deposit_view` | Formulario de depósito |
| `/send-money/` | `send_money_view` | Transferencia a contactos |
| `/add-contact/` | `add_contact_view` | Alta de contacto |
| `/delete-contact/<id>/` | `delete_contact_view` | Baja de contacto |
| `/transactions/` | `transactions_view` | Historial de movimientos |
| `/logout/` | `logout_view` | Cerrar sesión |

---
## Notas

El proyecto usa DEBUG = True. No usar en producción sin configurar ALLOWED_HOSTS y cambiar la SECRET_KEY.

Las contraseñas se almacenan en texto plano únicamente con fines demostrativos. En producción se debe usar el sistema de autenticación de Django con hashing.

Autor

Constanza Fernanda Saa Mercado

Desarrollado como proyecto final del Módulo 7 — Acceso a Datos en Aplicaciones Python Django

Curso: Desarrollo de Aplicaciones Web con Python Django — Alke Financial
# 🏦 Prueba técnica Cobros simulados
Este proyecto implementa una **API REST** para la gestión de clientes, tarjetas de prueba y cobros simulados con reembolsos, usando **FastAPI** y **MongoDB**.

La API permite:

- CRUD completo de clientes.
- CRUD de tarjetas de clientes (con validación Luhn).
- Cobros simulados aprobados o rechazados según reglas definidas.
- Reembolsos de cobros y consulta del historial completo.

Se prioriza la **seguridad de datos**, evitando exponer PAN completos, y se incluyen pruebas unitarias para asegurar consistencia.

---

## 📚 Tabla de Contenidos

1. [Tecnologías](#-tecnologías)
2. [Requisitos](#-requisitos)
3. [Instalación y Ejecución](#-instalación-y-ejecución)
4. [Pruebas Unitarias](#-pruebas-unitarias)

---

## 🛠 Tecnologías

- Python 3.13
- FastAPI 0.119
- MongoDB / pymongo 
- Pytest 8.4
- Docker & Docker Compose
- Pydantic 2.12 (para validación de DTOs)

---

## ⚙️ Requisitos

- [Python 3.13+](https://www.python.org/downloads/)
- [Docker y Docker Compose](https://www.docker.com/products/docker-desktop/)
- Postman (opcional para importar la colección de pruebas)

---

## 🚀 Instalación y Ejecución
    docker-compose up --build
## Servidor
La API estará disponible en http://127.0.0.1:8000

Documentación Swagger en http://127.0.0.1:8000/docs

La colección de Postman y el historial de cobros de prueba están incluidos en la imagen y pueden descargarse desde los endpoints de la API o desde el contenedor.
### Tarjetas de prueba
| Banco   | PAN (solo pruebas) | Últimos 4 | Expiración |
| ------- | ------------------ | --------- | ---------- |
| Banco A | 4507990000004905   | 4905      | 12/2030    |
| Banco B | 4532750000001234   | 1234      | 06/2031    |
| Banco C | 4916320000005678   | 5678      | 09/2029    |

⚖️ Reglas de Cobro

Monto máximo permitido: 10,000.0

Validación del last4 de la tarjeta

Estado de la tarjeta: activa

Solo se permiten cobros aprobados si cumplen las reglas

Reembolsos actualizan is_refunded=True y refund_date

### 🧪 Pruebas Unitarias

Incluye pruebas con Pytest para validar:

- Validación Luhn de tarjetas.

- CRUD completo de clientes y tarjetas.

- Cobros simulados aprobados y rechazados según reglas.

- Reembolsos de cobros.

- Consulta de historial de cobros con estado de reembolso.

- Ejecutar pruebas:  docker-compose run --rm api pytest --disable-warnings -v



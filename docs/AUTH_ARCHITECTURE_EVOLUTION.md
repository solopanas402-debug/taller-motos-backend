# Arquitectura de Autenticación: Evolución y Decisiones Técnicas
## Proyecto: Taller Motos Backend (AWS SAM + Python 3.11 + Cognito + Supabase)

Este documento detalla la transición del sistema de autenticación desde un modelo manual basado en base de datos local hacia una arquitectura empresarial gestionada con **AWS Cognito**.

---

## 1. El Problema Original (Legacy)
Al inicio del proyecto, la identidad de los usuarios se gestionaba directamente en la tabla `users` de Supabase.

*   **Identificación Insegura**: Las contraseñas se guardaban en texto plano o con hashes `bcrypt`.
*   **Riesgo Legal**: El negocio era el responsable absoluto de la seguridad de las claves. Una filtración de la base de datos comprometía todo el acceso.
*   **Falta de Estándares**: El sistema no manejaba de forma nativa flujos como:
    *   Expiración automática de sesiones.
    *   Refresh Tokens (para mantener la App abierta de forma segura).
    *   Recuperación de contraseña vía email.
    *   Detección de ataques de fuerza bruta.

---

## 2. La Nueva Arquitectura (AWS Cognito + Supabase)
Hemos migrado a un modelo de **Responsabilidad Compartida**:
*   **Seguridad**: AWS Cognito actúa como la "Caja Fuerte" (IdP), encargado de las contraseñas y los tokens.
*   **Negocio**: Supabase actúa como el "Directorio", encargado de los roles, nombres y estado de los empleados.

### El Campo `cognito_sub`
Es el puente inmutable. No usamos el `email` para vincular sistemas porque el email puede cambiar; el `sub` (Subject) de Cognito es un UUID único que nunca cambia y sirve de Clave Foránea en Supabase.

### El Estado `COGNITO_MANAGED`
En la tabla de usuarios, el campo `password` ahora muestra `COGNITO_MANAGED` para indicar que esa credencial ya no reside en nuestra base de datos, sino en los servidores de alta seguridad de Amazon.

---

## 3. Desafíos Técnicos y Soluciones (Log de Errores)

Durante la implementación, enfrentamos y resolvimos los siguientes obstáculos:

| Error | Descripción | Solución Técnica |
| :--- | :--- | :--- |
| `ResourceNotFound` | Cognito no era detectado por las Lambdas. | Estandarización de IDs en `locals.json`. |
| `Rollback Sync` | Usuarios creados en un sistema pero no en el otro. | Implementación de **Atomicidad Manual**: Si Supabase falla, la Lambda borra automáticamente el usuario de Cognito. |
| `42501 (RLS)` | Bloqueo de seguridad de Supabase al insertar. | Uso de la clave **`service_role`** (admin) en lugar de la `public` key en el backend. |
| `23502 (Not Null)` | La DB exigía `password` pero no la enviamos. | Se cambió la columna a **Nullable** en Supabase, delegando la clave a AWS. |

---

## 4. Estrategia de App Clients (Doble Puerta)
Para cumplir con las mejores prácticas de seguridad, configuramos **dos clientes** en Cognito:

1.  **Cliente de Sistema (Con Secreto)**:
    *   Uso: Scripts internos y comunicación entre servicios.
    *   Flujo: `client_credentials`.
2.  **Cliente de Aplicación (Sin Secreto)**:
    *   Uso: App móvil/web para mecánicos y administradores.
    *   Flujo: `ALLOW_USER_PASSWORD_AUTH`.
    *   **Razón**: El frontend no puede ocultar un secreto; por tanto, este cliente está diseñado para ser seguro en ambientes públicos.

---

## 5. Flujos Lógicos Implementados

### Registro (`/auth/register`)
`AdminCreateUser (Cognito)` → `AdminSetPassword (Confirmación)` → `Insert (Supabase)` → `[Rollback si falla]`

### Inicio de Sesión (`/auth/login`)
`AdminInitiateAuth (Cognito)` → `Validation (JWT)` → `Fetch Perfil (Supabase con cognito_sub)` → `Return Combined Identity`

---

## 6. Recomendaciones de Seguridad Futura
*   **MFA**: Se puede activar en Cognito el Doble Factor de Autenticación sin tocar el código.
*   **Migración**: Los usuarios antiguos con `bcrypt` deben resetear su clave para ser migrados automáticamente a Cognito en su primer ingreso.
*   **Costo**: Aprovechar que los primeros **50,000 Usuarios Activos Mensuales (MAU)** en Cognito son **Gratis**.

---
**Documentación técnica generada el 08 de Marzo de 2026.**

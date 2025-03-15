# Sistema de Hospital MVC

## Integrantes y Participación

| Nombre - Matrícula | Participación |
|------|--------------|
| [Iker Rolando Casillas Parra - A01641047] | • Implementación de cita, medico y paciente |
| [Diego Alejandro Calvario Aceves - A01642806] | • Implementación de usuario, administrador y enfermera |
| [Diego Rodríguez Romero - A01741413] | • Creación de todas las vistas del sistema |

## Descripción del Proyecto

Este proyecto implementa un sistema de gestión hospitalaria basado en la arquitectura MVC (Modelo-Vista-Controlador), desarrollado a partir del diagrama UML. El sistema permite la gestión de citas médicas, usuarios del hospital y sus diferentes roles.

## Credenciales para acceso

 - Médico
    - medico1
    - id -> 3
    - rol -> médico

 - Paciente
    - paciente1
    - id -> 1
    - rol -> paciente

 - Enfermera
    - enfermera1
    - id -> 2
    - rol -> enfermera

## Arquitectura del Sistema

### Modelo
El modelo gestiona los datos, la lógica y las reglas de la aplicación. En este sistema, los modelos principales son:

- **Cita**: Almacena información sobre las citas médicas con atributos como fecha, hora, motivo y estado.
- **Usuario**: Clase base que contiene información común para todos los usuarios del sistema como id, nombre y rol.

### Vista
La vista es responsable de la interfaz de usuario, permitiendo a los diferentes tipos de usuarios interactuar con el sistema según sus roles y permisos.

### Controlador
El controlador actúa como intermediario entre el modelo y la vista, procesando las solicitudes del usuario y manipulando los datos según sea necesario.

## Diagrama UML

El sistema está estructurado según el siguiente diagrama UML:

### Clases Principales:

1. **Cita**
   - Atributos: fecha (String), hora (String), motivo (String), estado (String)
   - Relaciones: Una cita está asociada a un paciente (1) y a un médico (1)

2. **Usuario** (Clase base)
   - Atributos: id (String, privado), nombre (String), rol (String)
   - Subclases: Médico, Paciente, Enfermera, Administrador

3. **Médico** (Extiende Usuario)
   - Métodos: verCitas(), confirmarCita(), actualizarCita()
   - Relaciones: Un médico puede tener múltiples citas (1..*)

4. **Paciente** (Extiende Usuario)
   - Métodos: agendarCita(), verCitas()
   - Relaciones: Un paciente puede tener múltiples citas (1..*)

5. **Enfermera** (Extiende Usuario)
   - Métodos: actualizarEstadoCita(), registrarSignosVitales(), asistirMedico()

6. **Administrador** (Extiende Usuario)
   - Métodos: visualizarCitas(), gestionarHorarios()

## Funcionalidades del Sistema

### Para Pacientes
- Agendar citas médicas
- Ver historial de citas

### Para Médicos
- Consultar lista de citas
- Confirmar citas
- Actualizar información de citas

### Para Enfermeras
- Actualizar el estado de las citas
- Registrar signos vitales de pacientes
- Asistir a los médicos

### Para Administradores
- Visualizar todas las citas del sistema
- Gestionar horarios de personal médico

![image](https://github.com/user-attachments/assets/aa8d45db-5f8b-440d-8c5a-75fcd6273a3e)


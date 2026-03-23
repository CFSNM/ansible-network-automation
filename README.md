# 🔴 Laboratorio OSPF Cisco — Automatización con Ansible

## Descripción General

Este laboratorio implementa una topología de red multi-área OSPF usando exclusivamente routers **Cisco IOS (C7200)** emulados en GNS3. El objetivo es desplegar y verificar la configuración OSPF de forma automática mediante playbooks de Ansible, utilizando la colección `cisco.ios`.

---

## Topología de Red

```
                   Nodo Gestión Ansible (Ubuntu VM)
                       |
               [Management-SW]  192.168.100.0/24
              /    |    |    \    \    \
           R1    R2    R3    R4   R5   R6
        .1   .2     .3    .4    .5   .6

 ┌──────────────────────────────────────────────────────────┐
 │                   OSPF Area 0 (Backbone)                  │
 │                                                           │
 │   R1 ──(Gi0/0)10.0.12.0/30(Gi0/0)── R2                  │
 │    \                                   /                  │
 │  Gi2/0                             Gi2/0                  │
 │  10.0.13.0/30                  10.0.23.0/30               │
 │     \                              /                      │
 │   Gi0/0\                      /Gi4/0                      │
 │          └──── R3 (ABR) ─────┘  (Area 0/10/20)           │
 └──────────────┬──────────────────────────────-─────────────┘
                │ R3
        Gi1/0   │   Gi2/0
    10.0.34.0/30│       │10.0.36.0/30
                │       │
 ┌──────────────▼──┐  ┌─▼────────────────┐
 │  OSPF Area 10   │  │  OSPF Area 20    │
 │                 │  │                  │
 │  R4 (Gi0/0)     │  │  R6 (Gi0/0)      │
 │      |          │  │      |           │
 │   Gi2/0         │  │   Gi2/0          │
 │  10.0.45.0/30   │  │  10.0.56.0/30    │
 │      |          │  │      |           │
 │  R5 (Gi0/0)─────────────(Gi2/0) R5   │
 └─────────────────┘  └──────────────────┘
```

> **Nota sobre interfaces:** El adaptador `C7200-IO-GE-E` (slot0) en GNS3 solo
> expone un puerto (Gi0/0). Los segundos enlaces de cada router usan adaptadores
> PA-GE en slots adicionales, resultando en Gi2/0 (slot2) para R1, R2, R4, R5, R6
> y Gi4/0 (slot4) para el segundo enlace de R3.

---

## Inventario de Nodos

| Nombre        | Plataforma    | IP Gestión      | Router-ID | Rol OSPF               | Puerto Consola |
|---------------|---------------|-----------------|-----------|------------------------|----------------|
| R1-CISCO      | Cisco C7200   | 192.168.100.1   | 1.1.1.1   | Internal — Area 0      | 5001           |
| R2-CISCO      | Cisco C7200   | 192.168.100.2   | 2.2.2.2   | Internal — Area 0      | 5002           |
| R3-CISCO      | Cisco C7200   | 192.168.100.3   | 3.3.3.3   | **ABR** (Area 0/10/20) | 5003           |
| R4-CISCO      | Cisco C7200   | 192.168.100.4   | 4.4.4.4   | Internal — Area 10     | 5004           |
| R5-CISCO      | Cisco C7200   | 192.168.100.5   | 5.5.5.5   | **ABR** (Area 10/20)  | 5005           |
| R6-CISCO      | Cisco C7200   | 192.168.100.6   | 6.6.6.6   | Internal — Area 20     | 5006           |
| Management-SW | Ethernet Switch | —             | —         | Infraestructura        | —              |
| Nodo Gestión Ansible     | Ubuntu 24.04  | —               | —         | Infraestructura       | —              |

---

## Tabla de Interfaces y Direccionamiento

### R1-CISCO (Router ID: 1.1.1.1)

| Interfaz GNS3       | Conecta a           | Red              | Área OSPF |
|---------------------|---------------------|------------------|-----------|
| GigabitEthernet0/0  | R2-CISCO Gi0/0      | 10.0.12.1/30     | 0         |
| GigabitEthernet2/0  | R3-CISCO Gi0/0      | 10.0.13.1/30     | 0         |
| GigabitEthernet1/0  | Management-SW       | 192.168.100.1/24 | —         |

### R2-CISCO (Router ID: 2.2.2.2)

| Interfaz GNS3       | Conecta a           | Red              | Área OSPF |
|---------------------|---------------------|------------------|-----------|
| GigabitEthernet0/0  | R1-CISCO Gi0/0      | 10.0.12.2/30     | 0         |
| GigabitEthernet2/0  | R3-CISCO Gi4/0      | 10.0.23.1/30     | 0         |
| GigabitEthernet1/0  | Management-SW       | 192.168.100.2/24 | —         |

### R3-CISCO — ABR (Router ID: 3.3.3.3)

| Interfaz GNS3       | Conecta a           | Red              | Área OSPF |
|---------------------|---------------------|------------------|-----------|
| GigabitEthernet0/0  | R1-CISCO Gi2/0      | 10.0.13.2/30     | 0         |
| GigabitEthernet4/0  | R2-CISCO Gi2/0      | 10.0.23.2/30     | 0         |
| GigabitEthernet1/0  | R4-CISCO Gi0/0      | 10.0.34.1/30     | 10        |
| GigabitEthernet2/0  | R6-CISCO Gi0/0      | 10.0.36.1/30     | 20        |
| GigabitEthernet3/0  | Management-SW       | 192.168.100.3/24 | —         |

### R4-CISCO (Router ID: 4.4.4.4)

| Interfaz GNS3       | Conecta a           | Red              | Área OSPF |
|---------------------|---------------------|------------------|-----------|
| GigabitEthernet0/0  | R3-CISCO Gi1/0      | 10.0.34.2/30     | 10        |
| GigabitEthernet2/0  | R5-CISCO Gi0/0      | 10.0.45.1/30     | 10        |
| GigabitEthernet1/0  | Management-SW       | 192.168.100.4/24 | —         |

### R5-CISCO — ABR (Router ID: 5.5.5.5)

| Interfaz GNS3       | Conecta a           | Red              | Área OSPF |
|---------------------|---------------------|------------------|-----------|
| GigabitEthernet0/0  | R4-CISCO Gi2/0      | 10.0.45.2/30     | 10        |
| GigabitEthernet2/0  | R6-CISCO Gi2/0      | 10.0.56.1/30     | 20        |
| GigabitEthernet1/0  | Management-SW       | 192.168.100.5/24 | —         |

### R6-CISCO — Internal Area 20 (Router ID: 6.6.6.6)

| Interfaz GNS3       | Conecta a           | Red              | Área OSPF |
|---------------------|---------------------|------------------|-----------|
| GigabitEthernet0/0  | R3-CISCO Gi2/0      | 10.0.36.2/30     | 20        |
| GigabitEthernet2/0  | R5-CISCO Gi2/0      | 10.0.56.2/30     | 20        |
| GigabitEthernet1/0  | Management-SW       | 192.168.100.6/24 | —         |

---

## Requisitos de Hardware GNS3

### Imagen Cisco IOS

| Parámetro  | Valor                                          |
|------------|------------------------------------------------|
| Imagen     | `c7200-advipservicesk9-mz.152-4.S5.image`      |
| Plataforma | Cisco 7200 (Dynamips)                          |
| RAM        | 512 MB                                         |
| NPE        | npe-400                                        |
| Slot 0     | C7200-IO-GE-E (1 × GigabitEthernet — Gi0/0)   |
| Slot 1     | PA-GE (Gi1/0 — gestión)                        |
| Slot 2     | PA-GE (Gi2/0 — segundo enlace OSPF, R1/R2/R4/R5/R6) |
| Slot 3     | PA-GE (Gi3/0 — gestión R3)                     |
| Slot 4     | PA-GE (Gi4/0 — segundo enlace OSPF, solo R3)   |
| idlepc     | 0x62cc930c                                     |

### Recursos del Host

| Recurso      | Mínimo | Recomendado |
|--------------|--------|-------------|
| RAM total    | 6 GB   | 8 GB        |
| CPU cores    | 2      | 4           |
| Disco        | 2 GB   | 5 GB        |
| GNS3 versión | 2.2.x  | 2.2.33+     |

---

## Requisitos de Software

```bash
# Ansible y colecciones
pip install ansible
ansible-galaxy collection install cisco.ios
ansible-galaxy collection install ansible.netcommon
ansible-galaxy collection install ansible.utils

# Verificar versiones
ansible --version
ansible-galaxy collection list cisco.ios
```

---

## Configuración Inicial de los Routers

La startup-config de cada router ya está preconfigurada en GNS3 con:
- Hostname, usuario `ansible`, SSH v2
- Direcciones IP en todas las interfaces según la tabla anterior
- Ruta de gestión `0.0.0.0/0 → 192.168.100.254`

Para conectarse por consola directamente:

```bash
telnet localhost 5001   # R1-CISCO
telnet localhost 5002   # R2-CISCO
telnet localhost 5003   # R3-CISCO
telnet localhost 5004   # R4-CISCO
telnet localhost 5005   # R5-CISCO
telnet localhost 5006   # R6-CISCO
```

---

## Verificación de Conectividad

```bash
# Ping a todos los routers desde el host Ansible
for i in 1 2 3 4 5 6; do
  echo -n "R${i} (192.168.100.${i}): "
  ping -c 1 -W 1 192.168.100.${i} &>/dev/null && echo "OK" || echo "FAIL"
done

# Verificar SSH (ejemplo R1)
ssh -o StrictHostKeyChecking=no ansible@192.168.100.1 "show version | inc Version"
```

---

## Estructura del Proyecto Ansible

```
ospf-cisco-lab-ansible/
├── ansible.cfg
├── inventory/
│   ├── hosts.yml                   # IPs, ospf_interfaces, ospf_networks, interfaces_config
│   └── group_vars/
│       ├── all.yml                 # Credenciales y conexión
│       └── cisco_routers.yml       # process_id, mgmt_interface, gateway, domain
├── playbooks/
│   ├── base_config.yml             # Rol cisco_base
│   ├── ospf_deploy.yml             # Rol cisco_ospf
│   ├── ospf_verify.yml             # Verificación con ios_facts + asserts
│   └── full_deploy.yml             # Despliegue completo con pre/post facts
└── roles/
    ├── cisco_base/
    └── cisco_ospf/
```

---

## Ejecución Rápida

```bash
cd ospf-cisco-lab-ansible/

# 1. Verificar conectividad
ansible all -m ping

# 2. Configuración base (interfaces, SSH, usuario)
ansible-playbook playbooks/base_config.yml

# 3. Desplegar OSPF
ansible-playbook playbooks/ospf_deploy.yml

# 4. Verificar convergencia
ansible-playbook playbooks/ospf_verify.yml

# O todo en uno:
ansible-playbook playbooks/full_deploy.yml
```

---

## Credenciales

```yaml
usuario:    ansible
contraseña: Ansible123
enable:     Ansible123
```

> ⚠️ Cambiar en producción. Usar `ansible-vault` para proteger credenciales sensibles.

---

## Verificación OSPF (comandos Cisco)

```cisco
! Ver vecinos OSPF
show ip ospf neighbor

! Ver tabla de rutas OSPF
show ip route ospf

! Ver base de datos OSPF
show ip ospf database

! Ver resumen de interfaces OSPF
show ip ospf interface brief

! Verificar conectividad extremo a extremo desde R1 hacia Area 20
ping 10.0.56.1
ping 10.0.56.2
ping 10.0.36.2
```

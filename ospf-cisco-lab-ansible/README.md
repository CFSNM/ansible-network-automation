# Proyecto Ansible — OSPF Cisco

---

## Topología de Red

```
                   Cloud (NAT)
                       |
               [Management-SW]  192.168.100.0/24
              /    |    |    \    \    \
           R1    R2    R3    R4   R5   R6
        .1   .2     .3    .4    .5   .6

 ┌──────────────────────────────────────────────────────────┐
 │                   OSPF Area 0 (Backbone)                  │
 │                                                           │
 │   R1 ──10.0.12.0/30(Gi0/0)── R2                         │
 │    \                            /                         │
 │  Gi2/0                       Gi2/0                       │
 │  10.0.13.0/30             10.0.23.0/30                    │
 │     \                        /                            │
 │      └────── R3 (ABR) ──────┘                             │
 │          Gi0/0    Gi4/0                                    │
 └──────────────┬──────────────────────────────-─────────────┘
                │ R3
        Gi1/0   │   Gi2/0
    10.0.34.0/30│       │10.0.36.0/30
                │       │
 ┌──────────────▼──┐  ┌─▼────────────────┐
 │  OSPF Area 10   │  │  OSPF Area 20    │
 │                 │  │                  │
 │  R4 (Gi0/0)     │  │  R6 (Gi0/0)      │
 │   |             │  │   |              │
 │  Gi2/0          │  │  Gi2/0           │
 │  10.0.45.0/30   │  │  10.0.56.0/30    │
 │   |             │  │   |              │
 │  R5 (Gi0/0)────────────(Gi2/0) R5    │
 └─────────────────┘  └──────────────────┘
```

---

## Inventario de Nodos

| Nombre   | IP Gestión      | Router-ID | Rol OSPF            | Consola |
|----------|-----------------|-----------|---------------------|---------|
| R1-CISCO | 192.168.100.1   | 1.1.1.1   | Internal — Area 0   | 5001    |
| R2-CISCO | 192.168.100.2   | 2.2.2.2   | Internal — Area 0   | 5002    |
| R3-CISCO | 192.168.100.3   | 3.3.3.3   | ABR (Area 0/10/20)  | 5003    |
| R4-CISCO | 192.168.100.4   | 4.4.4.4   | Internal — Area 10  | 5004    |
| R5-CISCO | 192.168.100.5   | 5.5.5.5   | **ABR** (Area 10/20)| 5005  |
| R6-CISCO | 192.168.100.6   | 6.6.6.6   | Internal — Area 20  | 5006    |

---

## Tabla de Interfaces y Direccionamiento

> **Nota:** El adaptador `C7200-IO-GE-E` (slot0) solo expone un puerto (Gi0/0).
> Los segundos enlaces usan adaptadores PA-GE en slots adicionales (Gi2/0, Gi4/0).

### R1-CISCO (Router ID: 1.1.1.1)

| Interfaz GNS3       | Conecta a           | Red             | Área OSPF |
|---------------------|---------------------|-----------------|-----------|
| GigabitEthernet0/0  | R2-CISCO Gi0/0      | 10.0.12.1/30    | 0         |
| GigabitEthernet2/0  | R3-CISCO Gi0/0      | 10.0.13.1/30    | 0         |
| GigabitEthernet1/0  | Management-SW       | 192.168.100.1/24| —         |

### R2-CISCO (Router ID: 2.2.2.2)

| Interfaz GNS3       | Conecta a           | Red             | Área OSPF |
|---------------------|---------------------|-----------------|-----------|
| GigabitEthernet0/0  | R1-CISCO Gi0/0      | 10.0.12.2/30    | 0         |
| GigabitEthernet2/0  | R3-CISCO Gi4/0      | 10.0.23.1/30    | 0         |
| GigabitEthernet1/0  | Management-SW       | 192.168.100.2/24| —         |

### R3-CISCO — ABR (Router ID: 3.3.3.3)

| Interfaz GNS3       | Conecta a           | Red             | Área OSPF |
|---------------------|---------------------|-----------------|-----------|
| GigabitEthernet0/0  | R1-CISCO Gi2/0      | 10.0.13.2/30    | 0         |
| GigabitEthernet4/0  | R2-CISCO Gi2/0      | 10.0.23.2/30    | 0         |
| GigabitEthernet1/0  | R4-CISCO Gi0/0      | 10.0.34.1/30    | 10        |
| GigabitEthernet2/0  | R6-CISCO Gi0/0      | 10.0.36.1/30    | 20        |
| GigabitEthernet3/0  | Management-SW       | 192.168.100.3/24| —         |

### R4-CISCO (Router ID: 4.4.4.4)

| Interfaz GNS3       | Conecta a           | Red             | Área OSPF |
|---------------------|---------------------|-----------------|-----------|
| GigabitEthernet0/0  | R3-CISCO Gi1/0      | 10.0.34.2/30    | 10        |
| GigabitEthernet2/0  | R5-CISCO Gi0/0      | 10.0.45.1/30    | 10        |
| GigabitEthernet1/0  | Management-SW       | 192.168.100.4/24| —         |

### R5-CISCO — ABR (Router ID: 5.5.5.5)

| Interfaz GNS3       | Conecta a           | Red             | Área OSPF |
|---------------------|---------------------|-----------------|-----------|
| GigabitEthernet0/0  | R4-CISCO Gi2/0      | 10.0.45.2/30    | 10        |
| GigabitEthernet2/0  | R6-CISCO Gi2/0      | 10.0.56.1/30    | 20        |
| GigabitEthernet1/0  | Management-SW       | 192.168.100.5/24| —         |

### R6-CISCO — Internal Area 20 (Router ID: 6.6.6.6)

| Interfaz GNS3       | Conecta a           | Red             | Área OSPF |
|---------------------|---------------------|-----------------|-----------|
| GigabitEthernet0/0  | R3-CISCO Gi2/0      | 10.0.36.2/30    | 20        |
| GigabitEthernet2/0  | R5-CISCO Gi2/0      | 10.0.56.2/30    | 20        |
| GigabitEthernet1/0  | Management-SW       | 192.168.100.6/24| —         |

---

## Módulos utilizados

### cisco_base (rol)

| Módulo                        | Propósito                                          |
|-------------------------------|----------------------------------------------------|
| `cisco.ios.ios_hostname`      | Configura el hostname del dispositivo              |
| `cisco.ios.ios_system`        | Dominio, no ip domain-lookup                       |
| `cisco.ios.ios_user`          | Crea usuario ansible con privilege 15              |
| `cisco.ios.ios_l3_interfaces` | Asigna direcciones IPv4 a interfaces               |
| `cisco.ios.ios_interfaces`    | Activa interfaces (enabled: true) + descripciones  |
| `cisco.ios.ios_static_routes` | Ruta por defecto 0.0.0.0/0 hacia gateway           |
| `cisco.ios.ios_config`        | SSH params y VTY (sin módulo declarativo)          |
| `cisco.ios.ios_command`       | write memory                                       |

### cisco_ospf (rol)

| Módulo                          | Propósito                                              |
|---------------------------------|--------------------------------------------------------|
| `cisco.ios.ios_ospfv2`          | Proceso OSPF, router-id, passive-interface, networks   |
| `cisco.ios.ios_ospf_interfaces` | Asigna cada interfaz a su área OSPF                    |
| `cisco.ios.ios_command`         | write memory                                           |

### Verificación (playbook ospf_verify)

| Módulo                   | Propósito                                                   |
|--------------------------|-------------------------------------------------------------|
| `cisco.ios.ios_facts`    | Recoge estado OSPF estructurado (gather_network_resources)  |
| `cisco.ios.ios_command`  | Salidas operacionales (show ip ospf neighbor, etc.)         |

---

## Estructura del Proyecto

```
ospf-cisco-lab-ansible/
├── ansible.cfg
├── inventory/
│   ├── hosts.yml                   # IPs, ospf_interfaces, ospf_networks, interfaces_config
│   └── group_vars/
│       ├── all.yml                 # Credenciales y conexión
│       └── cisco_routers.yml       # process_id, mgmt_interface, gateway, domain
├── playbooks/
│   ├── base_config.yml             # Rol cisco_base (módulos declarativos)
│   ├── ospf_deploy.yml             # Rol cisco_ospf (ios_ospfv2 + ios_ospf_interfaces)
│   ├── ospf_verify.yml             # ios_facts + asserts estructurados
│   └── full_deploy.yml             # Full deploy con pre/post facts y asserts
└── roles/
    ├── cisco_base/
    │   ├── defaults/main.yml
    │   └── tasks/main.yml
    └── cisco_ospf/
        ├── defaults/main.yml
        └── tasks/main.yml
```

---

## Requisitos

```bash
pip install ansible
ansible-galaxy collection install cisco.ios
ansible-galaxy collection install ansible.netcommon
ansible-galaxy collection install ansible.utils   # requerido para filtro ipaddr
```

---

## Ejecución

```bash
cd ospf-cisco-lab-ansible/

# Verificar conectividad
ansible all -m ping

# Por pasos
ansible-playbook playbooks/base_config.yml
ansible-playbook playbooks/ospf_deploy.yml
ansible-playbook playbooks/ospf_verify.yml

# O todo en uno
ansible-playbook playbooks/full_deploy.yml
```

---

## Idempotencia — cómo funciona

Al ejecutar el playbook por segunda vez sin cambios en el inventario:

- `ios_ospfv2` comparará el estado deseado con el `gathered` del dispositivo
  y no generará ningún cambio (`changed=0`).
- `ios_ospf_interfaces` hará lo mismo por cada interfaz.
- Los asserts del playbook `ospf_verify` verificarán que `ios_facts` devuelve
  el router-id correcto como dato estructurado.

---

## Estados disponibles en ios_ospfv2 / ios_ospf_interfaces

| state        | Comportamiento                                         |
|--------------|--------------------------------------------------------|
| `merged`     | Aplica solo los cambios necesarios (por defecto)       |
| `replaced`   | Sustituye la config completa del proceso               |
| `overridden` | Borra todos los procesos OSPF y recrea desde cero      |
| `deleted`    | Elimina el proceso OSPF especificado                   |
| `gathered`   | Solo lee el estado actual (sin cambios, para audit)    |
| `rendered`   | Genera los comandos IOS sin conectarse (dry-run)       |
| `parsed`     | Parsea una config dada como texto (testing offline)    |

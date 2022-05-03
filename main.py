import ipaddress
import getpass
from netmiko.snmp_autodetect import SNMPDetect
from netmiko import SSHDetect
import pyfiglet
import napalm
from alive_progress import alive_bar
import time
import json
from pysnmp.hlapi import *
import easygui
community = "#MVXKP3M78EQUIP#"
community2 = "MVXKP3M78EQUIP"


def validate_ip_address(address):
    try:
        ipaddress.ip_address(address)
        print("Endereço de IP {} é valido.".format(address))
        return True
    except ValueError:
        print("Endereço de IP {} não valido".format(address))
        return False


def identificar_snmp(ip):
    host = ip
    device = {"host": ip, "username": router_user, "password": router_pass}
    snmp_community = community
    my_snmp = SNMPDetect(ip, snmp_version="v2c", community=snmp_community)
    device_type = my_snmp.autodetect()
    print("OS Do Aparelho: {}".format(device_type))
    if device_type is None:
        print("SNMP falhou! Tentando identificar por SSH.")
        ssh_detectar(ip)
    device["device_type"] = device_type
    return device_type, host


def ssh_detectar(ip):
    remote_device = {'device_type': 'autodetect',
                     'host': ip,
                     'username': router_user,
                     'password': router_pass}
    detectar = SSHDetect(**remote_device)
    melhor_resultado = detectar.autodetect()
    if melhor_resultado is None:
        print("O teste de SSH Falhou, não é possível identificar a OS.")
        return main()
    else:
        return melhor_resultado

def snmp_get(host):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.6.0'))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))


def napalm_get(tipo, host):
    item = tipo
    dict_netmiko_napalm = {
        "cisco_ios": "ios",
        "mikrotik_routeros": "ros",
    }
    if item in dict_netmiko_napalm.keys():
        a = dict_netmiko_napalm.get(item)
    else:
        print("OS de equipamento não suportado.")
        return main()
    driver = napalm.get_network_driver(a)
    device = driver(
        hostname=host,
        username=router_user,
        password=router_pass,
    )
    print("Conectando-se ao Equipamento...")
    try:
        device.open()
        print(device.get_facts())
        arptable = device.get_arp_table()
        for entry in arptable:
            print(entry)
        print(device.get_config(retrieve='running', full=False))
        print(device.get_environment())
        device.close()
    except:
        print("Não foi possível conectar ao Equipamento.")
        return saida()


def saida():
    while True:
        saidas = input('''
Selecionar Operação:
[1] Exportar Dados em JSON
[2] Menu Principal
''')

        if saidas == '1':
            pass
        elif saidas == '2':
            return main()


def main():
    while True:
        driver = input('''
Selecionar Operação:
[1] SNMP
[2] SSH
[3] Identificar Vendedor Automaticamente
[4] Fechar Programa
''')
        if driver == '1':
            router_mikrotik = input('Informe o IP:')
            if validate_ip_address(router_mikrotik) is True:
                start_time = time.time()
                #device_type, host = identificar_snmp(router_mikrotik)
                #napalm_get(device_type, host)
                snmp_get(router_mikrotik)
                performance = int(time.time() - start_time)
                with alive_bar(100) as bar:
                    for x in range(performance):
                        time.sleep(.5)
                        bar()
                saida()
            elif validate_ip_address(router_mikrotik) is False:
                print('IP Inválido.')
                return saida()

        elif driver == '2':
            router_cisco = input('Informe o IP:')
            validate_ip_address(router_cisco)
            saida()
        elif driver == '3':
            path = easygui.fileopenbox()

        elif driver == '4':
            exit()
        else:
            print("Escolha Inválida, Tente novamente..")


ascii_banner = pyfiglet.figlet_format("Mundivox")
print(ascii_banner)
router_user = input('Informe o Usuário:')
while len(router_user) == 0:
    router_user = input('Informe o Usuário:')
router_pass = getpass.getpass(prompt='Informe a Senha: ', stream=None)
while router_pass is None:
    router_pass = getpass.getpass(prompt='Informe a Senha: ', stream=None)

main()

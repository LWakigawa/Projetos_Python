import ipaddress
from netmiko.snmp_autodetect import SNMPDetect
from netmiko import SSHDetect
import pyfiglet
import napalm
from alive_progress import alive_bar
from pysnmp.hlapi import *
from easygui import *
import time
import sys

def validate_ip_address(address):
    try:
        ipaddress.ip_address(address)
        print("Endereço de IP {} é valido.".format(address))
        return True
    except ValueError:
        print("Endereço de IP {} não valido".format(address))
        return False


def identificar_snmp(ip):
    device = {"host": ip, "username": user, "password": password}
    snmp_community = community
    my_snmp = SNMPDetect(ip, snmp_version="v2c", community=snmp_community)
    device_type = my_snmp.autodetect()
    print("OS Do Aparelho: {}".format(device_type))
    device["device_type"] = device_type
    if device_type is None:
        print("SNMP falhou!.")
        device_type = Null
    return device_type


def identificar_ssh(ip):
    remote_device = {'device_type': 'autodetect',
                     'host': ip,
                     'username': user,
                     'password': password}
    detectar = SSHDetect(**remote_device)
    melhor_resultado = detectar.autodetect()
    if melhor_resultado is None:
        print("O teste de SSH Falhou, não é possível identificar a OS.")
        melhor_resultado = Null
    return melhor_resultado


def snmp_getvendor(host):
    iterator = nextCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((host, 161)),
        ContextData(),
        #ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr')).addAsn1MibSource('file:///usr/share/snmp',
        #                                                                      'http://mibs.snmplabs.com/asn1/@mib@'),
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysObjectID')).addAsn1MibSource('file:///usr/share/snmp',
                                                                              'http://mibs.snmplabs.com/asn1/@mib@'),
        #ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime')).addAsn1MibSource('file:///usr/share/snmp',
        #                                                                         'http://mibs.snmplabs.com/asn1/@mib@'),
        #ObjectType(ObjectIdentity('IF-MIB', 'ifTable')).addAsn1MibSource('file:///usr/share/snmp',
        #                                                                      'http://mibs.snmplabs.com/asn1/@mib@'),
        lexicographicMode=False
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        for oid, val in varBinds:
            convert = val.prettyPrint()
            if "enterprises.9." in convert:
                data_dict = {
                    "IP": linha,
                    "OS": "cisco",
                }
                return data_dict
            elif "enterprises.2011." in convert:
                data_dict = {
                    "IP": linha,
                    "OS": "huaweii",
                }
                return data_dict
            elif "enterprises.14988." in convert:
                data_dict = {
                    "IP": linha,
                    "OS": "mikrotik",
                }
                return data_dict
            print(f'{oid.prettyPrint()} = {val.prettyPrint()}')

def snmp_getdata(host, os):

    if os == 'cisco':
        iterator = nextCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr')).addAsn1MibSource('file:///usr/share/snmp',
                                                                                  'http://mibs.snmplabs.com/asn1/@mib@'),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime')).addAsn1MibSource('file:///usr/share/snmp',
                                                                                     'http://mibs.snmplabs.com/asn1/@mib@'),
            ObjectType(ObjectIdentity('IF-MIB', 'ifTable')).addAsn1MibSource('file:///usr/share/snmp',
                                                                            'http://mibs.snmplabs.com/asn1/@mib@'),
            lexicographicMode=False
        )
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        if errorIndication:
            print(errorIndication)

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

        else:
            for oid, val in varBinds:
                print(f'{oid.prettyPrint()} = {val.prettyPrint()}')

    elif os == 'huaweii':
        iterator = nextCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr')).addAsn1MibSource('file:///usr/share/snmp',
                                                                                  'http://mibs.snmplabs.com/asn1/@mib@'),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime')).addAsn1MibSource('file:///usr/share/snmp',
                                                                                     'http://mibs.snmplabs.com/asn1/@mib@'),
            ObjectType(ObjectIdentity('IF-MIB', 'ifTable')).addAsn1MibSource('file:///usr/share/snmp',
                                                                            'http://mibs.snmplabs.com/asn1/@mib@'),
            lexicographicMode=False
        )
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        if errorIndication:
            print(errorIndication)

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

        else:
            for oid, val in varBinds:
                print(f'{oid.prettyPrint()} = {val.prettyPrint()}')

    elif os == 'mikrotik':
        iterator = nextCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr')).addAsn1MibSource('file:///usr/share/snmp',
                                                                                  'http://mibs.snmplabs.com/asn1/@mib@'),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime')).addAsn1MibSource('file:///usr/share/snmp',
                                                                                     'http://mibs.snmplabs.com/asn1/@mib@'),
            ObjectType(ObjectIdentity('IF-MIB', 'ifTable')).addAsn1MibSource('file:///usr/share/snmp',
                                                                            'http://mibs.snmplabs.com/asn1/@mib@'),
            lexicographicMode=False
        )
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        if errorIndication:
            print(errorIndication)

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

        else:
            for oid, val in varBinds:
                print(f'{oid.prettyPrint()} = {val.prettyPrint()}')



community = "#MVXKP3M78EQUIP#"
community2 = "MVXKP3M78EQUIP"


login = multpasswordbox(msg='Entre com suas informações de Login.', title='Mundivox Login', fields=["Usuario", "Senha"], values=[], callback=None, run=True)
user, password = login

x = indexbox(msg='Selecione a Operação Desejada',
                 title='Mundivox Operações',
                 choices=['Selecionar lista de IPs', 'Inserir IPs Manualmente', 'Fechar Programa'],
                 cancel_choice='Fechar Programa')
if x == 0:
    arquivo = fileopenbox(msg='Escolha o arquivo .txt', title='Explorador de Arquivo', default='*', filetypes="*.txt", multiple=False)
    lista_ip = filter(None, open(arquivo, "r").read().splitlines())
    contador = 0
    texto_lista_valida = []
    texto_lista_invalida = []
    lista_ipvalido = []
    lista_invalido = []
    for linha in lista_ip:
        contador += 1
        if validate_ip_address(linha) is True:
            lista_ipvalido.append(linha)
            texto_lista_valida.append(f'IP {contador}: {linha}\n')
        elif validate_ip_address(linha) is False:
            lista_invalido.append(linha)
            texto_lista_invalida.append(f'IP {contador}: {linha}\n')
    #codebox(msg="IPs Validados.", title="Lista de IPs Válidos", text=texto_lista_valida)
    #codebox(msg="IPs com erro.", title="Lista de IPs Não Validados", text=texto_lista_invalida)

    for linha in lista_ipvalido:
        vendedor_dicionario = snmp_getvendor(linha)
        print(vendedor_dicionario)
        snmp_getdata(linha, vendedor_dicionario.get('OS'))

if x == 1:
    lista_ip = []
    lista_invalido = []
    ip_range = integerbox(msg='Quantos IPs quer consultar? Digite um valor inteiro.',lowerbound = 1, upperbound=20,title='Listagem de IP',image=None, root=None)
    exceptionbox(msg='Digite um Valor Inteiro.', title='Erro')
    l = [['IP'] for linha in range(ip_range)]
    print(l)
    z = multenterbox(msg='Entre com o(s) IP(s)', title='Listagem de IP', fields=l, values=[])
    print(z)



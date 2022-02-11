import sys
import netmiko
import pyfiglet
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_dispatcher import ConnectHandler
intro = pyfiglet.figlet_format("Mundivox", font = "isometric3")
print("intro")
print("Entre com seu usuário e senha")
user = input('Usuário:')
password = input('Senha:')
remotedevice = {'device_type': 'autodetect',
                'host': 'loremipsum',
                'username': 'user',
                'password': 'passwordpassword'}
print("Realizando conexão SSH, por favor, aguarde.\n")
guesser = SSHDetect(**remote_device)
best_match = guesser.autodetect()
if best_match is None:
    print("Erro: Nenhum modelo para esse tipo de GPE/Switch foi detectado.")
    exit()
print("Modelo: " + best_match)
remote_device['device_type'] = best_match
connection = ConnectHandler(**remote_device)
print(connection.send_command('show version'))
connection.disconnect()

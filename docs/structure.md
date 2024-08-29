# Como o código está estruturado?

Criei esta página na documentação, para tentar ajudar meu eu futuro a lembrar o que sua versão passado fez no meio do código. Já que minha memória me deixa na mão às vezes 😅. Neste processo, acredito que posso ajudar outras pessoas a entender melhor o que cada parte do código faz ou deveria fazer.

Abaixo será descrito o que cada módulo/classe contém e quais tarefas esta deve desempenhar.

### *class* Base(**kwargs)

Responsável por realizar a conexão com o roteador e definir métodos básicos porém fundamentais para a interação com o dispositivo, métodos esses que serão usados por todo o Netmikro para realizar as mais variadas tarefas.

!!! warning "Aviso"

    Essa classe não deve ser usada diretamente por você, assim como os métodos presentes nela. Ela é usada internamente pelo Netmikro. O que você provavelmente vai querer fazer é criar uma instância da classe **RouterOS**, a qual abordamos mais abaixo nesse mesma página.

#### _get(command)

Executa um comando no terminal de seu roteador Mikrotik e, caso exista, retorna um `str` contendo o conteúdo devolvido pelo roteador após a execução do comando.

#### _get_number(command)

Este método é utilizado para executar um comando que retornar um valor numérico inteiro, com isso Netmikro te retornará o valor como um `int`.

#### _get_float(command)

Semelhante ao método anterior, porém é usado quando o comando deve retornar um valor numérico decimal, e o valor retornado será um `float`.

#### _get_bool(command)

Executa um comando no roteador Mikrotik que deve retornar um valor booleano. Valores booleanos nos dispositivos Mikrotik são retonados como strings `'true'` ou `'false'`, sendo assim Netmikro lê esses valores e faz o casting para o devido tipo booleano em Python (`True` caso receba `'true'`, ou `False` caso receba qualquer outra coisa) e o retorna.

#### disconnect()

Encerra a conexão com o roteador.

#### cmd(command):

Executa demais comandos no roteador.

### *class* RouterOS(host, username, password, ssh_port)

Responsável por criar uma instancia de um roteador Mikrotik, segue um exemplo:

```python
from netmikro import RouterOS


router = RouterOS(
    '192.168.3.3',
    'user',
    'password',
    22,
)

router.cmd('/system identity print')
...
```

#### cmd_multiliine(commands)

Recebe uma lista contendo comandos a serem executados no roteador e os executa um a um.

### *class* Ip()

Responsável por realizar as configurações relacionadas a endereços IPv4 no dispositivo.

#### service

Um dicionário contendo as configuracoes de portas de serviço atuais.

#### ip_port_set(service_name, port)

Configura um novo número de porta para um servço específico.

### *class* System()

Realiza as configurações referentes ao sistema do roteador,

#### identity

Nome de identidade do roteador.

#### routerboard

Se e somente se o dispositivo for uma Routerboard isso será um dicionário contendo:

- model
- revision
- serial-number
- firmware-type
- factory-firmware
- current-firmware
- upgrade-firmware

#### license

Um dicionário contendo:

- software-id
- level
- features

#### note

Conteúdo presente nas notas do sistema.

#### resources

Um dicionário contendo:

- cpu
- cpu-frequency
- memory
- storage
- architecture
- board-name
- version

#### clock_time_get()

Obtém a hora atual do sistema.

#### clock_time_zone_get()

Obtém o timezone do roteador.

#### clock_gmt_offset()

Obtém o GMT Offset do dispositivo.

#### clock_dst_active_get()

Retorna um booleano informando se o DST está ativado ou não.

#### clock_timezone_autodetect_get()

Retorna um valor booleano informando se a deteção automática de timezone está ativado ou não.

#### health_voltage()

Retorna um `float` com a voltagem atual do dispositivo.

#### health_temperature()

Retorna um `float` com a temperatura do dispositivo.

#### history_system_get()

Imprime na tela um histórico de alterações no sistema.

#### identity_set(new_identity)

Configura uma nova identidade para o roteador.

#### note_set(note, show_at_login)

Configura uma nova nota para o dispositivo.

#### ntp_client_get()

Retorna um dicionário contendo informações sobre configurações de cliente NTP, chaves presentes no dicionário:

- enabled
- mode
- servers
- vrf
- freq-diff
- status
- synced-server
- synced-stratum
- system-offset

#### ntp_client_set(servers, enabled, mode, vrf)

Configura o client NTP do dispositivo.

#### ntp_server_get()

Retorna um dicionário com as configurações de servidor NTP do roteador. O dicionário contém as seguintes chaves:

- enabled
- broadcast
- multicast
- manycast
- broadcast-address
- vrf

#### is_routerboard()

Retorna `True` se o dispositivo for uma Routerboard Mikrotik.

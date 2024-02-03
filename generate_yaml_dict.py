minionTemplate = "      master: somehost\n      id: {MINIONNAME}"
params = {
    'group-1': {
        'vmwareTemplateName' : 'baseTemplate',
        'VMparams': [
                {
                    'vmName': 'vm1',
                    'cpu': 4,
                    'mem': 32,
                    'script_params': {
                        'hostname' : 'hostname1', 
                        'domain': 'some.domain',
                        'ip': '127.0.0.10',
                        'netmask': '255.255.255.0',
                        'gateway': '127.0.0.1', 
                        'dns': 'dns_separated'
                    },
                    'network_params': [
                        {'vlanName': 'vlanName1','interfaceState': 'distributed' },
                        {'vlanName': 'vlanName2','interfaceState': 'distributed' }
                    ],
                    'disk_params': [{'size': 890,'thin': True},{'size': 987,'thin': True}],
                    'minionTemplate': minionTemplate
                },
                {
                    'vmName': 'vm2',
                    'cpu': 4,
                    'mem': 32,
                    'script_params': {
                        'hostname' : 'hostname2', 
                        'domain': 'some.domain',
                        'ip': '127.0.0.10',
                        'netmask': '255.255.255.0',
                        'gateway': '127.0.0.1', 
                        'dns': 'dns_separated'
                    },
                    'network_params': [
                        {'vlanName': 'vlanName1','interfaceState': 'distributed' },
                        {'vlanName': 'vlanName2','interfaceState': 'distributed' }
                    ],
                    'disk_params': [{'size': 500,'thin': True},{'size': 98700,'thin': True}],
                    'minionTemplate': minionTemplate
                }
        ]
    },
    'group-2': {
        'vmwareTemplateName' : 'baseTemplate',
        'VMparams': [
            {
            'vmName': 'vm1',
            'cpu': 4,
            'mem': 32,
            'script_params': {
                'hostname' : 'hostname1', 
                'domain': 'some.domain',
                'ip': '127.0.0.10',
                'netmask': '255.255.255.0',
                'gateway': '127.0.0.1', 
                'dns': 'dns_separated'
            },
            'network_params': [
                {'vlanName': 'vlanName1','interfaceState': 'distributed' },
                {'vlanName': 'vlanName2','interfaceState': 'distributed' }
            ],
            'disk_params': [{'size': 890,'thin': True},{'size': 987,'thin': True}],
            'minionTemplate': minionTemplate
        }
        ]
    }
}

templateVM = ("  - {NAME}:\n    " +
              "num_cpus: {CPU}\n    " +
              "memory: {MEM}GB\n    " +
              "script_args: {ARGS}\n    " +
              "devices:\n      "
              "disk:{DISKS}\n      " +
              "network:{NET}\n    " +
              "minion: {MINION}")

def createInterfaces(InterfaceParams):
    interfaces = "\n"
    i = 1
    for interfaceParam in InterfaceParams:
        interfaceParam = dict(interfaceParam)
        interfase = "        Network adapter " + str(i) + ":\n          name: {VLANNAME}\n          switch_type: {INSTATE}\n" + "          ip: 127.0.0.1\n          gateway: 127.0.0.1\n          subnet_mask: 255.255.255.0\n"
        interfaces = interfaces + interfase.format(VLANNAME=interfaceParam['vlanName'], INSTATE=interfaceParam['interfaceState'])
        i += 1
    interfaces = interfaces[:-1]
    return interfaces

def createDisks(diskParams):
    disks = "\n"
    i = 1;
    for diskparm in diskParams:
        diskparm = dict(diskparm)
        disk = "        Hard disk " + str(i) + ":\n          size: {DISKSIZE}\n          thin_provision: {DISKTIPE}\n"
        disks = disks + disk.format(DISKSIZE=diskparm['size'],DISKTIPE=diskparm.get('thin'))
        i += 1
    disks = disks[:-1]
    return disks

def createVM(template, VMparams):
    VMparams_d = dict(VMparams)
    script_args = " ".join(VMparams_d['script_params'].values())
    interfaces = createInterfaces(VMparams_d['network_params'])
    disks = createDisks(VMparams_d['disk_params'])
    minion = "\n" + VMparams_d['minionTemplate'].format(MINIONNAME=(VMparams_d['script_params']['hostname'] + "." + VMparams_d['script_params']['domain']))
    textfile = template.format(NAME=VMparams_d['vmName'],CPU=VMparams_d['cpu'],MEM=VMparams_d['mem'],ARGS=script_args,NET=interfaces,DISKS=disks,MINION=minion) + "\n"
    return textfile

def createVMs(template, params):
    textfile = ""
    for VM in params:
        textfile = textfile + createVM(template, VM)
    textfile = textfile[:-1]
    return textfile

for key, value in params.items():
    #finalvm =  value['vmwareTemplateName'] + ":\n" + createVMs(templateVM, value['VMparams'])
    finalvm =  value['vmwareTemplateName'] + ":\n" + createVMs(templateVM, value['VMparams'])
    print(finalvm)
    # f = open(groupVM[0] + '.txt','w')  # открытие в режиме записи
    # f.write(finalvm)  # запись Hello World в файл
    # f.close()  # закрытие файла
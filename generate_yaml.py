minionTemplate = "      master: somehost\n      minionName: {MINIONNAME}"
params = [
    ["group-1",
     [
         ["host1", 4, 32, ["127.0.0.10", "127.0.0.1", "255.255.255.0", "dns1", "dns2"],
          [
              ["vlanName1", True],
              ["vlanName2", True]
          ],
          [
              [890, "t1"],
              [987, "t2"]
          ],
          minionTemplate],
         ["host2", 4, 16, ["127.0.0.10", "127.0.0.1", "255.255.255.0", "dns1", "dns2"],
          [
              ["vlanName1", True],
              ["vlanName2", False]
          ],
          [
              [890, "t1"],
              [987, "t2"]
          ],
          minionTemplate]
     ]
    ],
    ["group-2",
     [
         ["host1",4,8,["127.0.0.10","127.0.0.1","255.255.255.0","dns1","dns2"],
          [
              ["vlanName1",True],
              ["vlanName2",False]
          ],
          [
              [890,"t1"],
              [987,"t2"]
          ],
          minionTemplate],
         ["host2", 4, 8, ["127.0.0.10", "127.0.0.1", "255.255.255.0", "dns1", "dns2"],
          [
              ["vlanName1", True],
              ["vlanName2", False]
          ],
          [
              [890, "t1"],
              [987, "t2"]
          ],
          minionTemplate],
         ["host3", 4, 8, ["127.0.0.10", "127.0.0.1", "255.255.255.0", "dns1", "dns2"],
          [
              ["vlanName1", True],
              ["vlanName2", False]
          ],
          [
              [890, "t1"],
              [987, "t2"]
          ],
          minionTemplate]
     ]
    ]
]
templateVM = ("  - {NAME}:\n    " +
              "cpu: {CPU}\n    " +
              "memory: {MEM}\n    " +
              "script_args: {ARGS}\n    " +
              "network:{NET}\n    " +
              "disks:{DISKS}\n    " +
              "minion: {MINION}")
def createInterfaces(InterfaceParams):
    interfaces = "\n"
    i = 1
    for interfaceParam in InterfaceParams:
        interfase = "    - interface" + str(i) + ":\n      vlan: {VLANNAME}\n      CONNECTED: {INSTATE}\n"
        interfaces = interfaces + interfase.format(VLANNAME=interfaceParam[0], INSTATE=interfaceParam[1])
        i += 1
    interfaces = interfaces[:-1]
    return interfaces
def createDisks(diskParams):
    disks = "\n"
    i = 1;
    for diskparm in diskParams:
        disk = "    - disk" + str(i) + ":\n      disksize: {DISKSIZE}\n      disktype: {DISKTIPE}\n"
        disks = disks + disk.format(DISKSIZE=diskparm[0],DISKTIPE=diskparm[1])
        i += 1
    disks = disks[:-1]
    return disks

def createVM(template, params):
    script_args = " ".join(params[3])
    interfaces = createInterfaces(params[4])
    disks = createDisks(params[5])
    minion = "\n" + params[6].format(MINIONNAME=params[0])
    textfile = template.format(NAME=params[0],CPU=params[1],MEM=params[2],ARGS=script_args,NET=interfaces,DISKS=disks,MINION=minion) + "\n"
    return textfile

def createVMs(template,params):
    textfile = ""
    for VM in params:
      textfile = textfile + createVM(template, VM)
    textfile = textfile[:-1]
    return textfile

for groupVM in params:
    finalvm = groupVM[0] + ":\n" + createVMs(templateVM, groupVM[1])
    print(finalvm)
    f = open(groupVM[0] + '.txt','w')  # открытие в режиме записи
    f.write(finalvm)  # запись Hello World в файл
    f.close()  # закрытие файла
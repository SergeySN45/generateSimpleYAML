minionTemplate = "      master: somehost\n      id: {MINIONNAME}"
params = [
    ["group-1", "vmwareTemplateName",
     [
         ["VMname1", 4, 32, ["hostname1", "domain", "127.0.0.10", "255.255.255.0", "127.0.0.1", "dns_separated"],
          [
              ["vlanName1", "distributed"],
              ["vlanName2", "distributed"]
          ],
          [
              [890, True],
              [987, True]
          ],
          minionTemplate],
         ["host2", 4, 16, ["127.0.0.10", "127.0.0.1", "255.255.255.0", "dns1", "dns2"],
          [
              ["vlanName1", "distributed"],
              ["vlanName2", "distributed"]
          ],
          [
              [890, False],
              [987, True]
          ],
          minionTemplate]
     ]
    ],
    ["group-2", "vmwareTemplateName",
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
        interfase = "        Network adapter " + str(i) + ":\n          name: {VLANNAME}\n          switch_type: {INSTATE}\n" + "          ip: 127.0.0.1\n          gateway: 127.0.0.1\n          subnet_mask: 255.255.255.0\n"
        interfaces = interfaces + interfase.format(VLANNAME=interfaceParam[0], INSTATE=interfaceParam[1])
        i += 1
    interfaces = interfaces[:-1]
    return interfaces

def createDisks(diskParams):
    disks = "\n"
    i = 1;
    for diskparm in diskParams:
        disk = "        Hard disk " + str(i) + ":\n          size: {DISKSIZE}\n          thin_provision: {DISKTIPE}\n"
        disks = disks + disk.format(DISKSIZE=diskparm[0],DISKTIPE=diskparm[1])
        i += 1
    disks = disks[:-1]
    return disks

def createVM(template, VMparams):
    script_args = " ".join(VMparams[3])
    interfaces = createInterfaces(VMparams[4])
    disks = createDisks(VMparams[5])
    minion = "\n" + VMparams[6].format(MINIONNAME=(VMparams[0] + "." + VMparams[3][1]))
    textfile = template.format(NAME=VMparams[0],CPU=VMparams[1],MEM=VMparams[2],ARGS=script_args,NET=interfaces,DISKS=disks,MINION=minion) + "\n"
    return textfile

def createVMs(template,params):
    textfile = ""
    for VM in params:
      textfile = textfile + createVM(template, VM)
    textfile = textfile[:-1]
    return textfile

for groupVM in params:
    finalvm = groupVM[1] + ":\n" + createVMs(templateVM, groupVM[2])
    print(finalvm)
    f = open(groupVM[0] + '.txt','w')
    f.write(finalvm)
    f.close()
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
    disks = createDisks(params[6])
    minion = "\n" + params[7].format(MINIONNAME=params[0])
    textfile = template.format(NAME=params[0],CPU=params[1],MEM=params[2],NET=params[3],DISKS=disks,MINION=minion) + "\n"
    return textfile

def createVMs(template,params):
    textfile = ""
    for VM in params:
      textfile = textfile + createVM(template, VM)
    textfile = textfile[:-1]
    return textfile

minionTemplate = '''      master: somehost
      minionName: {MINIONNAME}'''
params = [["host1",4,8,123,321,"ttt",[[890,"t1"],[987,"t2"]],minionTemplate],["host2",8,16,456,876,"ttt",[[852,"t1"],[951,"t3"]],minionTemplate]]
tempalteVMS = "{VMs}"
templateVM = "- {NAME}:\n    cpu: {CPU}\n    memory: {MEM}\n    network: {NET}\n    disks:{DISKS}\n    minion: {MINION}"
template2 = '''its another 
  text'''

finalvm = "mainTemplate:\n"  + createVMs(templateVM, params)
print(finalvm)
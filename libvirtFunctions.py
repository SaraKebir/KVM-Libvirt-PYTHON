# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import libvirt

def hostInfo():
    #opening the connexion
    conn = libvirt.open('qemu:///system')
    if conn == None:
        print('Failed to open connection to qemu:///system', file=sys.stderr)
        exit(1)
    #Hostname
    print('Hostname : ' + conn.getHostname())
    #Max virtual CPU
    vcpus = conn.getMaxVcpus(None)
    print('Maximum support virtual CPUs: '+str(vcpus))
    #Host Infos
    nodeinfo = conn.getInfo()
    print('Modèle: '+str(nodeinfo[0]))
    print('Taille de la mémoire: '+str(nodeinfo[1])+'MB')
    print('Nombre de CPUs: '+str(nodeinfo[2]))
    print('MHz des CPUs: '+str(nodeinfo[3]))
    print('Nombre de NUMA nodes: '+str(nodeinfo[4]))
    print('Nombre de CPU sockets: '+str(nodeinfo[5]))
    print('Nombre de coeurs CPU par socket: '+str(nodeinfo[6]))
    print('Nombre de thread threads per coeur: '+str(nodeinfo[7]))
    #Virtualization type
    print('Type de virtualisation: '+conn.getType())
    conn.close()
    raw_input("Appuillez sur Entrée pour revenir au menu précedent...")

def vmInfo(domainName):
    #opening the connexion
    conn = libvirt.open('qemu:///system')
    if conn == None:
        print('Failed to open connection to qemu:///system', file=sys.stderr)
        exit(1)
    dom = conn.lookupByName(domainName)
    if dom == None:
        print('Failed to get the domain object', file=sys.stderr)
        exit(1)
    print("Name : "+ domainName)
    id = dom.ID()
    if id == -1:
        print("La machine n'est pas en marche donc n'a pas d'ID.")
    else:
        print("L'ID de la machine est " + str(id))
    osType = dom.OSType()
    print("Type de L'OS = '" + osType + "'")
    state, maxmem, mem, cpus, cput = dom.info()
    print('Max Mémoire = ' + str(maxmem))
    print('Mémoire = ' + str(mem))
    print('Nombre de CPUs = ' + str(cpus))
    print('Temps CPU (en ns) = ' + str(cput))
    flag = dom.isActive()
    if flag == True:
        print('La machine est active.')
    else:
        print("La machine n'est pas active.")
    state, reason = dom.state()

    if state == libvirt.VIR_DOMAIN_NOSTATE:
        print("l'etat est VIR_DOMAIN_NOSTATE")
    elif state == libvirt.VIR_DOMAIN_RUNNING:
        print("l'etat est VIR_DOMAIN_RUNNING")
    elif state == libvirt.VIR_DOMAIN_BLOCKED:
        print("l'etat est VIR_DOMAIN_BLOCKED")
    elif state == libvirt.VIR_DOMAIN_PAUSED:
        print("l'etat est VIR_DOMAIN_PAUSED")
    elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
        print("l'etat est VIR_DOMAIN_SHUTDOWN")
    elif state == libvirt.VIR_DOMAIN_SHUTOFF:
        print("l'etat est VIR_DOMAIN_SHUTOFF")
    elif state == libvirt.VIR_DOMAIN_CRASHED:
        print("l'etat est VIR_DOMAIN_CRASHED")
    elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
        print("l'etat est VIR_DOMAIN_PMSUSPENDED")
    else:
        print("l'etat est unknown.")
    raw_input("Appuillez sur Entrée pour revenir au menu précedent...")
    conn.close()

def domainList():
    #opening the connexion
    domainNames = []
    conn = libvirt.open('qemu:///system')
    if conn == None:
        print('Failed to open connection to qemu:///system', file=sys.stderr)
        exit(1)
    #getting the list of active and inactive domains
    domains = conn.listAllDomains(0)
    if len(domains) != 0:
        for domain in domains:
            print('  '+domain.name())
            domainNames.append(domain.name())
    else:
        print('  None')
    conn.close()
    return domainNames

def startDomain(domainName):
    conn = libvirt.open('qemu:///system')
    if conn == None:
        print('Failed to open connection to qemu:///system', file=sys.stderr)
        exit(1)
    dom = conn.lookupByName(domainName)
    if dom == None:
        print('Failed to get the domain object', file=sys.stderr)
        exit(1)
    flag = dom.isActive()
    if flag == True:
        print('La machine est déja en marche.')
    else:
        print("La machine a été mise en marche.")
    	dom.create()
    raw_input("Appuillez sur Entrée pour revenir au menu précedent...")
    conn.close()

def destroyDomain(domainName):
    conn = libvirt.open('qemu:///system')
    if conn == None:
        print('Failed to open connection to qemu:///system', file=sys.stderr)
        exit(1)
    dom = conn.lookupByName(domainName)
    if dom == None:
        print('Failed to get the domain object', file=sys.stderr)
        exit(1)
    flag = dom.isActive()
    if flag == True:
        print('La machine a été éteinte.')
	dom.destroy()
    else:
        print("La machine n'est pas en marche.")
    raw_input("Appuillez sur Entrée pour revenir au menu précedent...")
    conn.close()

def networkDomain(domainName):
    conn = libvirt.open('qemu:///system')
    if conn == None:
        print('Failed to open connection to qemu:///system', file=sys.stderr)
        exit(1)
    dom = conn.lookupByName(domainName)
    if dom == None:
        print('Failed to get the domain object', file=sys.stderr)
        exit(1)
    #ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE,0)
    #ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
    try:
        ifaces = domain.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT)
    except (TypeError, libvirt.libvirtError):
        try:
            raw_input("Appuillez sur Entrée pour revenir au menu précedent...")
            ifaces = domain.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE)
        except (TypeError, libvirt.libvirtError):
            pass
    print("Les adresses IP des interfaces:")
    
    for (name, val) in ifaces.iteritems():
	if val['addrs']:
	    for ipaddr in val['addrs']:
		    if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
		        print(ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV4")
		    elif ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV6:
		        print(ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV6")

    raw_input("Appuillez sur Entrée pour revenir au menu précedent...")
    conn.close()

import libvirt
import random
import time
from xml.dom import minidom
import xml.etree.ElementTree as ET

conn = libvirt.open("qemu:///system")
if not conn:
    raise SystemExit("Failed to open connection to qemu:///system")


def getMacAddresses(dom, guest_name):
    raw_xml = dom.XMLDesc()
    xml = minidom.parseString(raw_xml)

    macs = {}
    interfaceTypes = xml.getElementsByTagName("interface")
    interface_type = {}
    for interfaceType in interfaceTypes:
        # print("interface: type=" + interfaceType.getAttribute("type"))
        interfaceNodes = interfaceType.childNodes
        # print(interfaceNodes[0].nodeName)
        mac = ''
        for interfaceNode in interfaceNodes:
            if interfaceNode.nodeName == "source":
                # print(interfaceNode.attributes[interfaceType.getAttribute("type")].value)
                # print(interfaceType.getAttribute("type"))
                # print(interface_type)
                # if interfaceNode.attributes[interfaceType.getAttribute("type")].value == 'default':
                macs[interfaceNode.attributes[interfaceType.getAttribute("type")].value + '-' + guest_name] = mac
                interface_type[interfaceNode.attributes[interfaceType.getAttribute("type")].value + '-' + guest_name] = interfaceType.getAttribute("type")
                # else:
                    # macs[interfaceNode.attributes[interfaceType.getAttribute("type")].value] = mac
            if interfaceNode.nodeName == "mac":
                for attr in interfaceNode.attributes.keys():
                    if interfaceNode.attributes[attr].name == "address":
                        # print(networkName)
                        mac = interfaceNode.attributes[attr].value
    # print(interface_type)
    return macs, interface_type

mac_addresses = {}
interface_types = {}
list = conn.listAllDomains()
xmls = {}
xmls_string = {}
for domain in list:
    dom = conn.lookupByID(domain.ID())
    # raw_xml = dom.XMLDesc()
    mac_addresses[domain.name()], types = getMacAddresses(dom, domain.name())
    xmls[domain.name()] = domain
    xmls_string[domain.name()] = xmls[domain.name()].XMLDesc()
    # print(types)
    interface_types.update(types)
    # print(interface_types)
    # print(domain.name(), domain.interfaceAddresses(2))
    # print(dom.XMLDesc())
# print(interface_types)
print('MAC addresses of all guest VMs:')
for guest_vm in mac_addresses:
    print(guest_vm + ':')
    for net_interface in mac_addresses[guest_vm]:
        print('\t' + net_interface.split('-')[0] + ':\t' + mac_addresses[guest_vm][net_interface])
    print('\n')
print('\n')

mac_list = {}
to_restart = {}
for vm in mac_addresses:
    # print(dir(xmls[vm]))
    for net_interface in mac_addresses[vm]:
        # print(mac_list)
        if mac_addresses[vm][net_interface] not in mac_list:
            # if mac == 'default':
            # mac = mac + '-' + vm
            mac_list[mac_addresses[vm][net_interface]] = net_interface
        else:
            # trigger mac update function
            # xml = ET.fromstring(xmls[vm].XMLDesc()) if isinstance(xmls[vm], libvirt.virDomain) else ET.fromstring(xmls[vm])
            print('Duplicate MAC Address found at ' + net_interface)
            xml = ET.fromstring(xmls_string[vm])
            finder = './devices/interface[@type=\'network\']' if (interface_types[net_interface] == 'network') else './devices/interface[@type=\'bridge\']'
            # print(finder)
            mac = xml.find(finder + '/mac')
            interface = xml.find(finder)
            # print(ET.tostring(interface, encoding='unicode'))
            mac.set('address',"02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            # interface = xml.find('./devices/interface[@type=\'bridge\']')
            # print(ET.tostring(interface, encoding='unicode'))
            # xmls[vm].updateDeviceFlags(ET.tostring(interface, encoding='unicode'))
            xmls_string[vm] = ET.tostring(xml, encoding='unicode')
            conn.defineXMLFlags(ET.tostring(xml, encoding='unicode'))
            # print(dir(conn))
            to_restart[vm] = True
# print(to_restart)
for vm in to_restart:
    xmls[vm].shutdown()
    time.sleep(10)
    xmls[vm].create()

conn.close()

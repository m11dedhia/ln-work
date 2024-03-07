import libvirt
import sys
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
    for interfaceType in interfaceTypes:
        # print("interface: type=" + interfaceType.getAttribute("type"))
        interfaceNodes = interfaceType.childNodes
        # print(interfaceNodes[0].nodeName)
        mac = ''
        interface_type = {}
        for interfaceNode in interfaceNodes:
            if interfaceNode.nodeName == "source":
                # print(interfaceNode.attributes[interfaceType.getAttribute("type")].value)
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
    return macs, interface_type

mac_addresses = {}
interface_types = {}
list = conn.listAllDomains()
xmls = {}
for domain in list:
    dom = conn.lookupByID(domain.ID())
    # raw_xml = dom.XMLDesc()
    mac_addresses[domain.name()], types = getMacAddresses(dom, domain.name())
    xmls[domain.name()] = domain
    interface_types.update(types)
    # print(domain.name(), domain.interfaceAddresses(2))
    # print(dom.XMLDesc())

mac_list = {}
for vm in mac_addresses:
    # print(dir(xmls[vm]))
    for net_interface in mac_addresses[vm]:
        print(mac_list)
        if mac_addresses[vm][net_interface] not in mac_list:
            # if mac == 'default':
            # mac = mac + '-' + vm
            mac_list[mac_addresses[vm][net_interface]] = net_interface
        else:
            # trigger mac update function
            xml = ET.fromstring(xmls[vm].XMLDesc())
            # print(ET.tostring(xml, encoding='unicode'))
            finder = './devices/interface[@type=\'network\']' if (interface_types[net_interface] == 'network') else './devices/interface[@type=\'bridge\']'
            print(finder)
            mac = xml.find(finder + '/mac')
            interface = xml.find(finder)
            # print(ET.tostring(interface, encoding='unicode'))
            mac.set('address',"02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            # interface = xml.find('./devices/interface[@type=\'bridge\']')
            # print(ET.tostring(interface, encoding='unicode'))
            # xmls[vm].updateDeviceFlags(ET.tostring(interface, encoding='unicode'))
            conn.defineXMLFlags(ET.tostring(xml, encoding='unicode'))
            # print(dir(conn))
            xmls[vm].shutdown()
            time.sleep(10)
            xmls[vm].create()

conn.close()


print(mac_addresses)

import libvirt
conn = libvirt.open('qemu:///system')

print(conn.getCapabilities())

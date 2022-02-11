#!/usr/bin/env python3
start_subinterface = 3010
count_subinterface = 500

with open("custom_template/traffic_policies.j2", "w") as f:
    traffic_policy_settings = """traffic-policies
   field-set ipv4 prefix BOGONS
      0.0.0.0/8
      10.0.0.0/8
      100.64.0.0/10
      127.0.0.0/8
      169.254.0.0/16
      192.0.2.0/24
      192.88.99.0/24
      192.168.0.0/16
      198.18.0.0/15
      198.51.100.0/24
      203.0.113.0/24
      224.0.0.0/4
      240.0.0.0/4
   !
   field-set ipv6 prefix BOGONSv6
      ::/8
      100::/64
      2001:2::/48
      2001:10::/28
      2001:db8::/32
      2002::/16
      3ffe::/16
      fc00::/7
      fe80::/10
      fec0::/10
      ff00::/8
   !
   field-set l4-port UDP_CHARGEN
      19
   !
   field-set l4-port UDP_HTTPS
      443
   !
   field-set l4-port UDP_LDAP
      389
   !
   field-set l4-port UDP_NTP
      123
   !
   field-set l4-port UDP_SSDP
      1900
   !"""
    f.write(traffic_policy_settings)

    for i in range(start_subinterface, start_subinterface + count_subinterface + 1):
        print(f"Generating {i}")
        traffic_policy = f"""
   traffic-policy EDGE-PROTECTION-CUST-IN-{i}
      match BOGONS-DISCARD ipv4
         source prefix field-set BOGONS
         !
         actions
            drop
      !
      match BOGONS-DISCARDv6 ipv6
         source prefix field-set BOGONSv6
         !
         actions
            drop
      !
      match UDP_CHARGEN ipv4
         protocol udp destination port field-set UDP_CHARGEN
         !
         actions
            police rate 5000 kbps burst-size 10000 bytes
      !
      match UDP_CHARGENv6 ipv6
         protocol udp destination port field-set UDP_CHARGEN
         !
         actions
            police rate 5000 kbps burst-size 10000 bytes
      !
      match UDP_NTP ipv4
         protocol udp destination port field-set UDP_NTP
         !
         actions
            police rate 5000 kbps burst-size 10000 bytes
      !
      match UDP_NTPv6 ipv6
         protocol udp destination port field-set UDP_NTP
         !
         actions
            police rate 5000 kbps burst-size 10000 bytes
      !
      match UDP_LDAP ipv4
         protocol udp destination port field-set UDP_LDAP
         !
         actions
            police rate 5000 kbps burst-size 10000 bytes
      !
      match UDP_LDAPv6 ipv6
         protocol udp destination port field-set UDP_LDAP
         !
         actions
            police rate 5000 kbps burst-size 10000 bytes
      !
      match UDP_HTTPS ipv4
         protocol udp destination port field-set UDP_HTTPS
         !
         actions
            police rate 10000 kbps burst-size 10000 bytes
      !
      match UDP_HTTPSv6 ipv6
         protocol udp destination port field-set UDP_HTTPS
         !
         actions
            police rate 10000 kbps burst-size 10000 bytes
      !
      match UDP_SSDP ipv4
         protocol udp destination port field-set UDP_SSDP
         !
         actions
            police rate 5000 kbps burst-size 10000 bytes
      !
      match UDP_SSDPv6 ipv6
         protocol udp destination port field-set UDP_SSDP
         !
         actions
            police rate 5000 kbps burst-size 10000 bytes
      !
      match ipv4-all-default ipv4
         actions
            police rate 100 mbps burst-size 100000 bytes
      !
      match ipv6-all-default ipv6
         actions
            police rate 100 mbps burst-size 100000 bytes
   !"""
        f.write(traffic_policy)

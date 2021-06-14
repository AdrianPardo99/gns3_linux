# En R2
show ip route | begin Gateway

# En R1
show running-config | section class-map
show running-config | section policy-map
show running-config | section access-list
show running-config interface f0/0
show running-config interface f2/0
show policy-map interface f0/0
show policy-map interface f2/0

# En la VM1 conocida como VPC1 de acuerdo a la topologia
telnet 10.10.2.100 80

# En R1
show policy-map interface f0/0 input class MATCH_HTTP

# En R3
show policy-map interface f1/0 output class HTTP_TO_CORE

# En R1
ping
# Con los siguientes datos que se despliegan cuando se da ping:
# Protocol [ip]:
# Target IP address: 10.10.23.2
# Repeat count [5]: 100
# Datagram size [100]: 1400
# Timeout in seconds [2]:
# Extended commands [n]: y
# Source address or interface: 10.10.13.1
# Type of service [0]: 32
# Set DF bit in IP header? [no]: yes
# Validate reply data? [no]:
# Data pattern [0xABCD]:
# Loose, Strict, Record, Timestamp, Verbose[none]:
# Sweep range of sizes [n]:

show policy-map interface f2/0 output class ICMP_TO_CORE

# En R3
show policy-map interface f2/0 output class ICMP_TO_CORE

#!/usr/bin/env python3
from pysnmp.hlapi import *
HOSTNAME_OID = "1.3.6.1.2.1.1.5.0"
DESCR_OID = "1.3.6.1.2.1.1.1.0"
CONTACT_OID = "1.3.6.1.2.1.1.4.0"
LOCATION_OID = "1.3.6.1.2.1.1.6.0"
INTERFACE_OID = "1.3.6.1.2.1.2.2.1"
INTNUMBER_OID = "1.3.6.1.2.1.2.1.0"
user='admin'
password='administrador_snmp'

def set_information(index,host,value):
    if index==0:
        snmp_query_set(host,HOSTNAME_OID,value)
    elif index==1:
        snmp_query_set(host,DESCR_OID,value)
    elif index==2:
        snmp_query_set(host,CONTACT_OID,value)
    elif index==3:
        snmp_query_set(host,LOCATION_OID,value)


def snmp_query_set(host, oid, value):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        setCmd(
            SnmpEngine(),
            UsmUserData(user, password,password,
                authProtocol=usmHMACSHAAuthProtocol,
                privProtocol=usmDESPrivProtocol),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid),value),
            lookupMib=False,
        )
    )
    if errorIndication:
        raise Exception(str(errorIndication))

    if errorStatus:
        raise Exception(
            f"{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1] or '?'}"
        )
    return "Change correct"

#set_information(2,"10.0.1.254","La pandilla mantequilla")

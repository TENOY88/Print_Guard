from pysnmp.hlapi import *
from pysnmp.hlapi.v3arch.asyncio import *
import asyncio
import sqlite3

''' Check les évènements d'alertes et lorsqu'il ya une erreur corespondant a un 
 bourrage, ou "printer offline" envoies une alerte
 Gestion centralisée des alertes et notifications.
 Enrégistre les évenements d'alertes dans un fichier log qui sera envoyé 
 en fin de journée '''


async def run():
  data = ObjectType(ObjectIdentity('1.3.6.1.2.1.43.18.1.1.4.1.1')) 
    #ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
  

  g = get_cmd(SnmpEngine()
            , CommunityData('public', mpModel=1)
            , await UdpTransportTarget.create(('10.11.99.43', 161))
            , ContextData()
            , data)

  errorIndication, errorStatus, errorIndex, varBinds = await g

  if errorIndication:
      print(errorIndication)
  elif errorStatus:
      print('%s at %s' % (
                          errorStatus.prettyPrint(),
                          errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
                        )

            )
  else:
      for varBind in varBinds:
          print(' = '.join([x.prettyPrint() for x in varBind]))
          
          if varBinds[0][1].prettyPrint() < "3":
           print("Problème de toner, de tambour ou d'encre")

          elif varBinds[0][1].prettyPrint() < "4":
           print("Bourrage papier")

          elif varBinds[0][1].prettyPrint() < "5":
           print("Erreur de traitement (PostScript, PCL)")

          elif varBinds[0][1].prettyPrint() < "6":
           print("Capot ouvert")

          elif varBinds[0][1].prettyPrint() < "8":
           print("Bac papier vide")

          elif varBinds[0][1].prettyPrint() < "9":
           print("Bac de sortie plein ou bloqué")

          elif varBinds[0][1].prettyPrint() < "10":
           print("Niveau de toner bas")

          elif varBinds[0][1].prettyPrint() < "11":
           print("Problème de toner")

          elif varBinds[0][1].prettyPrint() < "12":
           print("Chargement de papier impossible")
          else :
             print ("Pas d'alerte")

          
asyncio.run(run())


''' configurer plutot l'envoi d'alertes à travers l'EWS de l'imprimante'''


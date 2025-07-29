from pysnmp.hlapi import *
from pysnmp.hlapi.v3arch.asyncio import *
import asyncio

''' ce module contiendra toutes les actions a faire (se trouvant dans le
module cli.py en passantn les arguments au script sauf les actions sur
 la BD qui se trouveront dans le module manage_db'''

'''Rappel: Gestion des exceptions pour toutes les fonctions ici
Il reste à passer aussi les adresses IP de la BD pour les fonctions'''



# 1- Arguments de base

#1.1. Pour -info
class HelpDisplay:
    """Classe pour afficher l'aide et les informations générales."""
    
    @staticmethod
    def afficher_info():
        """ Affiche une présentation générale du script et de ses arguments """
        print("""
    **Présentation de PrintGuard.py**
    Ce script permet de superviser les imprimantes du réseau en utilisant SNMP et une base de données MySQL.

    **Options disponibles :**

    **Supervision des imprimantes**
    - `PrintGuard.py -report` → Génère un rapport immédiat général des imprimantes
    - `PrintGuard.py -report <IP>` → Génère un rapport pour une imprimante spécifique
    - `PrintGuard.py -status <IP>` → Affiche le statut d’une imprimante donnée
    - `PrintGuard.py -alerts <IP>` → Affiche les alertes en cours sur une imprimante donnée
    - `PrintGuard.py -history <IP>` → Affiche l’historique des événements d’une imprimante
    - `PrintGuard.py -cartbridge <IP>` → Affiche le niveau de cartouches d’une imprimante
    - `PrintGuard.py -paper <IP>` → Affiche le niveau de papier d’une imprimante
    - `PrintGuard.py -maintenance <IP>` → Affiche la dernière date de maintenance d’une imprimante
    - `PrintGuard.py --start <IP>` → Démarre une imprimante
    - `PrintGuard.py --stop <IP>` → Arrête une imprimante

    **Gestion de la base de données**
    - `PrintGuard.py -l` → Affiche la liste des imprimantes dans la BD
    - `PrintGuard.py -a <IP> <nom> <modèle>` → Ajoute une imprimante
    - `PrintGuard.py -r <IP>` → Supprime une imprimante
    - `PrintGuard.py -i <IP>` → Affiche les informations d’une imprimante
    - `PrintGuard.py -h` → Affiche l’historique des ajouts/suppressions des imprimantes
    - `PrintGuard.py -update-mdate <IP> <AAAA-MM-JJ>` → Met à jour la date de maintenance d’une imprimante

    **Dépannage**
    - `PrintGuard.py -repair <IP> <type_intervention> <AAAA-MM-JJ> "<description>" <technicien>` → Enregistre un dépannage
    - `PrintGuard.py -hh <IP>` → Affiche l’historique des dépannages d’une imprimante

    **Aide**
    - `PrintGuard.py -info` → Affiche cette présentation générale
    - `PrintGuard.py -help` → Liste tous les arguments possibles et leurs actions

    **Exemple d'utilisation :**
    ```bash
    python PrintGuard.py -status 192.168.1.100
    """)
        
        #1.2. Pour -help
    
    @staticmethod
    def print_help():
        print("""
    **Présentation de PrintGuard.py**
    Ce script permet de superviser les imprimantes du réseau en utilisant SNMP et une base de données MySQL.

    **Options disponibles :**

    **Supervision des imprimantes**
    - `PrintGuard.py -report` → Génère un rapport immédiat général des imprimantes
    - `PrintGuard.py -report <IP>` → Génère un rapport pour une imprimante spécifique
    - `PrintGuard.py -status <IP>` → Affiche le statut d’une imprimante donnée
    - `PrintGuard.py -alerts <IP>` → Affiche les alertes en cours sur une imprimante donnée
    - `PrintGuard.py -history <IP>` → Affiche l’historique des événements d’une imprimante
    - `PrintGuard.py -cartbridge <IP>` → Affiche le niveau de cartouches d’une imprimante
    - `PrintGuard.py -paper <IP>` → Affiche le niveau de papier d’une imprimante
    - `PrintGuard.py -maintenance <IP>` → Affiche la dernière date de maintenance d’une imprimante
    - `PrintGuard.py --start <IP>` → Démarre une imprimante
    - `PrintGuard.py --stop <IP>` → Arrête une imprimante

    **Gestion de la base de données**
    - `PrintGuard.py -l` → Affiche la liste des imprimantes dans la BD
    - `PrintGuard.py -a <IP> <nom> <modèle>` → Ajoute une imprimante
    - `PrintGuard.py -r <IP>` → Supprime une imprimante
    - `PrintGuard.py -i <IP>` → Affiche les informations d’une imprimante
    - `PrintGuard.py -h` → Affiche l’historique des ajouts/suppressions des imprimantes
    - `PrintGuard.py -update-mdate <IP> <AAAA-MM-JJ>` → Met à jour la date de maintenance d’une imprimante

    **Dépannage**
    - `PrintGuard.py -repair <IP> <type_intervention> <AAAA-MM-JJ> "<description>" <technicien>` → Enregistre un dépannage
    - `PrintGuard.py -hh <IP>` → Affiche l’historique des dépannages d’une imprimante
    """
        )


# 2- Actions SNMP et rapports

class PrinterSNMP:
    """Classe pour gérer les interactions SNMP avec les imprimantes."""
    
    def __init__(self, ip: str, community: str = "public", port: int = 161):
        self.ip = ip
        self.community = community
        self.port = port
    
    async def _snmp_get(self, oid: str):
        """Méthode générique pour envoyer une requête SNMP GET."""
        data = ObjectType(ObjectIdentity(oid))
        transport = await UdpTransportTarget.create((self.ip, self.port))
        
        g = get_cmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            transport,
            ContextData(),
            data
        )
        errorIndication, errorStatus, errorIndex, varBinds = await g
        return errorIndication, varBinds
    
    #2.1. Générer un rapport
    '''En cours de développement'''

    
    #2.2.  Voir le statut d'une imprimante

    ''' Vérifie l'état des imprimantes puis contitut un message
    relatif à l'état des imprimantes qu'il met dans le rapport '''

    async def check_status(self):
        """Vérifie l'état de l'imprimante."""
        oid = "1.3.6.1.2.1.25.3.5.1.1.1"
        error, varBinds = await self._snmp_get(oid)
        
        if error:
            print(f"Erreur SNMP : {error}")
            return None
        
        status = varBinds[0][1].prettyPrint()
        states = {
            "1": "En veille",
            "2": "État indéterminé",
            "3": "Prête",
            "4": "En cours d'impression",
            "5": "En réchauffement"
        }
        return states.get(status, "Non accessible")

    #2.3. Afficher les alertes
    '''En cours de développment'''

    #2.4.  Voir le niveau de cartouche
    '''En cours de développment'''

    #2.5. Voir le niveau de papier

    ''' Check les taches en temps réel et lorsque le nombre de pages 
    d'une tache dépasse 200, envoies une alerte '''

    async def check_paper_level(self):
            """
            Vérifie le niveau de papier et retourne un message d'alerte si le bac est presque vide.
            L'OID est à vérifier et les valeurs de sorties de l'OID sont à vérifier
            """
            oid = "1.3.6.1.2.1.43.8.2.1.11.1.1"
            error, varBinds = await self._snmp_get(oid)
            
            if error or not varBinds:
                return "Erreur lors de la récupération du niveau de papier."
            
            level = varBinds[0][1].prettyPrint()
            if level == "9":
                return "Le bac de papier est presque vide. Veuillez en rajouter !"
            return f"Niveau de papier normal : {level}"
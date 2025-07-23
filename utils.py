''' ce module contiendra toutes les actions a faire (se trouvant dans le
module cli.py en passantn les arguments au script sauf les actions sur
 la BD qui se trouveront dans le module manage_db'''


# 1- Arguments de base

#1.1. Pour -info
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

#2.1. Générer un rapport
'''En cours de développement'''

#2.2.  Voir le statut d'une imprimante
'''En cours de développment'''

#2.3. Afficher les alertes
'''En cours de développment'''

#2.4.  Voir le niveau de cartouche
'''En cours de développment'''

#2.5. Voir le niveau de papier
'''En cours de développement'''
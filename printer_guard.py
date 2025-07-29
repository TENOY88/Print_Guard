from typing import Dict, Callable, List, Optional
import asyncio
from manage_db import DatabaseManager
from utils import PrinterSNMP, HelpDisplay


''' Le script doit etre lancé chaque heure et doit envoyer un rapport contenant
l'état des imprimantes (nom, IP, modèle, statut) ; '
'Le niveau de papier dans les imprimantes ; Etat des cartouches en considérant 
le nombre de pages restants à imprimer et la date de la dernière maintenance préventive
et les alertes sur chaque imprimante '''

'''Le script doit s'exécuter à 7h00 et démarrer 
l'imprimante à  travers une prise connectée '''

'''Le script doit s'exécuter à 22h00 et arrêter 
l'imprimante à  travers une prise connectée '''

'''Penser à enrégister aussi les IP des prises connectées dans les BD correspondant à
chaque imprimante (dans la table imprimante) --> Trouver donc une prise connectée
détachable pour les tests'''

''' Penser à Pouvoir enregistrer l’historique des alertes de façons journalières sur une imprimante dans la BD (avec la table alertes) 
et auusi à Pouvoir avoir l’historique des alertes sur une imprimante pour une date donnée
'''

class PrintGuard:
    """Classe principale pour la gestion des commandes et de la logique métier."""
    
    def __init__(self, db_config: Dict[str, str] = None):
        """
        Initialise avec une configuration optionnelle de base de données.
        
        Args:
            db_config: Dictionnaire de configuration MySQL (host, user, password, database)
        """
        self.db_manager = DatabaseManager(**(db_config or {}))
        
        self.snmp_handler = PrinterSNMP
        self.command_handlers = self._setup_command_handlers()

    def _setup_command_handlers(self) -> Dict[str, Callable]:
        """Mappe chaque commande CLI à sa méthode de traitement."""
        return {
            # Aide
            # Commandes sans paramètre
        '-info': (self._display_info, 0),  # 0 = aucun argument attendu
        '-help': (self._display_help, 0),
        
        # Commandes avec IP obligatoire
        '-report': (self._generate_report, 1),  # 1 = IP requise
        '-status': (self._check_printer_status, 1),
        '-paper': (self._check_paper_level, 1),
        
        # Commandes spéciales
        '-l': (self._list_printers, 0),  # Liste toutes les imprimantes
        '-a': (self._add_printer, 3),    # Requiert IP, nom ET modèle
        '-r': (self._remove_printer, 1),   # Requiert IP
        '-h': (self._display_full_history,0), #historique d'ajout et de supression des imprimantes
        '-repair': (self._record_maintenance, 1), #enregistrer une imprimante
        '-hh': (self._display_maintenance_history, 1),#voir l'historique de maintenace pour une imprimante
        '-mh': (self._display_maintenance_histories, 0) #voir l'historique de maintenace pour toutes les imprimantes
        }

    async def execute_command(self, args: List[str]) -> None:
        """
        Route les arguments CLI vers les handlers appropriés.
        
        Args:
            args: Liste des arguments passés au script (sans le nom du script)
        """
        if not args or args[0] in ('-info', '-help'):
            return self.command_handlers[args[0] if args else '-info'][0]()

        command = args[0]
        if command not in self.command_handlers:
            print(f"Commande inconnue: {command}")
            return self._display_help()

        handler, required_args = self.command_handlers[command]

        # Vérification du nombre d'arguments
        if len(args[1:]) < required_args:
            print(f"Erreur: {command} requiert {required_args} argument(s)")
            return self._display_help()

        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(args[1:])
            else:
                handler(args[1:])
        except Exception as e:
            print(f"Erreur: {str(e)}")

    # --------------------------------------------------------------------------
    # Méthodes de commandes
    # --------------------------------------------------------------------------

    # Aide
    def _display_info(self) -> None:
        """Affiche les informations générales (-info)"""
        HelpDisplay.afficher_info()

    def _display_help(self) -> None:
        """Affiche l'aide rapide (-help)"""
        HelpDisplay.print_help()

    # Supervision
    async def _generate_report(self, args: List[str]) -> None:
        """Génère un rapport (-report [IP])"""
        if args:
            await self._generate_printer_report(args[0])
        else:
            await self._generate_full_report()

    async def _generate_full_report(self) -> None:
        """Rapport complet pour toutes les imprimantes"""
        printers = self.db_manager.get_printer_ips()
        if not printers:
            print("Aucune imprimante trouvée.")
            return

        tasks = []
        for name, ip in printers:
            tasks.append(self._generate_printer_report(ip, name))
        
        await asyncio.gather(*tasks)

    async def _generate_printer_report(self, ip: str, name: Optional[str] = None) -> None:
        """Génère un rapport pour une imprimante spécifique"""
        printer = self.snmp_handler(ip)
        name_display = name or ip
        
        print(f"\n[=== Rapport pour {name_display} ===]")
        print(f"- Statut: {await printer.check_status()}")
        print(f"- Niveau papier: {await printer.check_paper_level()}")
        # ... autres vérifications ...

    async def _check_printer_status(self, args: List[str]) -> None:
        """Vérifie le statut d'une imprimante (-status <IP>)"""
        if not args:
            raise ValueError("L'adresse IP est requise")
        
        printer = self.snmp_handler(args[0])
        status = await printer.check_status()
        print(f"Statut: {status}")

    async def _check_paper_level(self, args: List[str]) -> None:
        """Vérifie le niveau de papier (-paper <IP>)"""
        if not args:
            raise ValueError("L'adresse IP est requise")
        
        printer = self.snmp_handler(args[0])
        level = await printer.check_paper_level()
        print(level)


    # Gestion BD
    def _list_printers(self, _: List[str]) -> None:
        """Liste toutes les imprimantes (-l)"""
        printers = self.db_manager.get_printer_ips()
        for name, ip in printers:
            print(f"{name}: {ip}")

    def _add_printer(self, args: List[str]) -> None:
        """Ajoute une imprimante (-a <IP> <nom> <modèle>)"""
        if len(args) < 3:
            raise ValueError("Format: -a <IP> <nom> <modèle>")
        
        ip, name, model = args[:3]
        # Implémentation de l'ajout à la BD
        print(f"Imprimante {name} ({ip}) ajoutée avec succès.")

    def _remove_printer(self, args: List[str]) -> None:
        """Supprime une imprimante (-r <IP>)"""
        if not args:
            raise ValueError("L'adresse IP est requise")
        
        ip = args[0]
        # Implémentation de la suppression
        print(f"Imprimante {ip} supprimée.")

    
    def _display_full_history(self, _: List[str]) -> None:
        """Affiche l'historique complet (-h)"""
        history = self.db_manager.get_full_history()
        if not history:
            print("Aucun historique trouvé")
            return
        
        print("\nHISTORIQUE COMPLET")
        print("="*50)
        for entry in history:
            print(f"{entry['date_historique']} - {entry['description']}")


    async def _record_maintenance(self, args: List[str]) -> None:
        """Handler pour -repair (maintenance)"""
        if len(args) < 5:
            print("Usage: -repair <IP> <type> <date> \"<description>\" <technicien>")
            return
        
        ip = args[0]
        maint_type = args[1]
        date = args[2]
        description = args[3]
        technician = " ".join(args[4:])
        
        if self.db_manager.add_maintenance(ip, maint_type, date, description, technician):
            print("✅ Maintenance enregistrée avec succès")
        else:
            print("❌ Échec de l'enregistrement")


    async def _display_maintenance_history(self, args: List[str]) -> None:
        """Handler pour -hh (historique maintenance)"""
        if not args:
            print("Usage: -hh <IP>")
            return
        
        ip = args[0]
        history = self.db_manager.get_maintenance_history(ip)
        
        if not history:
            print(f"Aucun historique de maintenance pour {ip}")
            return
        
        print(f"\nHISTORIQUE MAINTENANCE - {ip}")
        print("="*50)
        for entry in history:
            print(f"\nDate: {entry['date_maintenance']}")
            print(f"Type: {entry['type_maintenance']}")
            print(f"Technicien: {entry['nom_technicien']}")
            print(f"Description: {entry['description']}")
            print("-"*50)

    async def _display_maintenance_histories(self) -> None:
        """Handler pour -mh (historique maintenance)"""

        history = self.db_manager.get_full_history()
        
        if not history:
            print(f"Aucun historique de maintenance ")
            return
        
        print(f"\nHISTORIQUE MAINTENANCE")
        print("="*50)
        for entry in history:
            print(f"\nDate: {entry['date_maintenance']}")
            print(f"Type: {entry['type_maintenance']}")
            print(f"Technicien: {entry['nom_technicien']}")
            print(f"Description: {entry['description']}")
            print("-"*50)

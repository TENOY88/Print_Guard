''' Requêtes et actions (ajout, supression, mise à jour...) d'imprimante dans la
 base de données avec les paramétrages du script
 Gestion de l'enrégistrement de l'historique dans la BD
'''

'''Ajouts: Voir la possibilité d'ajout de la date d'achat et de la salle d'une imprimante
dans la table imprimante'''

import mysql.connector
from typing import List, Tuple
from typing import Dict, Optional, Any
from datetime import datetime
class DatabaseManager:
    def __init__(self, host: str = "localhost", user: str = "root", 
                 password: str = "", database: str = "print_guard_db"):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }


    def _validate_ip(self, ip: str) -> bool:
        """Valide le format d'une adresse IP"""
        import re
        pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        return re.match(pattern, ip) is not None
    


    def get_printer_ips(self) -> List[Tuple[str, str]]:
        """Récupère toutes les imprimantes (nom, ip) de la base de données"""
        try:
            with mysql.connector.connect(**self.config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT nom, address_ip FROM imprimante")
                    return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erreur de base de données: {err}")
            return []


    def display_printers(self) -> None:
        """Affiche la liste des imprimantes de manière lisible"""
        printers = self.get_printer_ips()
        
        if not printers:
            print("Aucune imprimante trouvée dans la base de données.")
            return
        
        print("\nListe des imprimantes:")
        print("-" * 40)
        print(f"{'Nom':<20} | {'Adresse IP':<15}")
        print("-" * 40)
        
        for name, ip in printers:
            print(f"{name:<20} | {ip:<15}")
        
        print("-" * 40)
        print(f"Total: {len(printers)} imprimante(s)\n")

    
    def add_printer(self, ip: str, name: str, model: str) -> bool:
        """
        Ajoute une nouvelle imprimante dans la base de données avec vérifications complètes.
        
        Args:
            ip: Adresse IP de l'imprimante (format xxx.xxx.xxx.xxx)
            name: Nom convivial de l'imprimante (max 50 caractères)
            model: Modèle de l'imprimante (max 50 caractères)
        
        Returns:
            bool: True si l'ajout a réussi, False en cas d'échec
        
        Raises:
            ValueError: Si les paramètres sont invalides
        """
        # Validation des entrées
        if not self._validate_ip(ip):
            raise ValueError("Format d'IP invalide (ex: 192.168.1.1)")
        
        if not name or len(name) > 50:
            raise ValueError("Le nom doit contenir entre 1 et 50 caractères")
        
        if not model or len(model) > 50:
            raise ValueError("Le modèle doit contenir entre 1 et 50 caractères")

        try:
            with mysql.connector.connect(**self.config) as conn:
                with conn.cursor() as cursor:
                    # Vérification de l'existence de l'imprimante
                    cursor.execute(
                        "SELECT id FROM imprimante WHERE address_ip = %s OR nom = %s",
                        (ip, name)
                    )
                    if cursor.fetchone():
                        print(f"⚠️ Attention : Une imprimante avec cette IP ou ce nom existe déjà")
                        return False

                    # Insertion sécurisée
                    cursor.execute(
                        """INSERT INTO imprimante 
                        (address_ip, nom, modele) 
                        VALUES (%s, %s, %s)""",
                        (ip, name.strip(), model.strip())
                    )
                    conn.commit()
                    
                    print(f"✅ Imprimante '{name}' ({ip}) ajoutée avec succès")
                    return True

        except mysql.connector.Error as err:
            print(f"❌ Erreur base de données : {err}")
            return False
        

    def remove_printer(self, ip: str) -> bool:
        """
        Supprime une imprimante de la base de données après vérification de son existence.
        
        Args:
            ip (str): Adresse IP de l'imprimante à supprimer
        
        Returns:
            bool: 
                - True si la suppression a réussi
                - False si l'imprimante n'existe pas ou en cas d'erreur
        
        Raises:
            ValueError: Si l'adresse IP est invalide
        """
        # Validation du format IP
        if not self._validate_ip(ip):
            raise ValueError(f"Adresse IP invalide : {ip}")

        try:
            with mysql.connector.connect(**self.config) as conn:
                with conn.cursor() as cursor:
                    # Vérification préalable de l'existence
                    cursor.execute(
                        "SELECT id FROM imprimante WHERE address_ip = %s", 
                        (ip,)
                    )
                    if not cursor.fetchone():
                        print(f"⚠️ Aucune imprimante trouvée avec l'IP {ip}")
                        return False

                    # Exécution de la suppression
                    cursor.execute(
                        "DELETE FROM imprimante WHERE address_ip = %s",
                        (ip,)
                    )
                    conn.commit()
                    
                    # Vérification que la suppression a bien pris effet
                    if cursor.rowcount == 1:
                        print(f"✅ Imprimante {ip} supprimée avec succès")
                        return True
                    
                    print(f"❌ Échec inattendu lors de la suppression de {ip}")
                    return False

        except mysql.connector.Error as err:
            print(f"❌ Erreur base de données lors de la suppression : {err}")
            return False
        

    def get_printer_details(self, ip: str) -> Optional[Dict[str, str]]:
        """
        Récupère les informations de base d'une imprimante sous forme de dictionnaire.
        
        Args:
            ip (str): Adresse IP valide de l'imprimante (format xxx.xxx.xxx.xxx)
        
        Returns:
            Optional[Dict[str, str]]: 
                - Dictionnaire avec les clés 'name', 'model', 'ip' si trouvé
                - None si l'imprimante n'existe pas ou en cas d'erreur
        
        Raises:
            ValueError: Si l'adresse IP est invalide
        """
        if not self._validate_ip(ip):
            raise ValueError(f"Format d'IP invalide : {ip} (format attendu : xxx.xxx.xxx.xxx)")

        try:
            with mysql.connector.connect(**self.config) as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        """SELECT 
                            nom AS name,
                            modele AS model,
                            address_ip AS ip
                        FROM imprimante 
                        WHERE address_ip = %s""",
                        (ip,)
                    )
                    
                    result = cursor.fetchone()
                    
                    if not result:
                        print(f"[INFO] Aucune imprimante trouvée avec l'IP {ip}")
                        return None
                    
                    return result

        except mysql.connector.Error as err:
            print(f"[ERREUR] Impossible de récupérer les détails : {err}")
            return None
        
    # HISTORIQUE
    def add_history_entry(self, printer_id: int, description: str) -> bool:
        """Ajoute une entrée dans l'historique"""
        try:
            with mysql.connector.connect(**self.config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO historique (imprimante_id, date_historique, description) "
                        "VALUES (%s, CURDATE(), %s)",
                        (printer_id, description)
                    )
                    conn.commit()
                    return True
        except mysql.connector.Error as err:
            print(f"Erreur historique: {err}")
            return False

    def get_printer_history(self, ip: str) -> List[Dict[str, str]]:
        """Récupère l'historique d'une imprimante"""
        try:
            with mysql.connector.connect(**self.config) as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        """SELECT h.date_historique, h.description 
                        FROM historique h
                        JOIN imprimante i ON h.imprimante_id = i.id
                        WHERE i.address_ip = %s
                        ORDER BY h.date_historique DESC""",
                        (ip,)
                    )
                    return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erreur historique: {err}")
            return []

    # MAINTENANCE
    def add_maintenance(self, ip: str, maintenance_type: str, date: str, 
                      description: str, technician: str) -> bool:
        """Enregistre une intervention de maintenance"""
        try:
            maint_date = datetime.strptime(date, "%Y-%m-%d").date()
            with mysql.connector.connect(**self.config) as conn:
                with conn.cursor() as cursor:
                    # Récupère l'ID de l'imprimante
                    cursor.execute(
                        "SELECT id FROM imprimante WHERE address_ip = %s", 
                        (ip,)
                    )
                    printer = cursor.fetchone()
                    if not printer:
                        return False

                    cursor.execute(
                        """INSERT INTO maintenance 
                        (imprimante_id, date_maintenance, description, 
                        nom_technicien, type_maintenance)
                        VALUES (%s, %s, %s, %s, %s)""",
                        (printer[0], maint_date, description, 
                         technician, maintenance_type)
                    )
                    conn.commit()
                    return True
        except ValueError:
            print("Format de date invalide (utilisez AAAA-MM-JJ)")
            return False
        except mysql.connector.Error as err:
            print(f"Erreur maintenance: {err}")
            return False

    def get_maintenance_history(self, ip: str) -> List[Dict[str, str]]:
        """Récupère l'historique des maintenances"""
        try:
            with mysql.connector.connect(**self.config) as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        """SELECT m.date_maintenance, m.type_maintenance, 
                        m.description, m.nom_technicien
                        FROM maintenance m
                        JOIN imprimante i ON m.imprimante_id = i.id
                        WHERE i.address_ip = %s
                        ORDER BY m.date_maintenance DESC""",
                        (ip,)
                    )
                    return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erreur maintenance: {err}")
            return []
        
    
    def get_full_history(self) -> List[Dict[str, str]]:
        """Récupère tout l'historique"""
        try:
            with mysql.connector.connect(**self.config) as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        """SELECT i.address_ip AS ip, h.date_historique, 
                        h.description 
                        FROM historique h
                        JOIN imprimante i ON h.imprimante_id = i.id
                        UNION
                        SELECT i.address_ip AS ip, m.date_maintenance AS date_historique,
                        CONCAT('[MAINTENANCE] ', m.description) AS description
                        FROM maintenance m
                        JOIN imprimante i ON m.imprimante_id = i.id
                        ORDER BY date_historique DESC"""
                    )
                    return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erreur historique complet: {err}")
            return []


# Exemple d'utilisation
if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.display_printers()

  
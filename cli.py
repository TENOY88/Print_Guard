import argparse

def get_parser():
    parser = argparse.ArgumentParser(description="Supervision et gestion des imprimantes")

    # 1- Arguments de base
    parser.add_argument('-info', action='store_true',
                        help="Afficher une présentation générale du script et des arguments")
    parser.add_argument('-help', action='store_true',
                        help="Afficher la liste des arguments avec leurs actions respectives")

    # 2- Actions SNMP et rapports
    parser.add_argument('-report', nargs='?', const=True,
                        help="Générer un rapport général ou pour une imprimante spécifique")
    parser.add_argument('-status', metavar='<IP>', help="Voir le statut d'une imprimante donnée")
    parser.add_argument('-alerts', metavar='<IP>', help="Voir les alertes en cours pour une imprimante donnée")
    parser.add_argument('-cartbridge', metavar='<IP>', help="Voir le niveau de cartouche de l'imprimante")
    parser.add_argument('-paper', metavar='<IP>', help="Voir le niveau de papier de l'imprimante")
    parser.add_argument('-maintenance', metavar='<IP>',
                        help="Voir la dernière date de maintenance pour une imprimante donnée")
    parser.add_argument('-start', metavar='<IP>', help="Démarrer une imprimante donnée")
    parser.add_argument('-stop', metavar='<IP>', help="Arrêter une imprimante donnée")

    # 3- Actions sur la base de données
    parser.add_argument('-l', action='store_true', help="Afficher la liste des imprimantes dans la BD")
    parser.add_argument('-a', nargs=3, metavar=('<IP>', '<Nom>', '<Modèle>'), help="Ajouter une imprimante à la BD")
    parser.add_argument('-r', metavar='<IP>', help="Supprimer une imprimante de la BD")
    parser.add_argument('-i', metavar='<IP>', help="Afficher les infos d'une imprimante")
    parser.add_argument('--history', action='store_true',
                        help="Afficher l'historique d'ajout et suppression des imprimantes")
    parser.add_argument('-update-mdate', nargs=2, metavar=('<IP>', '<date>'),
                        help="Mettre à jour la date de maintenance préventive")

    # 4- Dépannage (fait parti aussi des actions sur la BD)
    parser.add_argument('-repair', nargs=5,
                        metavar=('<IP>', '<type_intervention>', '<date>', '<description>', '<technicien>'),
                        help="Enregistrer un dépannage pour une imprimante")
    parser.add_argument('-hh', metavar='<IP>', help="Voir l'historique des dépannages pour une imprimante donnée")

    return parser


def parse_arguments():
    parser = get_parser()
    args = parser.parse_args()
    return args





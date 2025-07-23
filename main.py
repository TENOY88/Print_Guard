import cli
import utils

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

def main():

    args = cli.parse_arguments()

 # Actions en fonction des arguments
    if args.info:
        utils.afficher_info()
    elif args.help:
        utils.print_help()
    elif args.report:
        rapport_imprimante()
    elif args.status:
        print(f" Statut de l'imprimante {args.status}")
    elif args.alerts:
        print(f" Afficher les alertes pour l'imprimante {args.alerts}")
    elif args.history:
        print(f" Afficher l'historique des événements pour l'imprimante {args.history}")
    elif args.cartbridge:
        print(f" Niveau de cartouche pour l'imprimante {args.cartbridge}")
    elif args.paper:
        print(f" Niveau de papier pour l'imprimante {args.paper}")
    elif args.maintenance:
        print(f" Dernière maintenance pour l'imprimante {args.maintenance}")
    elif args.start:
        print(f" Démarrer l'imprimante {args.start}")
    elif args.stop:
        print(f" Arrêter l'imprimante {args.stop}")
    elif args.l:
        afficher_l_imprimantes()
    elif args.a:
        print(f" Ajouter imprimante {args.a[0]} - Nom: {args.a[1]} - Modèle: {args.a[2]}")
    elif args.r:
        print(f" Supprimer l'imprimante {args.r}")
    elif args.i:
        print(f" Infos pour l'imprimante {args.i}")
    elif args.history:
        print(" Historique des ajouts et suppressions des imprimantes")
    elif args.update_mdate:
        print(
            f" Mettre à jour la date de maintenance pour l'imprimante {args.update_mdate[0]} - Date: {args.update_mdate[1]}")
    elif args.repair:
        print(
            f" Enregistrer un dépannage pour l'imprimante {args.repair[0]} avec intervention: {args.repair[1]} le {args.repair[2]} Description: {args.repair[3]} Technicien: {args.repair[4]}")
    elif args.hh:
        print(f" Historique des dépannages pour l'imprimante {args.hh}")
    else:
        print(" Aucun argument valide fourni.")


if __name__ == "__main__":
    main()

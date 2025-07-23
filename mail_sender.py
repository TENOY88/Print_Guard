# --------------------- 
# Créer un message email unique

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage



def send_alert_mail(adresse_email_exp, mot_de_passe_email, adresse_email_dest, reseau_a_scanner, alert_lines):
    message = MIMEMultipart()
    message["From"] = adresse_email_exp  # Remplacer par votre adresse email
    message["To"] = adresse_email_dest  # Remplacer par l'adresse email du destinataire
    message["Subject"] = f"Alertes scan nmap : {reseau_a_scanner}"

# Définir le corps du message avec les alertes accumulées
    corps_message = f" \U0001F6A8 \U0001F6A8 Les machines intruses ci-dessous viennent de se connecter à votre réseau:\n{''.join(alert_lines)}"
    message.attach(MIMEText(corps_message, "plain"))

# Connexion au serveur SMTP de Google (remplacer si fournisseur différent)
    with smtplib.SMTP("smtp.gmail.com", 587) as serveur_smtp:
        serveur_smtp.starttls()
        serveur_smtp.login(adresse_email_exp, mot_de_passe_email)  # Remplacer par votre mot de passe
        serveur_smtp.sendmail(adresse_email_exp, adresse_email_dest, message.as_string())
        print("Alertes envoyées par email avec succès.")
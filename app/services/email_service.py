import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings


class EmailService:
    """Service pour envoyer des emails via Gmail SMTP"""

    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = settings.SMTP_EMAIL
        self.sender_password = settings.SMTP_PASSWORD

    def send_otp_email(self, to_email: str, otp_code: str) -> bool:
        """
        Envoie un email avec le code OTP

        Args:
            to_email: L'adresse email du destinataire
            otp_code: Le code OTP à 6 chiffres

        Returns:
            True si l'email a été envoyé avec succès, False sinon
        """
        try:
            # Créer le message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Votre code de vérification OTP"
            message["From"] = self.sender_email
            message["To"] = to_email

            # Contenu de l'email en HTML
            html_content = f"""
            <html>
              <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                  <h1 style="color: #333; text-align: center; margin-bottom: 30px;">Code de vérification OTP</h1>

                  <p style="color: #666; font-size: 16px; line-height: 1.6;">
                    Bonjour,
                  </p>

                  <p style="color: #666; font-size: 16px; line-height: 1.6;">
                    Voici votre code de vérification pour vous connecter :
                  </p>

                  <div style="background-color: #4a90e2; color: white; font-size: 32px; font-weight: bold; text-align: center; padding: 20px; border-radius: 8px; margin: 30px 0; letter-spacing: 8px;">
                    {otp_code}
                  </div>

                  <p style="color: #666; font-size: 14px; line-height: 1.6;">
                    Ce code est valable pendant <strong>5 minutes</strong>.
                  </p>

                  <p style="color: #999; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                    Si vous n'avez pas demandé ce code, ignorez simplement cet email.
                  </p>

                  <p style="color: #999; font-size: 12px;">
                    Cordialement,<br>
                    L'équipe LogPages
                  </p>
                </div>
              </body>
            </html>
            """

            # Contenu de l'email en texte brut (fallback)
            text_content = f"""
            Code de vérification OTP

            Bonjour,

            Voici votre code de vérification pour vous connecter :

            {otp_code}

            Ce code est valable pendant 5 minutes.

            Si vous n'avez pas demandé ce code, ignorez simplement cet email.

            Cordialement,
            L'équipe LogPages
            """

            # Attacher les deux versions
            part1 = MIMEText(text_content, "plain")
            part2 = MIMEText(html_content, "html")
            message.attach(part1)
            message.attach(part2)

            # Connexion et envoi
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Sécuriser la connexion
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            print(f"[SUCCESS] Email sent to {to_email}")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to send email to {to_email}: {str(e)}")
            return False


# Singleton instance
email_service = EmailService()

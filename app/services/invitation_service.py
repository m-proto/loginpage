import json
from pathlib import Path
from typing import List


class InvitationService:
    """Service pour gérer les invitations utilisateurs"""

    def __init__(self):
        self.data_file = Path("app/data/invited_users.json")

    def is_invited(self, email: str) -> bool:
        """
        Vérifie si un email est dans la liste des invités

        Args:
            email: L'adresse email à vérifier

        Returns:
            True si l'email est invité, False sinon
        """
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            invited_emails = data.get("invited_emails", [])

            # Comparaison insensible à la casse
            return email.lower() in [e.lower() for e in invited_emails]

        except FileNotFoundError:
            print(f"[WARNING] Invitation file not found: {self.data_file}")
            return False
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON in invitation file")
            return False

    def get_all_invited_emails(self) -> List[str]:
        """Retourne la liste de tous les emails invités"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("invited_emails", [])
        except:
            return []

    def add_invited_email(self, email: str) -> bool:
        """
        Ajoute un email à la liste des invités

        Args:
            email: L'adresse email à ajouter

        Returns:
            True si ajouté avec succès, False sinon
        """
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            invited_emails = data.get("invited_emails", [])

            # Éviter les doublons
            if email.lower() not in [e.lower() for e in invited_emails]:
                invited_emails.append(email)
                data["invited_emails"] = invited_emails

                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                return True

            return False
        except:
            return False


# Singleton instance
invitation_service = InvitationService()

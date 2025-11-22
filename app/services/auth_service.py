import httpx
from fastapi import HTTPException
from app.config import settings


class AuthService:
    """Service d'authentification avec Keycloak"""

    async def get_token_from_keycloak(self, email: str) -> dict:
        """
        Récupère les tokens depuis Keycloak via Direct Access Grant

        Args:
            email: L'adresse email de l'utilisateur

        Returns:
            dict: Réponse de Keycloak contenant access_token, refresh_token, id_token, etc.

        Raises:
            HTTPException: Si l'obtention du token échoue
        """
        token_url = f"{settings.KEYCLOAK_BASE_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"

        data = {
            "grant_type": "password",
            "client_id": settings.KEYCLOAK_CLIENT_ID,
            "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
            "username": email,
            "password": settings.KEYCLOAK_DUMMY_PASSWORD,
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(token_url, data=data)

        if resp.status_code != 200:
            print(f"[ERROR] Keycloak token error: {resp.status_code} - {resp.text}")
            raise HTTPException(
                status_code=401,
                detail="Impossible d'obtenir le token depuis Keycloak"
            )

        return resp.json()


# Singleton instance
auth_service = AuthService()

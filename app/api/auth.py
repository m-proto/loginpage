from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.services.auth_service import auth_service
from app.services.otp_service import otp_service
from app.services.invitation_service import invitation_service
from app.services.email_service import email_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


class SendOtpRequest(BaseModel):
    """Request model pour l'envoi d'OTP"""
    email: EmailStr


class VerifyOtpRequest(BaseModel):
    """Request model pour la vérification d'OTP"""
    email: EmailStr
    code: str


@router.post("/send-otp")
async def send_otp(request: SendOtpRequest):
    """
    Envoie un code OTP à l'email fourni

    - Vérifie que l'email est dans la liste des invités
    - Génère un code OTP à 6 chiffres
    - Envoie le code par email
    - Le code est valide pendant 5 minutes
    """
    # Vérification : L'email est-il autorisé ?
    if not invitation_service.is_invited(request.email):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cet email n'est pas autorisé à utiliser ce service. Veuillez contacter l'administrateur pour obtenir une invitation.",
        )

    # Générer et stocker l'OTP
    otp = otp_service.generate_otp()
    otp_service.store_otp(request.email, otp)

    # Envoyer l'email
    email_sent = email_service.send_otp_email(request.email, otp)

    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'envoi de l'email. Vérifiez votre configuration SMTP.",
        )

    return {"ok": True, "message": f"Code OTP envoyé à {request.email}"}


@router.post("/verify-otp")
async def verify_otp(request: VerifyOtpRequest):
    """
    Vérifie le code OTP et retourne les tokens Keycloak

    - Vérifie que le code OTP est valide
    - Vérifie que l'email est toujours autorisé
    - Récupère les tokens depuis Keycloak
    - Retourne access_token, refresh_token, id_token, etc.
    """
    # Vérifier l'OTP
    is_valid = otp_service.verify_otp(request.email, request.code)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code OTP invalide ou expiré",
        )

    # Double vérification : L'email est-il toujours autorisé ?
    if not invitation_service.is_invited(request.email):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cet email n'est pas autorisé à utiliser ce service.",
        )

    # Récupérer les tokens depuis Keycloak
    token_response = await auth_service.get_token_from_keycloak(request.email)

    return token_response

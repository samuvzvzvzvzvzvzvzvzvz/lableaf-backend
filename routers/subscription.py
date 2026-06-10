from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth_utils import verificar_token
from database import supabase

router = APIRouter(prefix="/api")
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario_id = verificar_token(token)
    if not usuario_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    result = supabase.table("usuarios").select("id, plano").eq("id", usuario_id).single().execute()
    if result.error or not result.data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")

    return result.data


@router.get("/subscription")
def subscription(usuario: dict = Depends(get_current_user)):
    plan = usuario.get("plano", "gratuito")
    tokens = 100 if plan == "gratuito" else 1000
    return {
        "subscription": {
            "active": True,
            "plan": plan,
            "tokens_remaining": tokens,
        }
    }

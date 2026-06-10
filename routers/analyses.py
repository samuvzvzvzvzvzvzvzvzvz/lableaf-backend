from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth_utils import verificar_token
from database import supabase

router = APIRouter(prefix="/api")
security = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario_id = verificar_token(token)
    if not usuario_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return usuario_id


@router.post("/analyses")
async def create_analysis(
    classe: str = Form(...),
    confianca: Optional[float] = Form(None),
    recomendacao: Optional[str] = Form(None),
    imagem_resultado: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    usuario_id: str = Depends(get_current_user_id),
):
    payload = {
        "usuario_id": usuario_id,
        "classe": classe,
        "confianca": confianca,
        "recomendacao": recomendacao,
        "imagem_resultado": imagem_resultado,
    }

    try:
        result = supabase.table("analises").insert(payload).execute()
        if result.error or not result.data:
            return {"id": None}
        record = result.data[0]
        return {"id": record.get("id")}
    except Exception:
        return {"id": None}

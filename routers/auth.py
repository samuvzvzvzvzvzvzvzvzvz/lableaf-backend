from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

from auth_utils import criar_token, verificar_token
from database import supabase
from schemas import UsuarioCadastro, UsuarioLogin

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def resposta_auth(token: str, usuario: dict):
    return {
        "token": token,
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "nome": usuario.get("nome", ""),
            "email": usuario.get("email", ""),
        },
    }


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario_id = verificar_token(token)
    if not usuario_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    result = supabase.table("usuarios").select("id, nome, email, plano").eq("id", usuario_id).single().execute()
    if result.error or not result.data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")

    return result.data


@router.post("/cadastro", status_code=201)
@router.post("/api/auth/register", status_code=201)
def cadastrar(dados: UsuarioCadastro):
    existente = supabase.table("usuarios").select("id").eq("email", dados.email).execute()
    if existente.data:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    senha_hash = pwd_context.hash(dados.senha)
    result = supabase.table("usuarios").insert(
        {
            "nome": dados.nome,
            "email": dados.email,
            "senha_hash": senha_hash,
            "plano": "gratuito",
        }
    ).execute()

    if result.error or not result.data:
        raise HTTPException(status_code=500, detail="Erro ao criar usuário")

    usuario = result.data[0]
    token = criar_token(str(usuario.get("id")))
    return resposta_auth(token, usuario)


@router.post("/login")
@router.post("/api/auth/login")
def login(dados: UsuarioLogin):
    result = supabase.table("usuarios").select("id, nome, email, senha_hash, plano").eq("email", dados.email).execute()
    if not result.data:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

    usuario = result.data[0]
    if not pwd_context.verify(dados.senha, usuario["senha_hash"]):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

    token = criar_token(str(usuario.get("id")))
    return resposta_auth(token, usuario)


@router.post("/logout")
@router.post("/api/auth/logout")
def logout():
    return {"message": "logout realizado"}

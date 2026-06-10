from typing import Optional

from pydantic import BaseModel, EmailStr


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


class UsuarioCadastro(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    token: str
    access_token: str
    token_type: str = "bearer"
    user: dict


class AnaliseCreate(BaseModel):
    classe: str
    confianca: Optional[float] = None
    recomendacao: Optional[str] = None
    imagem_resultado: Optional[str] = None

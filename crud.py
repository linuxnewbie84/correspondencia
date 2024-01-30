from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from sqlalchemy.orm import Session
import model
from schemas.user_schema import CrearUsuario
from schemas.doc_Schema import CrearDoc
from schemas.doc_Schema import Id_Doc
from schemas.user_schema import Id_User


# Función para crear usuario
def crear(db: Session, user: CrearUsuario):
    user.set_password(user.user_password)
    usuario = model.user.User(
        name=user.name,
        cargo=user.cargo,
        username=user.username,
        user_password=user.user_password,
    )
    db.add(usuario)
    db.commit()
    db.flush(usuario)
    return usuario


# Función Crear Documento
def crearD(db: Session, doc: CrearDoc):
    new_doc = model.doc.Doc(
        fecha=doc.fecha,
        numoficio=doc.numoficio,
        asunto=doc.asunto,
        remitente=doc.remitente,
        turn=doc.turn,
        resp=doc.resp,
        femi=doc.femi,
        url=doc.url,
        urlresp=doc.urlresp,
    )
    db.add(new_doc)
    db.commit()
    db.flush(new_doc)
    return new_doc

from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy_utils import PasswordType, force_auto_coercion

from src.db.models import Base

force_auto_coercion()

class ApiUser(Base):
    __tablename__ = 'apiUser'
    __table_args__ =(
        UniqueConstraint('username'),
    )
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(PasswordType(
        schemes=[
            'sha256_crypt',
        ],
    ))
    token = Column(String(50), nullable=True) #TODO: handle cypher


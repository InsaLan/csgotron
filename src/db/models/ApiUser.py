from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import PasswordType, force_auto_coercion

from . import Base

force_auto_coercion()

class ApiUser(Base):
    __tablename__ = 'apiUser'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(PasswordType(
        schemes=[
            'sha256_crypt',
        ],
    ))
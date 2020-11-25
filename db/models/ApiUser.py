from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import PasswordType
from . import Base
class ApiUser(Base):
    __tablename__ = 'apiUser'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(PasswordType(
        schemes=[
            'sha256_crypt',
            'md5_crypt'#TODO: remove this in production, debug only
        ],
        deprecated=['md5_crypt']
    ))
    token = Column(String(1000), nullable=False)
"""Database models.
"""

import logging

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Float,
    MetaData,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base

from localpg.cfg import COMPOSE_PROJECT_NAME, PARENT_LOGGER, PG_CFG, get_uri_db_pg
from localpg.constants import DB_NAME, PG_PORT_DEFAULT

# We need to change this port because we need to access to PostgreSQL DB
# using the default port.
PG_CFG.update({"port": PG_PORT_DEFAULT})
ENV = COMPOSE_PROJECT_NAME.split("_")[1]


engine = create_engine(get_uri_db_pg(PG_CFG))
meta = MetaData(engine)
Base = declarative_base(metadata=meta)
logger = logging.getLogger(f"{PARENT_LOGGER}.{__name__}")


class BidmcPggRespiration(Base):
    __tablename__ = "BidmcPggRespiration"
    __schema__ = f"{DB_NAME}"

    ds = Column(
        Float,
        primary_key=True,
        nullable=False,
        comment='Processing time',
    )
    subject = Column(
        String,
        primary_key=True,
        comment='Studied subject',
    )
    resp = Column(
        Float,
        comment='Respiration',
    )
    pleth = Column(
        Float,
        comment='Plethysmograph',
    )
    v = Column(
        Float,
        comment='Anda a saber que es esta columna',
    )
    avr = Column(
        Float,
        comment='Ni idea che',
    )
    ii = Column(
        Float,
        comment='Nop',
    )


if __name__ == '__main__':
    logger.info("Creating tables..")
    Base.metadata.create_all()

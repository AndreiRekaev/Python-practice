from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey

# Base class for all entities:
class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

# Spaceship class:
class Spaceship(Base):
    __tablename__ = "spaceships"

    id: Mapped[int] = mapped_column(primary_key=True)
    alignment: Mapped[str]
    name: Mapped[str]
    type: Mapped[str]
    length: Mapped[float]
    crew_size: Mapped[int]
    armed: Mapped[bool]

# Class for officers:
class Officer(Base):
    __tablename__ = 'officers'

    id: Mapped[int] = mapped_column(primary_key=True)
    spaceship_id: Mapped[int] = mapped_column(ForeignKey('spaceships.id'))
    first_name: Mapped[str]
    last_name: Mapped[str]
    rank: Mapped[str]
    status: Mapped[str]

# Class of traitors:
class Traitor(Base):
    __tablename__ = 'traitors'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    rank: Mapped[str]

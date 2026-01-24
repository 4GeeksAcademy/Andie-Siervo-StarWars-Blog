from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    subscription_date: Mapped[str] = mapped_column(default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites: Mapped[list["User"]] = relationship(secondary="favorites", back_populates="users")



    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet (db.Model):
    _tablename_ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    climate: Mapped[str] = mapped_column(String(100), nullable=False)
    population: Mapped [int] = mapped_column(nullable=False)

    characters: Mapped[list["Character"]] = relationship(back_populates="planet")
    favorites: Mapped[list["User"]] = relationship(secondary="favorites", back_populates="users")

class Character (db.Model):
    _tablename_ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(20), nullable=False)
    lastname: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[str] = mapped_column(String(20), nullable=False)

    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    
    planet: Mapped["Planet"] = relationship(back_populates="characters")
    favorites: Mapped[list["User"]] = relationship(secondary="favorites", back_populates="users")


class Vehicles (db.Model):
    _tablename_ = "vehicles"
      
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    model: Mapped[str] = mapped_column(String(20), nullable=False)
    dateofmaking: Mapped[str] = mapped_column(default=datetime.utcnow)
    favorites: Mapped[list["User"]] = relationship(secondary="favorites", back_populates="users")

favorites = Table(
    "favorites",
    db.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("planet_id", ForeignKey("planet.id")),
    Column("character_id", ForeignKey("character.id")),
    Column("vehicles_id", ForeignKey("vehicles.id")),
)
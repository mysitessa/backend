from typing import Optional

from sqlalchemy import BigInteger, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class InitGames(Base):
    __tablename__ = 'init_games'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='init_games_pkey'),
    )

    frag_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    time_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    map_name: Mapped[str] = mapped_column(String(255), nullable=False)
    time: Mapped[str] = mapped_column(String(255), nullable=False)

    matches: Mapped[Optional['Matches']] = relationship('Matches', uselist=False, back_populates='initgame')


class Items(Base):
    __tablename__ = 'items'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='items_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    item_pickups: Mapped[list['ItemPickups']] = relationship('ItemPickups', back_populates='item')


class Weapons(Base):
    __tablename__ = 'weapons'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='weapons_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    weaponid: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    kills: Mapped[list['Kills']] = relationship('Kills', back_populates='weapon')


class Matches(Base):
    __tablename__ = 'matches'
    __table_args__ = (
        ForeignKeyConstraint(['initgame_id'], ['init_games.id'], name='fk_match_initgame'),
        PrimaryKeyConstraint('id', name='matches_pkey'),
        UniqueConstraint('initgame_id', name='matches_initgame_id_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    initgame_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    initgame: Mapped[Optional['InitGames']] = relationship('InitGames', back_populates='matches')
    clients: Mapped[list['Clients']] = relationship('Clients', back_populates='match')
    item_pickups: Mapped[list['ItemPickups']] = relationship('ItemPickups', back_populates='match')
    kills: Mapped[list['Kills']] = relationship('Kills', back_populates='match')


class Clients(Base):
    __tablename__ = 'clients'
    __table_args__ = (
        ForeignKeyConstraint(['match_id'], ['matches.id'], name='fk_client_match'),
        PrimaryKeyConstraint('id', name='clients_pkey')
    )

    clientid: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    match_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    name: Mapped[Optional[str]] = mapped_column(String(255))

    match: Mapped[Optional['Matches']] = relationship('Matches', back_populates='clients')
    events: Mapped[list['Events']] = relationship('Events', back_populates='client')
    item_pickups: Mapped[list['ItemPickups']] = relationship('ItemPickups', back_populates='client')
    kills: Mapped[list['Kills']] = relationship('Kills', foreign_keys='[Kills.killer_id]', back_populates='killer')
    kills_: Mapped[list['Kills']] = relationship('Kills', foreign_keys='[Kills.victim_id]', back_populates='victim')


class Events(Base):
    __tablename__ = 'events'
    __table_args__ = (
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='fk_event_client'),
        PrimaryKeyConstraint('id', name='events_pkey')
    )

    clientid: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    time: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    client_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='events')


class ItemPickups(Base):
    __tablename__ = 'item_pickups'
    __table_args__ = (
        ForeignKeyConstraint(['client_id'], ['clients.id'], name='fk_itempickup_client'),
        ForeignKeyConstraint(['item_id'], ['items.id'], name='fk_itempickup_item'),
        ForeignKeyConstraint(['match_id'], ['matches.id'], name='fk_itempickup_match'),
        PrimaryKeyConstraint('id', name='item_pickups_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    time: Mapped[str] = mapped_column(String(255), nullable=False)
    client_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    item_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    match_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    client: Mapped[Optional['Clients']] = relationship('Clients', back_populates='item_pickups')
    item: Mapped[Optional['Items']] = relationship('Items', back_populates='item_pickups')
    match: Mapped[Optional['Matches']] = relationship('Matches', back_populates='item_pickups')


class Kills(Base):
    __tablename__ = 'kills'
    __table_args__ = (
        ForeignKeyConstraint(['killer_id'], ['clients.id'], name='fk_kill_killer'),
        ForeignKeyConstraint(['match_id'], ['matches.id'], name='fk_kill_match'),
        ForeignKeyConstraint(['victim_id'], ['clients.id'], name='fk_kill_victim'),
        ForeignKeyConstraint(['weapon_id'], ['weapons.id'], name='fk_kill_weapon'),
        PrimaryKeyConstraint('id', name='kills_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    time: Mapped[str] = mapped_column(String(255), nullable=False)
    killer_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    match_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    victim_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    weapon_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    mod: Mapped[Optional[str]] = mapped_column(String(255))

    killer: Mapped[Optional['Clients']] = relationship('Clients', foreign_keys=[killer_id], back_populates='kills')
    match: Mapped[Optional['Matches']] = relationship('Matches', back_populates='kills')
    victim: Mapped[Optional['Clients']] = relationship('Clients', foreign_keys=[victim_id], back_populates='kills_')
    weapon: Mapped[Optional['Weapons']] = relationship('Weapons', back_populates='kills')
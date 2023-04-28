import datetime
import asyncio
from typing import Dict, Optional, Sequence

from nonebot import require
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

require("nonebot_plugin_localstore")

from nonebot_plugin_localstore import get_data_dir

data_dir = get_data_dir("abot").joinpath("place")


class DB:
    engine: AsyncEngine = None  # type: ignore

    @classmethod
    async def create_sqlite_engine(cls, bases: Optional[Sequence] = None):
        """创建sql引擎, 并添加传入的表"""
        url = data_dir.joinpath("data.db").absolute()
        url.parent.mkdir(0o755, True, True)
        engine = create_async_engine(f"sqlite+aiosqlite:///{url}", echo=False, future=True)
        cls.engine = engine

        if bases is not None:
            async with engine.begin() as conn:
                for base in bases:
                    await conn.run_sync(base.metadata.create_all)

        return True

    @classmethod
    async def ensure_engine(cls, bases: Optional[Sequence] = None):
        """获取sql引擎, 若无法获得则创建"""
        return cls.engine or await cls.create_sqlite_engine(bases)

    @classmethod
    async def get_session(cls, **kwargs):
        if not cls.engine:
            await cls.ensure_engine([PlaceHistory])
        return async_sessionmaker(cls.engine, **kwargs)()

    @classmethod
    async def async_fill_pixel(
        cls,
        member: str,
        group: str,
        new_color: int,
        chunk_x: int,
        chunk_y: int,
        pixel_x: int,
        pixel_y: int,
    ):
        session = await cls.get_session(expire_on_commit=False)
        old_pixel = (
            await session.execute(
                select(PlaceHistory)
                .where(
                    (PlaceHistory.chunk_x == chunk_x)
                    & (PlaceHistory.chunk_y == chunk_y)
                    & (PlaceHistory.pixel_x == pixel_x)
                    & (PlaceHistory.pixel_y == pixel_y)
                )
                .order_by(PlaceHistory.id.desc())
                .limit(1)
            )
        ).scalar()  # type: ignore
        old_color = old_pixel.new_color if old_pixel is not None else 1
        new_pixel = PlaceHistory(
            member=member,
            group=group,
            old_color=old_color,
            new_color=new_color,
            chunk_x=chunk_x,
            chunk_y=chunk_y,
            pixel_x=pixel_x,
            pixel_y=pixel_y,
        )
        session.add(new_pixel)
        await session.commit()
        id_ = new_pixel.id
        await session.close()

        return id_


class Base(DeclarativeBase):
    pass


class PlaceHistory(Base):
    __tablename__ = "place_histroy"
    id: Mapped[int] = mapped_column(primary_key=True)
    member: Mapped[str]
    group: Mapped[str]
    time: Mapped[Optional[datetime.datetime]] = mapped_column(default=datetime.datetime.now)
    old_color: Mapped[int]
    new_color: Mapped[int]
    chunk_x: Mapped[int]
    chunk_y: Mapped[int]
    pixel_x: Mapped[int]
    pixel_y: Mapped[int]

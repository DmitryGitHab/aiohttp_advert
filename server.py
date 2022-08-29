import json
from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.exc import IntegrityError


# router = web.RouteTableDef()
app = web.Application()


PG_DSN = "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/aiohttp_adv"
engine = create_async_engine(PG_DSN, echo=True)
Base = declarative_base()


class HTTPError(web.HTTPException):
    def __init__(self, *, headers=None, reason=None, body=None, message=None):
        json_response = json.dumps({"error": message})
        super().__init__(
            headers=headers,
            reason=reason,
            body=body,
            text=json_response,
            content_type="application/json",
        )


class BadRequest(HTTPError):
    status_code = 400


class NotFound(HTTPError):
    status_code = 400


class Advert(Base):
    __tablename__ = "Advert"

    id = Column(Integer, primary_key=True)
    header = Column(String(64), index=True, unique=True, nullable=False)
    description = Column(String(128))
    create_date = Column(DateTime, server_default=func.now())
    owner = Column(String(128))


async def get_advert(advert_id: int, session) -> Advert:
    advert = await session.get(Advert, advert_id)
    if not advert:
        raise NotFound(message="advert not found")
    return advert

#
# class AdvertView(web.View):
#     async def get(self):
#         user_id = int(self.request.match_info["user_id"])
#         async with app.async_session_maker() as session:
#             user = await get_user(user_id, session)
#             return web.json_response(
#                 {
#                     "username": user.username,
#                     "registration_time": int(user.registration_time.timestamp()),
#                 }
#             )
#
#     async def post(self):
#         user_data = await self.request.json()
#         new_user = User(**user_data)
#         async with app.async_session_maker() as session:
#             try:
#                 session.add(new_user)
#                 await session.commit()
#                 return web.json_response({"id": new_user.id})
#             except IntegrityError as er:
#                 raise BadRequest(message="user already exists")
#
#     async def patch(self):
#         user_id = int(self.request.match_info["user_id"])
#         user_data = await self.request.json()
#         async with app.async_session_maker() as session:
#             user = await get_user(user_id, session)
#             for column, value in user_data.items():
#                 setattr(user, column, value)
#             session.add(user)
#             await session.commit()
#             return web.json_response({"status": "success"})
#
#     async def delete(self):
#         user_id = int(self.request.match_info["user_id"])
#         async with app.async_session_maker() as session:
#             user = await get_user(user_id, session)
#             await session.delete(user)
#             await session.commit()
#             return web.json_response({"status": "success"})
#
#
# async def init_orm(app: web.Application):
#     print("Приложение стартовало")
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#         async_session_maker = sessionmaker(
#             engine, expire_on_commit=False, class_=AsyncSession
#         )
#         app.async_session_maker = async_session_maker
#         yield
#     print("Приложение завершило работу")
#
#
# app.cleanup_ctx.append(init_orm)
# app.add_routes([web.get("/users/{user_id:\d+}", UserView)])
# app.add_routes([web.patch("/users/{user_id:\d+}", UserView)])
# app.add_routes([web.delete("/users/{user_id:\d+}", UserView)])
# app.add_routes([web.post("/users/", UserView)])
# web.run_app(app)
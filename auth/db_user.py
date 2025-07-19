from auth.models import User
from sqlalchemy.future import select


async def get_user(login, session):
    stmt = select(User).where(User.email == login)
    result = await session.scalars(stmt)
    return result.first()

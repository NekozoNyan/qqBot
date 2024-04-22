from datetime import datetime
from services.db_context import db


class groupUsr(db.Model):
    __tablename__ = "groupUsr"

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    belonging_group = db.Column(db.BigInteger(), nullable=False)

    checkin_count = db.Column(db.Integer(), nullable=False)
    checkin_time_last = db.Column(db.DateTime(timezone=True), nullable=False)
    # 积分
    impression = db.Column(db.Numeric(scale=3, asdecimal=False), nullable=False)

    _idx1 = db.Index("group_usr_idx1", "usr_qq", "belonging_group", unique=True)

    @classmethod
    async def ensure(
        cls, user_qq: int, belonging_group: int, for_update: bool = False
    ) -> "groupUsr":
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        if for_update:
            query = query.with_for_update()
        user = await query.gino.first()

        return user or await cls.create(
            user_qq=user_qq,
            belonging_group=belonging_group,
            checkin_count=0,
            chekin_time_last=datetime.min,
            impression=0,
        )

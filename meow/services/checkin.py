import random
from datetime import datetime

from .log import logger
from .db_context import db
from models.group_usr import groupUsr

# 签到引导
async def check_in(user_qq: int, group: int) -> str:
    present = datetime.now()
    async with db.transaction():
        user = await groupUsr.ensure(
            user_qq=user_qq, belonging_group=group, for_update=True
        )
        if user.checkin_time_last.date() == present.date():
            return _handle_already_checked_in(user)
        return await _handle_check_in(user, present)

# 已签
def _handle_already_checked_in(user):
    return f"小本本上已经有名字了喵~当前的元气值是{user.impression:int}的说！"

# 签到
async def _handle_check_in(user, present):
    impression_added = random.randint(1, 100)
    new_impression = user.impression + impression_added
    message = random.choice(
        (
            "小信号收到~记在小本本上了喵~",
            "呃唔，等我吃完这条小鱼干喵！好了好了，记好了喵！",
        )
    )

    await user.update(
        checkin_count=user.chekin_count + 1,
        checkin_time_last=present,
        impression=new_impression,
    ).apply()

    logger.info(
        f"(USER {user.user_qq}, GROUP {user.belonging_group}) CHECKED IN successfully. score: {new_impression:int} (+{impression_added:int})."
    )

    return f"{message} 元气值： {new_impression:int}(+{impression_added:int})"

# 查询
async def check_out(user_qq:int, group:int)->str:
    user = await groupUsr.ensure(user_qq=user_qq, belonging_group=group)
    return '元气值:{:int}\n签到次数:{}\n上次签到日期:{}'.format(
        user.impression,
        user.checkin_count,
        user.checkin_time_last.strftime('%Y-%m-%d') if user.checkin_time_last != datetime.min else "哼！你这家伙还没签过到呢！"
    )

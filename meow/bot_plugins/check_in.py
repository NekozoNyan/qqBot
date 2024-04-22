from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command
from services.checkin import check_in, check_out

__plugin_name__ = "签到"
__plugin_usage__ = "用法:\n" "对我说“签到”就好啦\n" "用“签到历史”来查看元气值哦！"

checkin_permission = lambda sender: sender.is_groupchat

@on_command('签到', permission=checkin_permission)
async def _(session:CommandSession):
    await session.send(
        await check_in(session.event.user_id,session.event.group_id),
        at_sender=True,
    )

@on_command('签到历史', aliases={'元气值'}, permission=checkin_permission)
async def _(session:CommandSession):
    await session.send(
        await check_out(session.event.user_id, session.event.group_id),
        at_sender=True,
    )

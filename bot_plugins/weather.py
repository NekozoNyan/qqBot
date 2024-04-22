from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command, on_natural_language
from nonebot.natural_language import NLPSession, IntentCommand
from jieba import posseg

from services.common import ServiceException
from services.weather import get_current_weather_short


__plugin_name__ = "天气"
__plugin_usage__ = "用法：\n" '对我说 "天气 香港" 来获取天气简要'

weather_permission = lambda sender: (not sender.is_privatechat) or sender.is_superuser

                                                                                                              
# 表示 “不是私聊” 或 “超级用户” 可以触发此命令
@on_command("weather", aliases=("气温", "天气"), permission=weather_permission)
async def _(session: CommandSession):
    # 尝试从用户提供的信息中提取参数，如果没有参数，则主动询问
    # print(session.current_arg)
    # print(session.current_arg_text)
    args = session.current_arg_text.strip().split()
    if len(args) > 1:
        city = args[0]
    else:
        city = await session.aget(prompt="嗯？哪儿的nia~", at_sender=True)
    
    # 在这里调用 weather service，获取结果
    try:
        result = await get_current_weather_short(city)
        await session.send(f"{city}的天气现在是 {result} 喵~")
    except ServiceException as e:
        result = e.message
        await session.send(result)


# 只要消息包含“天气”，就执行此处理器
@on_natural_language(keywords={"气温", "天气"}, permission=weather_permission)
async def __(session: NLPSession):
    words = posseg.lcut(session.msg_text.strip())
    for word in words:
        if word.flag == 'ns':
            city = word.word
            break
    # args = {'city': city}
    # print(args['city'])
    result = await get_current_weather_short(city)
    await session.send(f"{city}的天气现在是 {result} 喵~")

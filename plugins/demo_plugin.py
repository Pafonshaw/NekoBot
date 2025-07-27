"""
NekoBot Plugin 开发简记:
常量:
    PRIORITY int 优先级, 越大优先级越高, 默认为 50
    NAME str 插件名, 默认为文件名
    DESCRIBE str 插件描述, 默认为 无
异步函数:
    onGroupAtMessage(message: GroupMessage, seq: int) -> int 群聊艾特时调用, seq为当前消息序号, 返回值将用作下一个插件的seq参数, seq初始值为1. 若返回0则停止继续执行其他插件. 因此, 当你回复了一条序号为seq的消息, 并希望下一个插件也能收到这条消息, 你需要返回 seq+1
    onC2CMessage(message: C2CMessage, seq: int) -> int 私聊时调用, seq同onGroupAtMessage
    onDirectMessage(message: DirectMessage) 频道私信时调用, 若返回 False, 则停止继续执行其他插件
    onAtMessage(message: Message, seq: int) 频道艾特时调用, 若返回 False, 则停止继续执行其他插件
    onLoad(admin: list[str], logger: logging.Logger) 插件加载/热重载时调用
    onUnload() 插件卸载时调用
可用工具:
    utils.utils:
      异步函数:
        send_pic
        send_video
        send_silk
        set_shared_data(key: str, value) 设置共享数据   # 这三个学安卓的
        get_shared_data(key: str) 获取共享数据
        del_shared_data(key: str) 删除共享数据
      函数:
        get_user_id(message: Union[GroupMessage, C2CMessage, DirectMessage, Message]) -> str 获取用户ID
"""


NAME: str = '示例插件'  # 插件名
DESCRIBE: str = '这是一个示例插件'  # 插件描述
PRIORITY: int = 10  # 插件优先级

from typing import Union
from utils.utils import send_pic, set_shared_data, get_shared_data, del_shared_data, get_user_id
from botpy.message import C2CMessage, GroupMessage

admin: list[str] = []
logger = None

async def onLoad(_admin: list[str], _logger):
    # 插件加载/热重载事件
    global logger
    global admin
    logger = _logger
    admin = _admin
    if (await get_shared_data('DEMO_OPEN')) is None:    # demo开关兼第一次加载标记
        # do something
        # async with httpx.AsyncClient() as client:
        #     resp = await client.get('使用人数统计')
        await set_shared_data('DEMO_OPEN', True)

async def onUnload():
    # 插件卸载事件
    if (await get_shared_data('DEMO_OPEN')) is not None:
        # do something
        # async with httpx.AsyncClient() as client:
        #     resp = await client.get('卸载人数统计')
        await del_shared_data('DEMO_OPEN')

async def onMessage(message: Union[C2CMessage, GroupMessage], seq: int = 1):
    # 同时用于 消息列表私聊事件 和 群聊艾特事件

    # 框架会处理
    # if message.content.startswith('/'): # 若开头有/
    #     message.content = message.content[1:].strip()   # 去掉/

    if (_open := message.content == '开启demo') or (message.content == '关闭demo'):
        # 开关插件
        if get_user_id(message) not in admin:
            await message.reply(content='权限不足', msg_seq=seq)
            return 0
        await set_shared_data('DEMO_OPEN', _open)
        await message.reply(content='已开启demo' if _open else '已关闭demo', msg_seq=seq)
        return 0

    if (await get_shared_data('DEMO_OPEN')) is False:   # 检查插件是否启用
        return seq

    elif message.content == '你好':
        await message.reply(content='你好', msg_seq=seq)
        return 0
    elif message.content == '来张图片':
        await send_pic(message, url='https://i0.hdslb.com/bfs/static/jinkela/long/images/512.png', msg_seq=seq)
        return 0
    else:
        return seq

# 群聊艾特事件
onGroupAtMessage = onMessage
# 私聊事件
onC2CMessage = onMessage

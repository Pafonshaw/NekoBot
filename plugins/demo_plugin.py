"""
这是NekoBot的一个插件示例

NekoBot Plugin 开发简记:
常量:
    PRIORITY int 优先级, 越大优先级越高, 默认为 50
    NAME str 插件名, 默认为文件名
    DESCRIBE str 插件描述, 默认为 无
异步函数:
    onGroupAtMessage(message: GroupMessage) 群聊艾特时调用
    onC2CMessage(message: C2CMessage) 私聊时调用
    onDirectMessage(message: DirectMessage) 直接消息时调用
    onAtMessage(message: Message) 艾特时调用
    若返回 True, 则停止继续执行其他插件
    onLoad(admin: list[str], logger: logging.Logger) 插件加载/热重载时调用
    onUnload() 插件卸载时调用
可用工具:
    utils.utils:
        send_pic
        send_video
        send_silk
        set_shared_data(key: str, value) 设置共享数据   # 这三个学安卓的
        get_shared_data(key: str) 获取共享数据
        del_shared_data(key: str) 删除共享数据
"""

NAME: str = '示例插件'  # 插件名
DESCRIBE: str = '这是一个示例插件'  # 插件描述
PRIORITY: int = 10  # 插件优先级

from typing import Union
from utils.utils import send_pic, set_shared_data, get_shared_data, del_shared_data
from botpy.message import C2CMessage, GroupMessage

admin: list[str] = []
logger = None

async def onLoad(_admin: list[str], _logger):
    # 插件加载/热重载事件
    global logger
    global admin
    logger = _logger
    admin = _admin
    if (await get_shared_data('DEMO_OPEN')) is None:    #demo开关兼第一次加载标记
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

async def onMessage(message: Union[C2CMessage, GroupMessage]):
    # 同时用于 消息列表私聊事件 和 群聊艾特事件
    if message.content.startswith('/'): # 若开头有/
        message.content = message.content[1:].strip()   # 去掉/

    if message.content == '开启demo':   # 开启插件指令
        user = message.author.user_openid if isinstance(message, C2CMessage) else message.author.member_openid
        if user in admin:  # 检查权限
            await set_shared_data('DEMO_OPEN', True)  # 设置插件开关为True
            await message.reply(content='已开启demo')
        else:
            await message.reply(content='你不是管理员，无法开启demo')
        return True
    elif message.content == '关闭demo':   # 关闭插件指令
        user = message.author.user_openid if isinstance(message, C2CMessage) else message.author.member_openid
        if user in admin:
            await set_shared_data('DEMO_OPEN', False)
            await message.reply(content='已关闭demo')
        else:
            await message.reply(content='你不是管理员，无法关闭demo')
        return True
    
    if (await get_shared_data('DEMO_OPEN')) is False:   # 检查插件是否启用
        return False
    elif message.content == '你好':
        await message.reply(content='你好')
        return True
    elif message.content == '来张图片':
        await send_pic(message, url='https://i0.hdslb.com/bfs/static/jinkela/long/images/512.png')
        return True
    else:
        return False

# 群聊艾特事件
onGroupAtMessage = onMessage
# 私聊事件
onC2CMessage = onMessage

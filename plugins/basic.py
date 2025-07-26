"""
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

NAME = '基础插件'
DESCRIBE = '基础插件'
PRIORITY = 100

import json
import random
import aiofiles
# from botpy.message import GroupMessage, C2CMessage, Message, DirectMessage

yuanqu_list = []
caocao_list = []
songci_list = []
tangshi_list = []
chengyu_list = []

def fake_menu(content: str):
    if content.startswith('菜单'):
        return ("\n· 随机唐诗"
                "\n· 随机成语"
                "\n· 随机宋词"
                "\n· 随机元曲"
                "\n· 曹操诗集")

    elif content.startswith("随机元曲"):
        yuanqu = yuanqu_list[random.randint(0, len(yuanqu_list) - 1)]
        paragraphs = '\n'.join(yuanqu['paragraphs'])
        return f'《{yuanqu["title"]}》 {yuanqu["author"]}\n{paragraphs}'

    elif content.startswith("曹操诗集"):
        caocao = caocao_list[random.randint(0, len(caocao_list) - 1)]
        paragraphs = '\n'.join(caocao['paragraphs'])
        return f'《{caocao["title"]}》 曹操\n{paragraphs}'

    elif content.startswith("随机宋词"):
        songci = songci_list[random.randint(0, len(songci_list) - 1)]
        paragraphs = '\n'.join(songci['paragraphs'])
        return f'《{songci["rhythmic"]}》 {songci["author"]}\n{paragraphs}'

    elif content.startswith("随机唐诗"):
        tangshi = tangshi_list[random.randint(0, len(tangshi_list) - 1)]
        paragraphs = '\n'.join(tangshi['paragraphs'])
        return f'《{tangshi["title"]}》 {tangshi["author"]}\n{paragraphs}\n\n短评:{tangshi["prologue"]}'

    elif content.startswith("随机成语"):
        chengyu = chengyu_list[random.randint(0, len(chengyu_list) - 1)]
        return f'成语: {chengyu["word"]}\n拼音: {chengyu["pinyin"]}\n注释: {chengyu["explanation"]}\n\n实例: {chengyu["derivation"]}'
    
    return False


async def onMessage(message):
    if message.content.startswith('/'):
        message.content = message.content[1:].strip()
    result = fake_menu(message.content)
    if result:
        await message.reply(content=result)
        return True
    return False

onGroupAtMessage = onMessage
onC2CMessage = onMessage
onDirectMessage = onMessage
onAtMessage = onMessage


async def onLoad(admin, logger):
    global yuanqu_list
    global caocao_list
    global songci_list
    global tangshi_list
    global chengyu_list
    async with aiofiles.open('./database/yuanqu.json', encoding='utf-8') as f:
        yuanqu_list = json.loads(await f.read())
    async with aiofiles.open(f'./database/caocao.json', encoding='utf-8') as f:
        caocao_list = json.loads(await f.read())
    async with aiofiles.open(f'./database/songci.json', encoding='utf-8') as f:
        songci_list = json.loads(await f.read())
    async with aiofiles.open(f'./database/tangshi.json', encoding='utf-8') as f:
        tangshi_list = json.loads(await f.read())
    async with aiofiles.open(f'./database/chengyu.json', encoding='utf-8') as f:
        chengyu_list = json.loads(await f.read())


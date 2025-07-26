
import base64
import aiofiles
from botpy.message import GroupMessage, C2CMessage
from typing import Union
import json

async def send_pic(
    message: Union[GroupMessage, C2CMessage],
    path: str = None,
    data: bytes = None,
    url: str = None,
    msg_seq: int = 1
):
    """
    发送图片

    @ param message GroupMessage: 消息对象
    @ param path str: 文件路径
    @ param data bytes: 文件数据
    @ param url str: 文件url
    @ param msg_seq int: 消息序号

    注意:
      path 和 data 和 url只能传一个
      当 path 和 data 都传时, 取 data
      其他情况传多个报错
    """
    if path:
        async with aiofiles.open(path, 'rb') as f:
            file_data = await f.read()
        file_data = base64.b64encode(file_data).decode('utf-8')
    else:
        file_data = None
    if data:
        file_data = base64.b64encode(data).decode('utf-8')
    try:
        if isinstance(message, GroupMessage):
            media = await message._api.post_group_file(url=url, file_data=file_data, group_openid=message.group_openid, file_type=1)
        elif isinstance(message, C2CMessage):
            media = await message._api.post_c2c_file(url=url, file_data=file_data, user_openid=message.author.user_openid, file_type=1)
    except ValueError:
        raise
    await message.reply(msg_type=7, media=media, msg_seq=msg_seq)


# async def send_pics(
#     message: Union[GroupMessage, C2CMessage],
#     paths: list = None,
#     datas: list = None,
#     urls: list = None,
#     page: Union[int, str] = 1,
#     item_count: int = 5,
#     start_seq: int = 1
# ):
#     """
#     发送多图片

#     @ param message GroupMessage: 消息对象
#     @ param paths list: 文件路径列表
#     @ param datas list: 文件数据列表
#     @ param urls list: 文件url列表
#     @ param page int: 页数
#     @ param item_count int: 每页图片数量
#     @ param start_seq int: 消息起始序号

#     注意:
#     paths , datas 和 urls 只能且必须传一个
#     page 应大于等于1
#     """
#     try:
#         page = int(page)
#     except:
#         raise ValueError('page 应为数字')
#     if urls:
#         imgs = urls
#     elif datas:
#         imgs = datas
#     elif paths:
#         imgs = paths
#     else:
#         raise ValueError('paths, datas 和 urls 只能且必须传一个')
#     if (page-1)*item_count < len(imgs):
#         msg_seq = start_seq
#         for i in imgs[(page-1)*item_count:page*item_count]:
#             try:
#                 if urls:
#                     await send_pic(message, url=i, msg_seq=msg_seq)
#                 elif datas:
#                     await send_pic(message, data=i, msg_seq=msg_seq)
#                 else:
#                     await send_pic(message, path=i, msg_seq=msg_seq)
#             except Exception as e:
#                 await message.reply(content=f'\n发送失败{repr(e)}', msg_seq=msg_seq)
#             finally:
#                 msg_seq += 1
#     else:
#         await message.reply(content=f'\n页码超出范围')


async def send_video(
    message: Union[GroupMessage, C2CMessage],
    path: str = None,
    data: bytes = None,
    url: str = None,
    msg_seq: int = 1
):
    """
    发送视频

    @ param message GroupMessage: 消息对象
    @ param path str: 文件路径
    @ param data bytes: 文件数据
    @ param url str: 文件url
    @ param msg_seq int: 消息序号

    注意:
      path 和 url只能传一个
      path 和 data 和 url只能传一个, 取 data
      其他情况传多个报错
    """
    if path:
        async with aiofiles.open(path, 'rb') as f:
            file_data = await f.read()
        file_data = base64.b64encode(file_data).decode('utf-8')
    else:
        file_data = None
    if data:
        file_data = base64.b64encode(data).decode('utf-8')
    try:
        if isinstance(message, GroupMessage):
            media = await message._api.post_group_file(url=url, file_data=file_data, group_openid=message.group_openid, file_type=2)
        elif isinstance(message, C2CMessage):
            media = await message._api.post_c2c_file(url=url, file_data=file_data, user_openid=message.author.user_openid, file_type=2)
    except ValueError as e:
        raise ValueError('path 和 url 只能传一个')
    await message._api.post_group_message(group_openid=message.group_openid, msg_type=7, msg_id=message.id, media=media, msg_seq=msg_seq)


async def send_silk(
    message: Union[GroupMessage, C2CMessage],
    path: str = None,
    data: bytes = None,
    url: str = None,
    msg_seq: int = 1
):
    """
    发送语音

    @ param message GroupMessage: 消息对象
    @ param path str: 文件路径
    @ param data bytes: 文件数据
    @ param url str: 文件url
    @ param msg_seq int: 消息序号

    注意:
      path 和 url只能传一个
      path 和 data 和 url只能传一个, 取 data
      其他情况传多个报错
    """
    if path:
        async with aiofiles.open(path, 'rb') as f:  # 修改为异步文件读取
            file_data = await f.read()
        file_data = base64.b64encode(file_data).decode('utf-8')
    else:
        file_data = None
    if data:
        file_data = base64.b64encode(data).decode('utf-8')
    try:
        if isinstance(message, GroupMessage):
            media = await message._api.post_group_file(url=url, file_data=file_data, group_openid=message.group_openid, file_type=3)
        elif isinstance(message, C2CMessage):
            media = await message._api.post_c2c_file(url=url, file_data=file_data, user_openid=message.author.user_openid, file_type=3)
    except ValueError as e:
        raise ValueError('path 和 url 只能传一个')
    await message._api.post_group_message(group_openid=message.group_openid, msg_type=7, msg_id=message.id, media=media, msg_seq=msg_seq)

async def set_shared_data(key: str, value):
    async with aiofiles.open('./config/shared_data.json', 'r+', encoding='utf-8') as f:
        data = await f.read()
        data = json.loads(data)
        data[key] = value
        await f.seek(0)
        await f.write(json.dumps(data, indent=4, ensure_ascii=False))
        await f.truncate()

async def get_shared_data(key: str):
    async with aiofiles.open('./config/shared_data.json', 'r', encoding='utf-8') as f:
        data = await f.read()
    data = json.loads(data)
    return data.get(key)

async def del_shared_data(key: str):
    async with aiofiles.open('./config/shared_data.json', 'r+', encoding='utf-8') as f:
        data = await f.read()
        data = json.loads(data)
        if key in data:
            del data[key]
            await f.seek(0)
            await f.write(json.dumps(data, indent=4, ensure_ascii=False))
            await f.truncate()


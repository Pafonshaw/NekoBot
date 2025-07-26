# -*- coding: utf-8 -*-
# TODO 插件热重载 包的子模块重载问题

if __import__('platform').system().startswith('Win'):
    # 让windows支持颜色代码
    __import__('colorama').init()


import os
import traceback
import json
import importlib
from typing import Union
import asyncio
import botpy
import time
from botpy import logger
from botpy.message import GroupMessage, C2CMessage, Message, DirectMessage
from botpy.logging import DEFAULT_FILE_HANDLER


plugins: dict = {}
admin: list = []

def plugin_name(plugin: str):
    return plugins[plugin].NAME if hasattr(plugins[plugin], "NAME") else plugin

async def admin_utils(message: Union[GroupMessage, C2CMessage]):
    if message.content.startswith('/'):
        message.content = message.content[1:].strip()
    if message.content.startswith('_menu'):
        # 主人菜单
        await message.reply(content='\nadmin menu:' \
                            '\n_menu: 本菜单' \
                            '\n_reload: 插件热重载' \
                            '\n_exit: 机器人关机' \
                            '\n_plugins: 插件列表')
    elif message.content.startswith('_reload'):
        if isinstance(message, GroupMessage):
            if message.author.member_openid not in admin:
                await message.reply(content='\n你没有权限执行该命令')
        else:
            if message.author.user_openid not in admin:
                await message.reply(content='\n你没有权限执行该命令')
        global plugins
        # 插件热重载
        await message.reply(content='\n插件热重载中...')
        logger.info("热重载插件中...")
        plugin_list = os.listdir('./plugins')
        for plugin in plugin_list:
            if plugin in ["__init__.py", "__pycache__"]:
                continue
            if os.path.isfile(f'./plugins/{plugin}') and plugin.endswith('.py'):
                plugin = plugin[:-3]
            elif os.path.isdir(f'./plugins/{plugin}') and os.path.exists(f'./plugins/{plugin}/__init__.py'):
                pass
            else:
                logger.error(f'插件 {plugin} 加载失败: 插件目录错误')
                continue
            if plugin in plugins:
                # 已经加载过了, 重载插件
                try:
                    importlib.reload(plugins[plugin])
                    logger.info(f'插件 {plugin_name(plugin)} 重载成功')
                except Exception as e:
                    logger.error(f'插件 {plugin_name(plugin)} 重载失败: {repr(e)}\n堆栈信息:\n{traceback.format_exc()}')
            else:
                # 没有加载的新插件, 加载插件
                try:
                    plugins[plugin] = importlib.import_module(f'plugins.{plugin}')
                    logger.info(f'插件 {plugin_name(plugin)} 加载成功')
                except Exception as e:
                    logger.error(f'插件 {plugin} 加载失败: {repr(e)}\n堆栈信息:\n{traceback.format_exc()}')
        temp_plugins: list = []
        for plugin in plugins:
            # 删除已移除插件
            if (plugins[plugin].__file__.endswith('__init__.py') and plugin not in plugin_list) \
                or (not plugins[plugin].__file__.endswith('__init__.py') and plugin + '.py' not in plugin_list):
                _plugin_name = plugin_name(plugin)
                if hasattr(plugins[plugin], 'onUnload'):
                    try:
                        await plugins[plugin].onUnload()
                    except Exception as e:
                        logger.error(f'插件 {_plugin_name} 卸载失败: {repr(e)}\n堆栈信息:\n{traceback.format_exc()}')
                temp_plugins.append(plugin)
        for plugin in temp_plugins:
            del plugins[plugin]
            logger.info(f'插件 {plugin} 已删除')
        logger.info(f"插件热重载完成, 当前共 {len(plugins)} 个插件")
        # 排序
        plugins = dict(sorted(plugins.items(), key=lambda x: x[1].PRIORITY if hasattr(x[1], 'PRIORITY') else 50, reverse=True))
        # 初始化
        logger.info("初始化插件中...")
        for plugin in plugins:
            if hasattr(plugins[plugin], 'onLoad'):
                try:
                    await plugins[plugin].onLoad(admin, logger)
                except Exception as e:
                    logger.error(f'插件 {plugin_name(plugin)} 初始化失败: {repr(e)}\n堆栈信息:\n{traceback.format_exc()}')
                    continue
        logger.info("插件初始化完成")
        await message.reply(content=f'\n插件热重载完成, 当前共 {len(plugins)} 个插件', msg_seq=2)
    elif message.content.startswith('_exit'):
        if isinstance(message, GroupMessage):
            if message.author.member_openid not in admin:
                await message.reply(content='\n你没有权限执行该命令')
        else:
            if message.author.user_openid not in admin:
                await message.reply(content='\n你没有权限执行该命令')
        await message.reply(content='\nNekoBot 已关机')
        os._exit(0)
    elif message.content.startswith('_plugins'):
        # 插件列表
        await message.reply(content='\n插件列表:\n' + '\n'.join([f'{plugin_name(plugin)}: {plugins[plugin].DESCRIBE if hasattr(plugins[plugin], "DESCRIBE") else "无"}' for plugin in plugins]))
    else:
        return False

class MyClient(botpy.Client):
    async def on_ready(self):
        logger.info(f"机器人 {self.robot.name} 已上线")

    # 群聊艾特
    async def on_group_at_message_create(self, message: GroupMessage):
        message.content = message.content.strip()
        logger.info(f"User: {message.author.member_openid}; Type: GA; Q: {message.content}")
        if (await admin_utils(message)) is not False:
            return
        for plugin in plugins:
            if hasattr(plugins[plugin], 'onGroupAtMessage'):
                try:
                    if await plugins[plugin].onGroupAtMessage(message):
                        break
                except Exception as e:
                    logger.error(f'插件 {plugin_name(plugin)} 群聊艾特消息处理失败: {repr(e)}\n堆栈信息:\n{traceback.format_exc()}')

    # 消息列表
    async def on_c2c_message_create(self, message: C2CMessage):
        message.content = message.content.strip()
        logger.info(f"User: {message.author.user_openid}; Type: C2C; Q: {message.content}")
        if (await admin_utils(message)) is not False:
            return
        for plugin in plugins:
            if hasattr(plugins[plugin], 'onC2CMessage'):
                try:
                    if await plugins[plugin].onC2CMessage(message):
                        break
                except Exception as e:
                    logger.error(f'插件 {plugin_name(plugin)} 消息列表消息处理失败: {repr(e)}\n堆栈信息:\n{traceback.format_exc()}')

    # 频道私信
    async def on_direct_message_create(self, message: DirectMessage):
        message.content = message.content.strip()
        logger.info(f"User: {message.author.id}; Type: DM; Q: {message.content}")
        if (await admin_utils(message)) is not False:
            return
        for plugin in plugins:
            if hasattr(plugins[plugin], 'onDirectMessage'):
                try:
                    if await plugins[plugin].onDirectMessage(message):
                        break
                except Exception as e:
                    logger.error(f'插件 {plugin_name(plugin)} 频道私信消息处理失败: {repr(e)}\n堆栈信息:\n{traceback.format_exc()}')

    # 频道艾特
    async def on_at_message_create(self, message: Message):
        message.content = message.content.strip()
        logger.info(f"User: {message.author.id}; Type: DA; Q: {message.content}")
        if (await admin_utils(message)) is not False:
            return
        for plugin in plugins:
            if hasattr(plugins[plugin], 'onAtMessage'):
                try:
                    if await plugins[plugin].onAtMessage(message):
                        break
                except Exception as e:
                    logger.error(f'插件 {plugin_name(plugin)} 频道艾特消息处理失败: {repr(e)}\n堆栈信息:\n{traceback.format_exc()}')


if __name__ == '__main__':

    # 初始化intents
    intents = botpy.Intents.all()
    DEFAULT_FILE_HANDLER["filename"] = f"./log/bot_{time.strftime('%Y-%m-%d')}.log"
    # 创建客户端实例
    client = MyClient(intents=intents, timeout=120, ext_handlers=DEFAULT_FILE_HANDLER)

    with open('./config/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    appid = config['appid']
    secret = config['secret']
    admin = config['admin']

    logger.info("加载插件中...")
    for plugin in os.listdir('./plugins'):
        if plugin in ["__init__.py", "__pycache__"]:
            continue
        if os.path.isfile(f'./plugins/{plugin}') and plugin.endswith('.py'):
            plugin = plugin[:-3]
        elif os.path.isdir(f'./plugins/{plugin}') and os.path.exists(f'./plugins/{plugin}/__init__.py'):
            pass
        else:
            logger.error(f'插件 {plugin} 加载失败: 插件目录错误')
            continue
        try:
            plugins[plugin] = importlib.import_module(f'plugins.{plugin}')
            logger.info(f'插件 {plugin_name(plugin)} 加载成功')
        except Exception as e:
            logger.error(f'插件 {plugin} 加载失败: {repr(e)}\n堆栈信息:\n{traceback.format_exc()}')
            continue
    logger.info(f'插件加载完成, 当前共 {len(plugins)} 个插件')

    # 插件重排序, PRIORITY 越大优先级越高, PRIORITY 默认为 50
    plugins = dict(sorted(plugins.items(), key=lambda x: x[1].PRIORITY if hasattr(x[1], 'PRIORITY') else 50, reverse=True))

    # 初始化插件
    logger.info("初始化插件中...")
    for plugin in plugins:
        if hasattr(plugins[plugin], 'onLoad'):
            try:
                asyncio.run(plugins[plugin].onLoad(admin, logger))
                logger.info(f'插件 {plugin_name(plugin)} 初始化成功')
            except Exception as e:
                logger.error(f'插件 {plugin_name(plugin)} 初始化失败: {repr(e)}\n堆栈信息:\n{traceback.format_exc()}')
                continue
    logger.info("插件初始化完成")

    # 运行机器人，需要提供appid和secret
    client.run(appid, secret)


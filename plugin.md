# NekoBot Plugin 开发文档  

## 前置条件  

- Python 基础  
- Python 异步编程  
- 了解 [qq-botpy](https://bot.q.qq.com/wiki/develop/pythonsdk/)  

## botpy 修复  
将botpy的api.py中 BotAPI 的 post_group_file 和 post_c2c_file 替换为 
```python
    async def post_group_file(
        self,
        group_openid: str,
        file_type: int,
        url: str = None,
        file_data: str = None,
        srv_send_msg: bool = False,
    ) -> message.Media:
        """
        上传/发送群聊图片

        Args:
          group_openid (str): 您要将消息发送到的群的 ID
          file_type (int): 媒体类型：1 图片png/jpg，2 视频mp4，3 语音silk，4 文件（暂不开放）
          url (str): 需要发送媒体资源的url
          file_data (str): 媒体文件的base64编码
          srv_send_msg (bool): 设置 true 会直接发送消息到目标端，且会占用主动消息频次
        
        注意:
          url 和 file_data 二选一即可
        """
        payload = locals()
        payload.pop("self", None)
        if url:
            payload.pop("file_data", None)
        elif file_data:
            payload.pop("url", None)
        else:
            raise ValueError("url 和 file_data 二选一即可")
        route = Route("POST", "/v2/groups/{group_openid}/files", group_openid=group_openid)
        return await self._http.request(route, json=payload)

    async def post_c2c_file(
        self,
        openid: str,
        file_type: int,
        url: str = None,
        file_data: str = None,
        srv_send_msg: bool = False,
    ) -> message.Media:
        """
        上传/发送c2c图片

        Args:
          openid (str): 您要将消息发送到的用户的 ID
          file_type (int): 媒体类型：1 图片png/jpg，2 视频mp4，3 语音silk，4 文件（暂不开放）
          url (str): 需要发送媒体资源的url
          file_data (str): 媒体文件的base64编码
          srv_send_msg (bool): 设置 true 会直接发送消息到目标端，且会占用主动消息频次
        """
        payload = locals()
        payload.pop("self", None)
        if url:
            payload.pop("file_data", None)
        elif file_data:
            payload.pop("url", None)
        else:
            raise ValueError("url 和 file_data 二选一即可")
        route = Route("POST", "/v2/users/{openid}/files", openid=openid)
        return await self._http.request(route, json=payload)
```
以修复不能发送本地媒体文件的问题  

# 开发插件  

## 1. 定义以下内容  

NekoBot 在使用前会检查属性是否存在, 您可根据需要定义以下内容:

### 1.1 常量  

- PRIORITY
  - 类型: int
  - 说明: 优先级, 越大优先级越高, 默认为 50 
- NAME
    - 类型: str
    - 说明: 插件名, 默认为文件名 
- DESCRIBE
    - 类型: str
    - 说明: 插件描述, 默认为 无 

### 1.2 异步函数  

- onGroupAtMessage
    - 参数:
      - message: botpy.message.GroupMessage
    - 说明: 群聊艾特时调用, 若函数返回True, 则会结束此次事件, 否则将继续调用下一个插件对应的函数
- onC2CMessage
    - 参数: 
      - message: botpy.message.C2CMessage
    - 说明: 私聊时调用, 若函数返回True, 则会结束此次事件, 否则将继续调用下一个插件对应的函数
- onDirectMessage
    - 参数: 
      - message: botpy.message.DirectMessage
    - 说明: 直接消息时调用, 若函数返回True, 则会结束此次事件, 否则将继续调用下一个插件对应的函数
- onAtMessage
    - 参数: 
      - message: botpy.message.Message
    - 说明: 艾特时调用, 若函数返回True, 则会结束此次事件, 否则将继续调用下一个插件对应的函数
- onLoad
    - 参数: 
      - admin: list[str], # 主人列表
      - logger: logging.Logger
    - 说明: 插件加载/热重载时调用
- onUnload
    - 参数: 无
    - 说明: 插件卸载时调用

## 2 可用工具

### utils.utils
- send_pic
    - 参数:
        - message: Union[botpy.message.GroupMessage, botpy.message.C2CMessage], # 消息对象
        - path: str = None, # 文件路径
        - data: bytes = None, # 文件数据
        - url: str = None, # 文件url
        - msg_seq: int = 1 # 消息序号
    - 说明: 发送图片, 支持GroupMessage和C2CMessage, path 和 data 和 url 三选一
- send_video
    - 参数:
        - message: Union[GroupMessage, C2CMessage],
        - path: str = None,
        - data: bytes = None,
        - url: str = None,
        - msg_seq: int = 1
    - 说明: 发送视频, 支持GroupMessage和C2CMessage, path 和 data 和 url 三选一
- send_silk
    - 参数:
        - message: Union[GroupMessage, C2CMessage],
        - path: str = None,
        - data: bytes = None,
        - url: str = None,
        - msg_seq: int = 1
    - 说明: 发送语音, 支持GroupMessage和C2CMessage, path 和 data 和 url 三选一
- set_shared_data
    - 参数:
        - key: str,
        - value: Any
    - 说明: 设置共享数据, 这三个shared_data借鉴了安卓
- get_shared_data
    - 参数:
        - key: str
    - 说明: 获取共享数据
- del_shared_data
    - 参数:
        - key: str
    - 说明: 删除共享数据

## 3 示例插件  
文档写的比较抽象, 可以看看 [示例](https://github.com/Pafonshaw/NekoBot/blob/main/plugins/demo_plugin.py)

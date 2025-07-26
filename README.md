# NekoBot  
自用QQ官机框架  

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
或直接将api.py替换为仓库中的 [api.py](https://github.com/Pafonshaw/NekoBot/blob/main/api.py)  
以修复不能发送本地媒体文件的问题  

## 配置  
修改 config/config.json 中的 appid 和 secret 为你自己的 appid 和 secret  
修改 config/config.json 中的admin为你自己的user_id(启动后通过日志获取)  

## 开发插件  
见文档 [plugin.md](https://github.com/Pafonshaw/NekoBot/blob/main/plugin.md)


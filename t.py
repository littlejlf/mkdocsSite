import asyncio
from pikpakapi import PikPakApi

async def main():
    client = PikPakApi(
        username="qq1672222rr+nkz2rstr@gmail.com",
        password="123abc123",
    )
    await client.login()
    await client.refresh_access_token()
    
    
    # 获取离线任务列表
    offline = await client.offline_list()
    print("离线任务列表：", offline)

# 运行入口
asyncio.run(main())

import asyncio
import subprocess
import sys

import requests
from playwright.async_api import async_playwright

# ENV = {
# "BOTID": sys.argv[1],
# "CHATID": sys.argv[2]
# }


def notice(title, message):
    print(message)
    subprocess.Popen(['notify-send', title, message])


async def main(headless=True):
    cookies = [{
        "name": "SAAS_S_ID",
        "value": "xmu",
        "domain": "xmuxg.xmu.edu.cn",
        "path": "/"
    }, {
        "name": "SAAS_U",
        "value": "6a20ba0fd410d55eedbaa22f13983a3e186ed1c5",
        "domain": "xmuxg.xmu.edu.cn",
        "path": "/"
    }, {
        "name": "iPlanetDirectoryPro",
        "value": "AQIC5wM2LY4Sfcxa5PLjr8Uvj%2BRcCqotLTcCXT7MlwUnphU%3D%40AAJTSQACMDE%3D%23",
        "domain": ".xmu.edu.cn",
        "path": "/"
    }, {
        "name": "JSESSIONID",
        "value": "B4ACA5ECAC17DED28FFDD3B79CDFB6D3",
        "domain": "xmuxg.xmu.edu.cn",
        "path": "/"
    }]
    async with async_playwright() as p:
        brower = await p.chromium.launch(headless=headless)
        context = await brower.new_context()
        await context.add_cookies(cookies)
        page = await context.new_page()
        await page.goto("http://xmuxg.xmu.edu.cn/xmu/app/214")
        await page.click('[title="我的表单"]')
        await page.click('//*[@id="select_1582538939790"]/div/div')
        await page.click('//html/body/div[8]/ul/div')
        page.on("dialog", lambda dialog: dialog.accept())
        await page.click('[class="form-save position-absolute"]')
        await asyncio.sleep(3)
        await page.reload()
        await page.click('[title="我的表单"]')
        await asyncio.sleep(1)
        html = await page.query_selector('[title="是 Yes"]')
        text = await html.inner_text()
        if text == "是 Yes":
            title = "Success"
            message = f"打卡成功 / 今日已打卡\n返回值: {text}"
        else:
            title = "Failure"
            message = f"打卡失败 / 未到打卡时间\n返回值: {text}"
        notice(title, message)
        # requests.get(f"https://api.telegram.org/bot{ENV['BOTID']}/sendMessage?chat_id={ENV['CHATID']}&parse_mode=Markdown&text={message}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        headless = eval(sys.argv[1])
    else:
        headless = True
    try:
        asyncio.run(main(headless=headless))
    except Exception as e:
        message = f"打卡失败 程序报错\n```\n{e}\n```"
        notice("Error", message)
        # requests.get(f"https://api.telegram.org/bot{ENV['BOTID']}/sendMessage?chat_id={ENV['CHATID']}&parse_mode=Markdown&text={message}")

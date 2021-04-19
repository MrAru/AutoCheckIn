import asyncio
import sys

import requests
from playwright.async_api import async_playwright

ENV = {
    "BOTID": sys.argv[1],
    "CHATID": sys.argv[2]
}


async def main():
    cookies = [{
        "name": "SAAS_S_ID",
        "value": sys.argv[3],
        "domain": "xmuxg.xmu.edu.cn",
        "path": "/"
    }, {
        "name": "SAAS_U",
        "value": sys.argv[4],
        "domain": "xmuxg.xmu.edu.cn",
        "path": "/"
    }, {
        "name": "iPlanetDirectoryPro",
        "value": sys.argv[5],
        "domain": ".xmu.edu.cn",
        "path": "/"
    }, {
        "name": "JSESSIONID",
        "value": sys.argv[6],
        "domain": "xmuxg.xmu.edu.cn",
        "path": "/"
    }]
    async with async_playwright() as p:
        brower = await p.chromium.launch()
        context = await brower.new_context()
        await context.add_cookies(cookies)
        page = await context.new_page()
        await page.goto("http://xmuxg.xmu.edu.cn/xmu/app/214")
        await page.click('//*[@id="mainM"]/div/div/div/div[1]/div[2]/div/div[3]/div[2]')
        await page.click('//*[@id="select_1582538939790"]/div/div')
        await page.click('//html/body/div[8]/ul/div')
        page.on("dialog", lambda dialog: dialog.accept())
        await page.click('[class="form-save position-absolute"]')
        await asyncio.sleep(5)
        await page.reload()
        text = page.query_selector(
            "/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[3]/div/div[30]/div/div/div/span[1]").inner_text()
        if text == "是":
            message = f"打卡成功\n返回值: {text}"
        else:
            message = f"打卡失败 / 未到打卡时间\n返回值: {text}"
        requests.get("https://api.telegram.org/bot" + ENV["BOTID"] + "/sendMessage?chat_id=" +
                     ENV["CHATID"] + "&parse_mode=Markdown&text=" + message, proxies=proxies)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        message = f"打卡失败 程序报错\n```\n{e}\n```"
    requests.get("https://api.telegram.org/bot" + ENV["BOTID"] + "/sendMessage?chat_id=" +
                 ENV["CHATID"] + "&parse_mode=Markdown&text=" + message, proxies=proxies)

import asyncio
import sys
import time

import requests
from playwright.async_api import async_playwright

ENV = {
    "BOTID": sys.argv[1],
    "CHATID": sys.argv[2],
    "USERNAME": sys.argv[3],
    "PASSWD": sys.argv[4],
}


async def main(headless=True):
    async with async_playwright() as p:
        brower = await p.firefox.launch(headless=headless)
        context = await brower.new_context()
        page = await context.new_page()
        await page.goto(
            "https://ids.xmu.edu.cn/authserver/login?service=https://xmuxg.xmu.edu.cn/login/cas/xmu"
        )
        await page.fill("#username", ENV["USERNAME"])
        await page.fill("#password", ENV["PASSWD"])
        await page.click(".auth_login_btn")
        await page.route("*qq*", lambda route: route.abort())
        await page.goto("https://xmuxg.xmu.edu.cn/app/214")
        await page.click('[title="我的表单"]')
        await page.click('//*[@id="select_1582538939790"]/div/div')
        await page.click("//html/body/div[8]/ul/div")
        page.on("dialog", lambda dialog: dialog.accept())
        await page.click('[class="form-save position-absolute"]')
        await asyncio.sleep(3)
        await page.reload()
        await page.click('[title="我的表单"]')
        await asyncio.sleep(1)
        html = await page.query_selector('[title="是 Yes"]')
        text = await html.inner_text()
        if text == "是 Yes":
            res = True
            message = f"打卡成功 / 今日已打卡\n返回值: {text}"
        else:
            res = False
            message = f"打卡失败 / 未到打卡时间\n返回值: {text}"
        requests.get(
            f"https://api.telegram.org/bot{ENV['BOTID']}/sendMessage?chat_id={ENV['CHATID']}&parse_mode=Markdown&text={message}"
        )
        print(message)
        return res


def run():
    try:
        res = asyncio.run(main())
    except Exception as e:
        res = False
        message = f"打卡失败 程序报错\n```\n{e}\n```"
        requests.get(
            f"https://api.telegram.org/bot{ENV['BOTID']}/sendMessage?chat_id={ENV['CHATID']}&parse_mode=Markdown&text={message}"
        )
    return res


if __name__ == "__main__":
    for _ in range(3):
        if run():
            quit()
        else:
            time.sleep(20)

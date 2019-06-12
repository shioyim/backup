import asyncio
from pyppeteer import launch
import random
import logger



username = ""
password = ""
url = "https://login.taobao.com/member/login.jhtml?style=mini&css_style=b2b&from=b2b&full_redirect=true"
async def exe_js(page):
    js1 = "() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }"
    js2 = "() =>{ window.navigator.chrome = { runtime: {},  }; }"
    js3 = "() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }"
    js4 = "() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }"
    await page.evaluateOnNewDocument(js1)
    await page.evaluateOnNewDocument(js2)
    await page.evaluateOnNewDocument(js3)
    await page.evaluateOnNewDocument(js4)



async def get_cookie(page):
    cookies_list = await page.cookies()
    cookies = ""
    for cookie in cookies_list:
        str_cookie = "{0}={1};"
        str_cookie = str_cookie.format(cookie["name"], cookie["value"])
        cookies += str_cookie
    print(cookies)
    return cookies


def wait_time():
    return random.randint(100, 150)



#鼠标滑行
async def mouse_slide(page=None):
    try:
        await page.hover("#nc_1_n1z")
        await page.mouse.down()
        await page.mouse.move(2000, 0, {"delay": random.randint(1000, 2000)})
        await page.mouse.up()
    except Exception as e:
        logger.error("Mouse slide error,please check your code!")
        return None
    else:
        await asyncio.sleep(random.uniform(1, 2))
        # 判断是否验证通过
        result = ""
        try:
            result = await page.Jeval(".nc-lang-cnt", "node => node.textContent")
        except Exception as e:
            pass
        if result != "验证通过":
            logger.error("verify fail:{}.".format(result))
            return None, page
        else:
            logger.info("verify pass.")
            return True, page

#提交后等待结果
async def click_wait_login(page):
    await asyncio.gather(page.waitForNavigation(), page.evaluate("document.getElementById('J_SubmitStatic').click()"))
    try:
        await page.waitForSelector(".account-id", {"timeout": 15000})
        print(page.url)
        return await get_cookie(page)
    except:
            logger.error("timeout wait for element.")
            return


async def login(page):
    nocaptcha = await page.Jeval("#nocaptcha", "node => node.style")
    if not nocaptcha:
        await click_wait_login(page)
        try:
            nocaptcha = await page.Jeval("#nocaptcha", "node => node.style")
            if nocaptcha:
                success, page = await mouse_slide(page=page)
                if success:
                # 登录失败出现验证，密码会被清空，所以需要重新输入密码
                    await page.type("#TPL_password_1", pwd, {"delay": wait_time()})
                    await click_wait_login(page)
        except:
            pass

    else:
        success, page = await mouse_slide(page=page)
        if success:
            await click_wait_login(page)

        # 刷新滑行验证
        errloading= str()
        try:
            errloading = await page.Jeval(".errloading", "node => node.textContent")
        except:
            pass
        if errloading:
            await page.hover("a[href='javascript:noCaptcha.reset(1)']")
            await page.mouse.down()
            await page.mouse.up()
            await asyncio.sleep(random.uniform(1, 2))
            try:
                # page.querySelector(".nc-lang-cnt[data-nc-lang='_startTEXT']")
                await page.J(".nc-lang-cnt[data-nc-lang='_startTEXT']")
                logger.info("refresh success,please slide again.")
                # 再次滑行验证
                success, page = await mouse_slide(page=page)
                if success:
                    return await login(page)
                else:
                    logger.error("second slider faild.")
                    return
            except:
                logger.error("refresh slider failed!")
                return

async def main():
    browser = await launch(headless=False, userDataDir="~/taobao-data", args=["--disable-infobars","--no-sandbox"])
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()
    await exe_js(page=page)

    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
    await page.goto(url,{"waitUntil": 'networkidle2'})
    await page.type("#TPL_username_1",username, {"delay": wait_time()-50})#毫秒  
    await page.type("#TPL_password_1",password, {"delay": wait_time()})
    await asyncio.sleep(random.random()+0.5)  
    await login(page=page)


asyncio.get_event_loop().run_until_complete(main())



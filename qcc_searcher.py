from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import random
import winsound

company_type = ['央企', '国有企业', '小微企业']
company_root = {}
provinces = ["河北", "山西", "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东",
          "海南", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "台湾"]
cities = []
with open('cities.txt', encoding='utf-8') as f:
    for city in f:
        cities.append(city.strip())

tmp_company_link = []


def search_company(company):
    global current_page

    driver.find_element(By.ID, "searchKey").clear()
    driver.find_element(By.ID, "searchKey").send_keys(company)
    driver.find_element(By.CLASS_NAME, "input-group-btn").click()

    if '企业没有找到' in driver.page_source:
        w.writelines(f",,,{name},,,,,,\n")
        return
    while True:
        try:
            driver.find_element(By.XPATH, "//table/tr/td[3]/div[1]/div[1]/span[1]/a[1]").click()
            break
        except:
            print("【【【出现错误！尽快查看Chrome！！】】】")
            winsound.Beep(440, 10000)
            time.sleep(10)
    change_page(+1)
    searched_name = driver.title.rstrip(" - 企查查")

    searched_type = None
    for tmp_type in company_type:
        if tmp_type in driver.page_source:
            searched_type = tmp_type
            break

    sub_root = None
    root = driver.title.rstrip(" - 企查查").rstrip("担任法定代表人/股东/高管信息查询 - 企查查")
    while '股东信息' in driver.page_source:
        tmp_company_link.append(root)
        time.sleep(random.uniform(4,6))
        try:
            driver.find_element(By.XPATH,
                                "//div[@class='app-tree-table'][1]/table[1]/tr[2]/td[2]/div[1]/span[2]/span[1]/a[1]").click()
        except:
            print("未找到股东信息！")
            w.writelines(f"{searched_name},{searched_type},,{name},【未知】,,,,,\n")
            change_page(-1)
            return

        change_page(+1)

        if searched_type == '央企':
            sub_root = root
        root = driver.title.rstrip(" - 企查查").rstrip("担任法定代表人/股东/高管信息查询 - 企查查")
        # print(root, sub_root)
        if root in company_root:
            root = company_root[root]
            sub_root = None
            break

    if type(root) == str:
        root = root.split('_')[0]
    if sub_root is not None:
        new_root = (root, sub_root)
    else:
        new_root = root
    # print("new_root", new_root)
    for com in tmp_company_link:
        company_root[com] = new_root
    tmp_company_link.clear()
    if searched_type == '央企':
        newline = f"{searched_name},{searched_type},【见后】,{name},央企,,,,{new_root[0]},{new_root[1]}\n"
    elif searched_type == '国有企业':
        newline = state_own_company_type(searched_name, searched_type, root)
    else:
        if len(root) <= 4:
            newline = f"{searched_name},{searched_type},{root},{name},民企,,,,,\n"
        elif '合作社' in root:
            newline = f"{searched_name},{searched_type},{root},{name},集体企业,,,,,\n"
        else:
            newline = f"{searched_name},{searched_type},{root},{name},【未知】,,,,,\n"

    w.writelines(newline)
    w.flush()
    print(newline, end="")

    while current_page > 0:
        time.sleep(0.2)
        change_page(-1)

    time.sleep(random.uniform(4, 6))


def state_own_company_type(searched_name, searched_type, root):
    for province in provinces:
        if province in searched_name:
            return f"{searched_name},{searched_type},{root},{name},省国企,,,{province},,\n"
    for city in cities:
        if city in searched_name:
            return f"{searched_name},{searched_type},{root},{name},市国企,,{city},,,\n"
    return f"{searched_name},{searched_type},{root},{name},国企,,,,,\n"


def change_page(op):
    global current_page

    if op == -1:
        driver.close()
    current_page += op
    driver.switch_to.window(driver.window_handles[current_page])


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # 开始最大化
    options.add_argument("--test-type")
    options.add_argument("--ignore-certificate-errors")  # 忽略证书错误
    options.add_argument("--disable-popup-blocking")  # 禁用弹出拦截
    options.add_argument("no-sandbox")  # 取消沙盒模式
    options.add_argument("no-default-browser-check")  # 禁止默认浏览器检查
    options.add_argument("about:histograms")
    options.add_argument("about:cache")
    options.add_argument("disable-extensions")  # 禁用扩展
    options.add_argument("disable-glsl-translator")  # 禁用GLSL翻译
    options.add_argument("disable-translate")  # 禁用翻译
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--hide-scrollbars")  # 隐藏滚动条, 应对一些特殊页面
    options.add_argument("blink-settings=imagesEnabled=false")  # 不加载图片, 提升速度
    options.add_argument(r"user-data-dir=C:\Users\SceneryMC\AppData\Local\Google\Chrome\User Data - 副本")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.qcc.com/")
    driver.implicitly_wait(10)
    current_page = 0
    with open('processed.txt') as f:
        processed = tmp_processed = int(f.read().strip())

    with open('company_list.txt', encoding='utf-8') as f:
        with open('result.csv', 'a', encoding='utf-8') as w:
            for name in f:
                if tmp_processed > 0:
                    tmp_processed -= 1
                    continue
                name = name.strip()
                if len(name) <= 3:
                    w.writelines(f",,,{name},个人,,,,,\n")
                elif re.match("[ \w,&./-]+", name, re.ASCII):
                    w.writelines(f",,,{name},外企,,,,,\n")
                else:
                    search_company(name)

                processed += 1
                with open('processed.txt', 'w') as x:
                    x.writelines(str(processed))

    driver.quit()

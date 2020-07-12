from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from urllib import request

######################## 用户定义参数 ########################

target_name = "没通网" # 需要爬取的人名称
path = "./data/result.txt"
username = '账号'
password = '密码'

######################## 华丽分割线 ########################

with open(path, "a+") as f:
    f.write(target_name + '\r\n') # \r\n是换行

browser = webdriver.Chrome()
browser.maximize_window() # 最大化窗口，防止有些组件加载不出来
browser.get('https://weibo.com/')
browser.implicitly_wait(30) # 隐性等待，若失败则报错，在时间内成功则继续
time.sleep(7)

# 填入账号密码
browser.find_element_by_name("username").send_keys(username)
browser.find_element_by_name("password").send_keys(password)
# browser.find_element_by_link_text("登录").click()
browser.find_element_by_xpath("//*[@id='pl_login_form']/div/div[3]/div[6]/a").click()

# 测试是否有验证码
# try:
#     # verifycode_class = browser.find_elements_by_class_name("info_list verify clearfix")
#     verifycode_pos = browser.find_elements_by_name("verifycode")
#     if len(verifycode_pos) != 0:
#         value = input("验证码：")
#         verifycode_pos[0].send_keys(value)
#         browser.find_elements_by_link_text("登录")[0].click()
# except:
#     pass
browser.implicitly_wait(7)

# 进入关注寻找需要爬取的人数据
browser.find_element_by_xpath("//*[@id='v6_pl_rightmod_myinfo']/div/div/div[2]/ul/li[1]/a").click()
browser.find_elements_by_link_text(target_name)[0].click()
browser.implicitly_wait(7)

# 切换到打开的新窗口
main_handle = browser.current_window_handle # 记录下原始主窗口句柄，未来多用户爬取可以用到
all_handles = browser.window_handles # 获取当前所有窗口句柄
browser.switch_to.window(all_handles[1]) # 切换到新打开的窗口句柄

# 获得所有条目位置信息
# base = browser.find_element_by_xpath("//*[@id='Pl_Official_MyProfileFeed__20']/div")
all_items = browser.find_elements_by_css_selector("[class='WB_cardwrap WB_feed_type S_bg2 WB_feed_like ']")
# all_items = base.find_elements_by_class_name("WB_cardwrap WB_feed_type S_bg2 WB_feed_like ") # 有空格不能直接找的样子，因此用css定位
for item in all_items:
    # print(item.find_element_by_css_selector("[class='W_f14 W_fb S_txt1']").text)
    if item.find_element_by_css_selector("[class='W_f14 W_fb S_txt1']").text == target_name:
        # 处理文本
        date = item.find_element_by_css_selector("[node-type='feed_list_item_date']").text + '\r\n'
        try:
            item.find_element_by_css_selector("[class='W_ficon ficon_arrow_down']").click()
            text = item.find_element_by_css_selector("[node-type='feed_list_content_full']").text + '\r\n' + '\r\n'
            text = text.replace('展开全文c', '').replace('收起全文d', '')
        except:
            text = item.find_element_by_css_selector("[node-type='feed_list_content']").text + '\r\n' + '\r\n'
        
        text = date + text
        with open(path, "a+") as f:
            f.write(text)

        # 处理图片
        try:
            media_box = item.find_element_by_css_selector("[class='media_box']")
            imgs = media_box.find_elements_by_xpath('./ul/li/img')
            for i in range(len(imgs)):
                img_link = imgs[i].get_attribute('src')
                name = item.find_element_by_css_selector("[node-type='feed_list_item_date']").get_attribute('title')[0:10] + '_' + ('%d' % i) + '.jpg'
                img_path = './data/' + name
                request.urlretrieve(img_link, img_path)
        except:
            pass

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from urllib import request
import random

######################## 用户定义参数 ########################

target_name = "没通网" # 监控对象
username = '账号'
password = '密码'
re_time = 20 # 刷新时间间隔，这里20s刷新一次
comments = None # 采用从评论库中随机抽取的方式，自定义评论请自行加入评论库中

######################## 华丽分割线 ########################

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
browser.implicitly_wait(7)

# 进入关注
browser.find_element_by_xpath("//*[@id='v6_pl_rightmod_myinfo']/div/div/div[2]/ul/li[1]/a").click()
browser.find_elements_by_link_text(target_name)[0].click()
browser.implicitly_wait(7)

# 切换到打开的新窗口
main_handle = browser.current_window_handle # 记录下原始主窗口句柄，未来多用户爬取可以用到
all_handles = browser.window_handles # 获取当前所有窗口句柄
browser.switch_to.window(all_handles[1]) # 切换到新打开的窗口句柄

# 我的主页，测试用
# browser.find_element_by_link_text('我的主页').click()

top_item_id = browser.find_elements_by_css_selector("[action-type='feed_list_item']")[0].get_attribute('mid') # 记录原来顶部元素id

# 刷新检查是否有新微博
while True:
    browser.refresh()
    browser.implicitly_wait(7)

    # 获得最上方微博的id
    new_top_item = browser.find_elements_by_css_selector("[action-type='feed_list_item']")[0]
    new_top_item_id = new_top_item.get_attribute('mid')
    # 发现新微博
    if top_item_id != new_top_item_id:

        # 判断是否是博主发的而不是点赞他人
        if new_top_item.find_element_by_css_selector("[class='W_f14 W_fb S_txt1']").text == target_name: # 是本人
            # 点赞
            new_top_item.find_element_by_css_selector("[node-type='like_status']").click()
            # 评论和转发
            new_top_item.find_element_by_css_selector("[node-type='forward_btn_text']").click()
            time.sleep(2) # 太快会导致原件加载不出来
            forward_box = browser.find_element_by_css_selector("[class='W_layer ']") # 转发窗口经过点击后被激活，定位到窗口上

            # 评论复选框
            try:
                forward_box.find_element_by_css_selector("[node-type='forwardInput']").click() # 转发评论的直接源头复选框勾选
            except:
                pass
            try:
                forward_box.find_element_by_css_selector("[node-type='originInput']").click() # 转发评论的最源头复选框勾选
            except:
                pass

            # 评论
            input_text = forward_box.find_element_by_css_selector("[title='转发微博内容']") # 输入框
            input_text.click() # 激活输入文本框
            with open('spy_comment.txt') as f:
                comments = f.read().split('\n')
            k = random.randint(0, len(comments) - 1) # 获得随机数
            input_text.send_keys(comments[k])

            time.sleep(2)
            forward_box.find_element_by_css_selector("[node-type='submit']").click() # 转发按钮

        # 把ID用最新的
        top_item_id = new_top_item_id

    # 间隔刷新时间
    time.sleep(re_time)
# 功能介绍
本项目简单实现微博爬虫相关功能：
1. dig.py：爬取某用户近期发布信息和图片（没有大规模爬取，怕被封号）
2. spy.py：监控某用户是否发了新微博，若检测到有发布，自动点赞+评论+转发（评论从评论库中随机选取，用户可自定义评论库 spy_comment.txt）

（用户自定义内容可见代码头部）

# 环境
python == 3.7

selenium

# 结果展示
爬取图片大概格式可见 demp 文件夹

# 相关问题
微博登录有时会要求验证码，这时候重新运行代码即可

# 注意
本项目仅供学习交流使用，请勿做出侵犯他人隐私、打扰他人生活等行为。

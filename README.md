# qiangke
暨南大学抢课脚本（适用于第一阶段的专业课，第二第三阶段）
**这是谷歌浏览器的版本，火狐浏览器版本看原仓库**
ChromeDriver下载浏览器对应版本：https://googlechromelabs.github.io/chrome-for-testing/
旧版：https://developer.chrome.com/docs/chromedriver/downloads

# 使用方法
1. 把chromedriver.exe放在与main.py同一目录下
2. 安装selenium库：pip install selenium（用于获取cookie）
3. 修改main.py中main函数里的设置（已整合）
4. 运行main.py，把验证滑块过掉，等待
5. 输出课程名及监测次数则标明部署成功

# 基本原理
每隔一定时间获取一次选课记录，筛选出给定课程，如果课程有余量则选课，反之继续等待

# 注意事项
1. 验证码识别代码注释掉了，我不会搞，有需要的去原仓库
2. token获取时偶现失败现象，时间有限并未深究原因，一般重启即可
3. 获取课程信息频率不能太高，默认为10s一次，频率过高可能被风控
4. 本脚本用于帮助选不到课就难以毕业的同学，请勿用于其他不良用途

# 有效日期
截止于 2024/6/18 16：37 实测有效

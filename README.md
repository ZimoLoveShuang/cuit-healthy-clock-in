# cuit-healthy-clock-in
成都信息工程大学健康打卡脚本，配合腾讯云函数使用

1. `clone`此仓库
    ```shell script
   git clone https://github.com/ZimoLoveShuang/cuit-healthy-clock-in.git
   ```
2. 配置`index.py`中的`username`，`password`，`key`等
    - `key`是`server酱`的`key`，获取`key`参考[server酱官方说明](http://sc.ftqq.com/3.version)
    - `username` 学号
    - `password` 密码
    - `isLeave` 是否开启请假，每天
    - `destination` 请假目的地
    - `reason` 请假理由
    - `isFridayAutoLeave` 是否开启周五自动请假，仅周五，一次请三天，也就是周五到周末都可以随意出入校门，当然前提是**辅导员审核通过**的情况下
    - **注意：只有destination和reason都填了内容才会提交请假的打卡，否则提交不请假的打卡**
2. 登陆腾讯云，并打开云函数控制台，[直接戳这里，快人一步](https://console.cloud.tencent.com/scf/index?rid=1)
3. 新建云函数，运行环境选择`python3.6`，创建方式选择空白函数，然后下一步
4. 提交方法选择上传文件夹，选择你刚刚克隆下来的文件夹，然后点击下面的高级设置，设置超时时间为`60秒`
5. 点击保存并测试，如果没有意外，你应该可以收到一条微信通知
6. 配置触发器，进行定时打卡，下面的cron表达式代表每天早上八点十分执行，更多用法请参考[官方文档](https://cloud.tencent.com/document/product/583/9708)
    ```shell script
    0 10 8 * * * *
    ```
7. enjoy it!!!

# 特性

1. 支持自动请假
2. 支持周五自动请假
3. 配合云函数自动打卡
4. 支持打卡消息推送

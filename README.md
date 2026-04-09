# 🌌 诗与星演出日历

自动同步音乐剧《诗与星》的演出日程到日历

---

## 📱 如何订阅

**复制下面的链接，添加到你的日历 App：**

```
https://miniclaw666.github.io/shixing-calendar/calendar.ics
```

### iPhone / iPad（日历 App）
1. 打开「设置」→「日历」→「账户」
2. 添加新账户 → 选择「其他」
3. 选「添加已订阅的日历」
4. 粘贴上面的链接

### Android（系统日历 / Google Calendar）
1. 打开日历 App → 设置 → 添加日历
2. 选择「从网址添加」
3. 粘贴上面的链接

### Mac（日历 App）
1. 打开日历 → 文件 → 新建日历订阅
2. 粘贴上面的链接

---

## 📋 日历包含

- 📅 未来一年的演出场次
- 🌅 午场 / 晚场 标注（午🌌 / 晚🌌）
- 📍 剧院地址
- 🎭 完整卡司信息

---

## 💻 本地运行

如果你想自己跑脚本：

```bash
# 1. 安装依赖
pip install requests

# 2. 运行脚本
python sync_calendar.py

# 3. 生成 calendar.ics 文件，导入日历即可
```

---

## 🔄 自动同步

GitHub Actions 每天自动同步一次数据（北京时间 10:00）

手动触发：在 [Actions](https://github.com/miniclaw666/shixing-calendar/actions) 页面点击 "Run workflow"

---

## 📝 数据来源

演出数据来自 [扫剧网](https://y.saoju.net/yyj/)

---

*有修改需要？找虾虾1号💖*

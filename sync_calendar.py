#!/usr/bin/env python3
"""
《诗与星》演出信息同步脚本
自动获取演出数据并生成 calendar.ics
时区: Asia/Shanghai (UTC+8)
"""

import json
import os
import requests
from datetime import datetime, timedelta
from urllib.parse import quote

# 配置
MUSICAL = "诗与星"
API_URL = "https://y.saoju.net/yyj/api/search_musical_show/"
ICS_FILE = "calendar.ics"

def get_date_range():
    """获取查询日期范围：过去1个月到未来1年"""
    today = datetime.now()
    start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = (today + timedelta(days=365)).strftime("%Y-%m-%d")
    return start_date, end_date

def fetch_shows():
    """从 API 获取演出数据"""
    start_date, end_date = get_date_range()
    # 中文需要 URL 编码
    encoded_musical = quote(MUSICAL)
    url = f"{API_URL}?musical={encoded_musical}&begin_date={start_date}&end_date={end_date}"

    print(f"获取 {MUSICAL} 演出信息...")
    print(f"日期范围: {start_date} ~ {end_date}")
    print(f"请求URL: {url}")

    response = requests.get(url)
    print(f"状态码: {response.status_code}")
    
    # 调试：打印原始响应前500字符
    print(f"原始响应: {response.text[:500]}")

    data = response.json()
    shows = data.get("show_list", [])
    print(f"获取到 {len(shows)} 场演出")
    return shows

def escape_ics_text(text):
    """转义 ICS 特殊字符"""
    if not text:
        return ""
    return text.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")

def create_ics_event(show):
    """创建 ICS 事件"""
    # 解析时间 - API 返回格式 "2026-03-11 19:30"
    time_str = show.get("time", "")
    
    try:
        # 先尝试空格分隔格式 (北京时间)
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        
        # 北京时间 14:30 = 午场, 19:30 = 晚场
        if dt.hour == 14:
            summary = "午💫诗与星"
        else:
            summary = "晚💫诗与星"
    except Exception as e:
        print(f"⚠️ 时间解析失败: {time_str}, 错误: {e}")
        summary = "诗与星"
        dt = None

    # 时间格式 (ICS 格式)
    if dt:
        start = dt.strftime("%Y%m%dT%H%M%S")
        end_dt = dt.replace(hour=dt.hour + 2, minute=30)
        end = end_dt.strftime("%Y%m%dT%H%M%S")
    else:
        start = end = ""

    # 地点
    theatre = escape_ics_text(show.get("theatre", ""))
    city = escape_ics_text(show.get("city", ""))

    # 描述：包含城市、剧院、卡司
    description = f"城市: {city}\\n"
    description += f"剧院: {theatre}\\n\\n"

    cast = show.get("cast", [])
    if cast:
        description += "卡司:\\n"
        for c in cast:
            role = escape_ics_text(c.get("role", ""))
            artist = escape_ics_text(c.get("artist", ""))
            description += f"- {role}: {artist}\\n"

    # 唯一ID
    uid = f"shixing-{time_str.replace(' ', '-').replace(':', '')}"

    # 生成 ICS 事件
    event = f"""BEGIN:VEVENT
UID:{uid}@shixing-calendar
DTSTART:{start}
DTEND:{end}
SUMMARY:{escape_ics_text(summary)}
DESCRIPTION:{description}
LOCATION:{theatre}
END:VEVENT
"""
    return event

def generate_ics(shows):
    """生成 ICS 日历文件"""
    ics_header = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//shixing-calendar//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:诗与星演出日历
X-WR-TIMEZONE:Asia/Shanghai
X-WR-CALDESC:音乐剧《诗与星》演出日程 (时区: Asia/Shanghai)
"""

    ics_footer = "END:VCALENDAR"

    events = ""
    for show in shows:
        events += "\n" + create_ics_event(show)

    return ics_header + events + "\n" + ics_footer

def main():
    print("=" * 50)
    print("诗与星演出同步开始")
    print("=" * 50)

    shows = fetch_shows()

    if not shows:
        print("⚠️ 没有获取到演出数据")
        ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//shixing-calendar//EN
X-WR-CALNAME:诗与星演出日历
END:VCALENDAR
"""
    else:
        ics_content = generate_ics(shows)

    # 保存
    with open(ICS_FILE, "w", encoding="utf-8") as f:
        f.write(ics_content)

    print(f"✅ 已生成 {ICS_FILE}")
    print(f"共 {len(shows)} 场演出")

if __name__ == "__main__":
    main()

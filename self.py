
import requests
import difflib

urls = ["https://mirror.ghproxy.com/https://raw.githubusercontent.com/YaMo335/TV/refs/heads/master/output/result.txt"]

final = []

def txt_decode(file_content):
    result = []
    for line in file_content.split("\n"):
        line = line.strip()
        if "#genre#" not in line and line != "":
            r = line.split(",")          
            result.append({
                "name": r[0],
                "url": r[1]
            })
    return result
        


def m3u8_decode(file_content):
    tv_name = ""
    result = []
    for file_line in file_content.split("\n"):
        file_line = file_line.strip()
        if file_line.startswith("#EXTINF"):
            tv_name = file_line.split(",")[-1]
        elif file_line and not file_line.startswith("#"):
            result.append({
                "name": tv_name,
                "url": file_line
            })
        # tv_name = ""
    return result


def isSimilar(str1, str2, threshold=0.8):
    ratio = difflib.SequenceMatcher(None, str1, str2).ratio()
    return ratio >= threshold

tvData = {
    "📺央视频道": [
        "CCTV-1综合",
        "CCTV-2财经",
        "CCTV-3综艺",
        "CCTV-4中文国际",
        "CCTV-5体育",
        "CCTV-5+体育赛事",
        "CCTV-6电影",
        "CCTV-7国防军事",
        "CCTV-8电视剧",
        "CCTV-9纪录",
        "CCTV-10科教",
        "CCTV-11戏曲",
        "CCTV-12社会与法",
        "CCTV-13新闻",
        "CCTV-14少儿",
        "CCTV-15音乐"
    ],
    "📡卫视频道" : [
        "安徽卫视",
        "东方卫视",
        "江苏卫视",
        "天津卫视",
        "重庆卫视",
        "黑龙江卫视",
        "吉林卫视",
        "辽宁卫视",
        "内蒙古卫视",
        "宁夏卫视",
        "甘肃卫视",
        "青海卫视",
        "陕西卫视",
        "河北卫视",
        "山西卫视",
        "山东卫视",
        "北京卫视",
        "河南卫视",
        "湖北卫视",
        "湖南卫视",
        "江西卫视",
        "浙江卫视",
        "东南卫视",
        "厦门卫视",
        "广东卫视",
        "深圳卫视",
        "广西卫视",
        "云南卫视",
        "贵州卫视",
        "四川卫视",
        "新疆卫视",
        "海南卫视"
    ],
    "🏠广东频道" : [
        "广东卫视",
        "广东珠江",
        "广东新闻",
        "大湾区卫视",
        "广州影视",
        "深圳卫视",
    ],
    "🌊港·澳·台" : [
        "翡翠台",
        "明珠台",
        "凤凰中文",
        "凤凰资讯",
        "凤凰香港",
        "凤凰卫视",
        "TVBS亚洲",
        "香港卫视",
    ],
    "🏀体育频道" : [
        "CCTV-5",
        "CCTV-5+",
        "广东体育",
        "纬来体育",
        "五星体育",
        "体育赛事",
        "劲爆体育",
        "爱体育",
        "超级体育",
        "精品体育",
        "广州竞赛",
    ]
}

allTvs = []

for url in urls:
    # global allTVs
    r = requests.get(url)
    r.encoding = "utf-8"
    allTvs.extend(txt_decode(r.text))

for key,value in tvData.items():
    final.append(f"{key},#genre#")
    for name in value:
        haveOne = False
        for tv in allTvs:
            if isSimilar(name, tv["name"]):
                final.append(f"{name},{tv['url']}")
                haveOne = True
        if not haveOne:
            final.append(f"{name},none")

with open("./self.txt","w",encoding="utf-8") as f:
    f.write("\n".join(final))


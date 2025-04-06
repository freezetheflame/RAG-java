import urllib.request
from bs4 import BeautifulSoup
import re
import xlwt

# 正则表达式模式
findLink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    savepath = "豆瓣电影Top250.xls"
    saveData(datalist, savepath)
    print("爬取完毕")


def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=head)
    try:
        response = urllib.request.urlopen(req)
        return response.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(f"访问失败: {e.reason}")
        return None


def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = askURL(url)
        if not html:
            continue

        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            data = []
            item = str(item)

            # 链接
            link = re.findall(findLink, item)[0] if re.findall(findLink, item) else ""
            data.append(link)

            # 图片
            imgSrc = re.findall(findImgSrc, item)[0] if re.findall(findImgSrc, item) else ""
            data.append(imgSrc)

            # 标题
            titles = re.findall(findTitle, item)
            if len(titles) == 2:
                data.append(titles[0])
                data.append(titles[1].replace("/", ""))
            else:
                data.append(titles[0] if titles else "")
                data.append("")

            # 评分
            rating = re.findall(findRating, item)[0] if re.findall(findRating, item) else ""
            data.append(rating)

            # 评价数
            judgeNum = re.findall(findJudge, item)[0] if re.findall(findJudge, item) else "0"
            data.append(judgeNum)

            # 概况
            inq = re.findall(findInq, item)
            data.append(inq[0].replace("。", "") if inq else "")

            # 相关信息 - 修复重点
            bd_match = re.findall(findBd, item)
            if bd_match:
                bd = bd_match[0]
                bd = re.sub(r'<br(\s+)?/>(\s+)?', " ", bd)
                bd = re.sub(r'/', " ", bd)
                data.append(bd.strip())
            else:
                data.append("")

            datalist.append(data)
    return datalist


def saveData(datalist, savepath):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet('豆瓣电影Top250')
    cols = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i, col in enumerate(cols):
        sheet.write(0, i, col)
    for i, data in enumerate(datalist, 1):
        for j, val in enumerate(data):
            sheet.write(i, j, val)
    book.save(savepath)


if __name__ == "__main__":
    main()
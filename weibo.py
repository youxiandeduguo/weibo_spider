import requests
import csv
import time
import random


def get_son_comment(max_id2, id2, uid2):
    url = f"https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id={id2}&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id={max_id2}&count=20&uid={uid2}&locale=zh-CN"
    #       https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id=5038300825913938&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id=82526154517874&count=20&uid=1396506364&locale=zh-CN
    # print(url)
    rep3 = requests.get(url, headers=headers)
    rep3.encoding = rep3.apparent_encoding
    # print(rep.text)
    comment2 = rep3.json()
    data2 = comment2['data']
    all_dic = {}
    # print(len(data))
    comment_count = 0
    for i in range(len(data2)):
        dic = {
            "name": data2[i]['user']['screen_name'],
            "content": data2[i]['text_raw'],
            "time": data2[i]['created_at'],
            "position": data2[i]['user']['location'],
            "like": data2[i]['like_counts']
        }
        csvwriter.writerow(dic.values())
        comment_count += 1

    count = '20'
    max_id2 = str(comment2['max_id'])
    rep3.close()

    return max_id2, comment_count


def get_url(count, max_id1, id1, uid1):
    url = f"https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={id1}&is_show_bulletin=2&is_mix=0{max_id1}&count={count}&uid={uid1}&fetch_level=0&locale=zh-CN"
    # print(url)
    # print(url)
    rep2 = requests.get(url, headers=headers)
    rep2.encoding = rep2.apparent_encoding
    # print(rep.text)
    comment = rep2.json()
    data = comment['data']
    all_dic = {}
    # print(len(data))
    comment_count2 = 0
    for i in range(len(data)):

        dic = {
            "name": data[i]['user']['screen_name'],
            "content": data[i]['text_raw'],
            "time": data[i]['created_at'],
            "position": data[i]['user']['location'],
            "like": data[i]['like_counts']
        }
        csvwriter.writerow(dic.values())
        comment_count2 += 1

        # https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=5057090198966603&is_show_bulletin=2&is_mix=0&count=10&uid=1989660417&fetch_level=0&locale=zh-CN
        # https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id=5057090198966603&is_show_bulletin=2&is_mix=0&max_id=149460054353095&count=20&uid=1989660417&fetch_level=0&locale=zh-CN
        # https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id=5057090198966603&is_show_bulletin=2&is_mix=0&max_id=140251644934475&count=20&uid=1989660417&fetch_level=0&locale=zh-CN
        total_number = data[i]['total_number']
        page_num=int(total_number/20)
        if total_number != 0:
            id2 = data[i]['id']
            uid2 = data[i]['user']['id']
            max_id2 = "0"
            for m in range(0,page_num+2):
                # print(max_id2)
                flag = 0
                time.sleep(random.random())
                max_id2, the_cot = get_son_comment(max_id2, id2, uid2)
                if max_id2=='0':
                    break
                comment_count2 += the_cot

    count = '20'
    max_id = "&max_id=" + str(comment['max_id'])
    rep2.close()

    return count, max_id, comment['total_number'], comment_count2


def get_sonpage(id, uid, csvwriter):
    comment_count = 0
    count = '10'
    max_id = ''
    time.sleep(random.random())
    count, max_id, total, the_count = get_url(count, max_id, id, uid)
    page = int((total / 20) + 2)
    # print(page)
    comment_count += the_count
    for i in range(2, page):
        time.sleep(random.random()+1)
        # print(page)
        count, max_id, total, the_count = get_url(count, max_id, id, uid)
        if max_id=="&max_id=0":
            break
        comment_count += the_count
    return comment_count


def get_main1():
    url = "https://weibo.com/ajax/feed/hottimeline?since_id=0&refresh=1&group_id=1028034488&containerid=102803_ctg1_1988_-_ctg1_1988&extparam=discover%7Cnew_feed&max_id=0&count=10"

    respond1 = requests.get(url, headers=headers)

    json_data = respond1.json()
    statues = json_data['statuses']
    comment_count = 0
    for i in range(len(statues)):
        print(i)
        id = statues[i]['id']
        uid = statues[i]['user']['id']
        comment_count += get_sonpage(id, uid, csvwriter)
    respond1.close()
    return comment_count


def get_main(page_cot):
    url = f"https://weibo.com/ajax/feed/hottimeline?since_id=0&refresh=1&group_id=1028034488&containerid=102803_ctg1_1988_-_ctg1_1988&extparam=discover%7Cnew_feed&max_id={page_cot}&count=10"

    respond = requests.get(url, headers=headers)

    json_data = respond.json()
    statues = json_data['statuses']
    comment_count = 0
    for i in range(len(statues)):
        print(i)
        id = statues[i]['id']
        uid = statues[i]['user']['id']
        comment_count += get_sonpage(id, uid, csvwriter)
    respond.close()
    return comment_count


if __name__ == '__main__':
    goal_comment = 100000
    comment_count = 0
    headers = {
        "Referer": "https://weibo.com/hot/weibo/102803",
        "Cookie": 'SINAGLOBAL=2264849924409.489.1720702968249; SCF=Atcx0RUrDyyOsykK2zMgkOAZRPrDJIq_nCMbC4tjF6rWKPPClRc4mCZsUOuDwJMxvCT7y9Qx8xONNFSmRCj9_yM.; UOR=,,cn.bing.com; ULV=1722219171574:9:9:2:305400004760.0125.1722219171554:1722213468009; PC_TOKEN=310f24b363; SUB=_2A25KFM99DeRhGeFH6FMZ-CrEyTmIHXVpaE61rDV8PUNbmtB-LXnakW9Ne2S8aV7J3C-qE7lCDjGlgwwgI3WUPnuq; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhIFNk5m3Jp5fN0dXplZPeo5NHD95QN1Kep1hnX1hzfWs4Dqcje9JDy9JpQIJ8NIgvL; ALF=02_1731742765; XSRF-TOKEN=hcB2iIFsBzdy6PQhCVV-B6L0; WBPSESS=2iln6soxPrjFtZX647xt5z078l6NpeDryWMfK47wzV1RA8RSHwdYVm3-44US-Uawv-7LVm-TJo7ouLQJqnKDMHVgVRRdK6d9fByG-Nl51xy7dqsIrwWi4NVz4so3hQwDRqELOAEQSqQ3wIIZ2ggl0g==',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }
    #
    f = open("weibo时尚区.csv", mode='a', encoding="utf-8", newline='')
    csvwriter = csv.writer(f)
    page_cot = 0
    #0
    comment_count += get_main1()
    while comment_count < goal_comment:
        print('-' + str(page_cot))
        time.sleep(random.random()+1)
        comment_count += get_main(page_cot)
        page_cot += 1
    #https://weibo.com/ajax/feed/hottimeline?since_id=0&refresh=1&group_id=1028031988&containerid=102803_ctg1_1988_-_ctg1_1988&extparam=discover%7Cnew_feed&max_id=0&count=10
    #https://weibo.com/ajax/feed/hottimeline?refresh=2&group_id=1028034388&containerid=102803_ctg1_4388_-_ctg1_4388&extparam=discover%7Cnew_feed&max_id=1&count=10
    #https://weibo.com/ajax/feed/hottimeline?refresh=2&group_id=1028034388&containerid=102803_ctg1_4388_-_ctg1_4388&extparam=discover%7Cnew_feed&max_id=2&count=10
    #https://weibo.com/ajax/feed/hottimeline?refresh=2&group_id=1028034388&containerid=102803_ctg1_4388_-_ctg1_4388&extparam=discover%7Cnew_feed&max_id=3&count=10

    #https://weibo.com/ajax/feed/hottimeline?since_id=0&refresh=1&group_id=1028031988&containerid=102803_ctg1_1988_-_ctg1_1988&extparam=discover%7Cnew_feed&max_id=0&count=10
    #https://weibo.com/ajax/feed/hottimeline?refresh=2&group_id=1028034388&containerid=102803_ctg1_4388_-_ctg1_4388&extparam=discover%7Cnew_feed&max_id=1&count=10
    #

    # get_sonpage('5059331001947434', '7826525638', csvwriter)
    f.close()

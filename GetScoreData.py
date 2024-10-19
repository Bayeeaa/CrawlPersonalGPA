import json
import requests


def send_to_server(url, headers, body):
    session = requests.Session()
    response = session.post(url, headers=headers, data=body).text
    response_json = json.loads(response)
    return response_json


def print_data(response, sum_score):
    length = len(response['items'])
    for t in range(length):
        subject_score = str(round(float(response['items'][t]['jd']), 1))
        subject = response['items'][t]['kcmc']
        print(subject + "：" + subject_score)
        sum_score += float(response['items'][t]['jd'])
    avg_score = round(round(sum_score, 3) / float(len(response['items'])), 2)
    avg_xq_score = str(round(round(sum_score, 3) / float(len(response['items'])), 2))
    sum_xq_score = str(round(sum_score, 2))
    print("该学期总绩点为" + sum_xq_score + "，平均绩点为" + avg_xq_score)
    print("----------------------------")
    return avg_score


class GetScore():
    def __init__(self):
        self.url = "https://jwxt.zufe.edu.cn/jwglxt/cjcx/cjcx_cxXsgrcj.html?doType=query&gnmkdm=N305005"
        self.headers = {
            "User-Agent": "",
            "Cookie": ""
        }
        self.xq_num = ["3", "12", "16"]
        self.xn_num = ["2023", "2024", "2025", "2026"]
        self.body = {
            "xnm": "2023",
            "xqm": "3",
            "queryModel.showCount": "15"
        }

    def analysis_xq(self, length, i, j):
        if length == 0:
            return 0
        elif self.xq_num[j] == "3":
            print(self.xn_num[i] + "第一学年")
        elif self.xq_num[j] == "12":
            print(self.xn_num[i] + "第二学年")
        elif self.xq_num[j] == "16":
            print(self.xn_num[i] + "第三学年")

    def get_data(self):
        all_avg_score = all_len = sum_score = 0
        for i in range(len(self.xn_num)):
            for j in range(len(self.xq_num)):
                self.body["xnm"] = self.xn_num[i]
                self.body["xqm"] = self.xq_num[j]
                response = send_to_server(self.url, self.headers, self.body)
                length = len(response['items'])
                if self.analysis_xq(length, i, j) == 0:
                    break
                else:
                    all_len += 1
                all_avg_score += print_data(response, sum_score)
        all_avg_score_str = str(round(all_avg_score / all_len, 2))
        print("全年总平均绩点为：" + all_avg_score_str)
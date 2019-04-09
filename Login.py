import requests
import Getcookie
import re
import PIL
import os
from PIL import Image
from bs4 import BeautifulSoup
import urllib
import lxml
from Chulikebiao import ResolvePage

class Who:
    def __init__(self, user, pswd):
        self.id = user
        self.password = pswd


class University:
    def __init__(self, student, pass1):
        self.student = student
        self.pass1 = pass1
        self.baseurl = 'https://jwjs.njit.casbs.cn/'
        self.session = requests.session()
        self.session.headers['Cookie'] = '%s;ASP.NET_SessionId=btoi3q455tfchr45dpt2v224 ' % (Getcookie.getcookie(self.student.id,self.pass1))
        self.session.headers['User-Agent']= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'

    def login(self):
        # session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        # session.headers['Cookie'] = 'web_vpn_user_token=3d37659bb76012af87043548431b190b;ASP.NET_SessionId=btoi3q455tfchr45dpt2v224 '
        # baseurl ='https://jwjs.njit.casbs.cn/'
        res = self.session.get(self.baseurl)
        content = res.content
        # content.decode()
        cont = content.decode('GBK', errors='ignore')
        # print(cont)
        soup = BeautifulSoup(cont, 'html.parser')
        view = soup.find(attrs={'name': '_VIEWSTATE'})
        view = soup.find('input')['value']
        # print(view)
        imgurl = 'https://jwjs.njit.casbs.cn/CheckCode.aspx?'
        imgres = self.session.get(imgurl, stream=True)
        img = imgres.content
        with open('code.jpg', 'wb') as f:
            f.write(img)
        jpg = Image.open('{}/code.jpg'.format(os.getcwd()))
        jpg.show()
        jpg.close()
        RadioButtonList1 = u"学生"
        code = input('输入密码')
        data = {
            "__VIEWSTATE": view,
            "txtUserName": self.student.id,
            "Textbox1": "",
            "TextBox2": self.student.password,
            "txtSecretCode": code,
            "RadioButtonList1": '学生'.encode('gbk'),
            "Button1": "",
            "lbLanguage": "",
            "hidPdrs": "",
            "hidsc": "",
        }
        posturl = 'https://jwjs.njit.casbs.cn/default2.aspx'
        # print(session.headers)
        # print(data)
        loginres = self.session.post(posturl, data=data)
        # print(loginres.text)
        # res_chengji = self.session.get('https://jwjs.njit.casbs.cn/xs_main.aspx?xh=202170811')
        # print(res_chengji.content.decode('GBK','ignore'))
        loginurl = self.baseurl + '/xs_main.aspx?xh=' + self.student.id
        # print(loginurl)
        logcont = self.session.get(loginurl)
        # print(logcont.content)
        logcont = self.session.get(loginurl).content.decode('GBK')
        pattern = re.compile('<span id="xhxm">(.*?)</span>')
        # print(logcont)
        xhxm = re.findall(pattern, logcont)
        name = xhxm[0].replace('同学', '')
        # 获取姓名的编码
        self.student.urlname = urllib.parse.quote_plus(str(name))

            # 获取学生课表

    def getclass(self):
        loginurl = self.baseurl + '/xs_main.aspx?xh=' + self.student.id
        kburl = self.baseurl + '/xskbcx.aspx?xh=' + self.student.id + \
                '&xm=' + self.student.urlname + '&gnmkdm=N121603'
        # print(kburl)
        self.session.headers['Referer'] = loginurl
        kbresponse = self.session.get(kburl)
        kbcont = kbresponse.text
        table  = BeautifulSoup(kbcont,'lxml')
        chuli = ResolvePage(kbcont)
        chuli.resolveScheduleContent()
        print(chuli.getSchedule())
        #print(table.table['Table1'])
        return chuli.getSchedule()

        # table = BeautifulSoup(kbcont.text, "lxml")
        # keys = [i.text for i in table.find('tr').find_all('td')]
        # classes = [
        #     dict(zip(
        #         keys, [i.text.strip() for i in tr.find_all('td')]))
        #     for tr in table.find_all('tr')[1:]]
        # return classes

    def highest_grade(self):
        btn_zg = "课程最高成绩".encode("GBK")
        posturl = self.baseurl + \
                  '/xs_main.aspx?xh=' + self.student.id
        self.session.headers['Referer'] = self.baseurl + \
                                          '/xs_main.aspx?xh=' + self.student.id
        gtrurl = self.baseurl + '/xscjcx.aspx?xh=' + self.student.id + \
                 '&xm=' + self.student.urlname + '&gnmkdm=N121617'
        gtrresponse = self.session.get(gtrurl).content.decode('GBK', errors='ignore')
        soup = BeautifulSoup(gtrresponse, "lxml")
        csrf_token = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        print(csrf_token)

        data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'hidLanguage': '',
            '__VIEWSTATE': csrf_token,
            'ddlXN': '',
            'ddlXQ': '',
            'ddl_kcxz': '',
            'btn_zg':"课程最高成绩".encode("GBK") ,

        }

        self.session.headers[
            'Referer'] =gtrurl

        #print(self.session.headers)
        # self.session.headers['Cookie'] += 'iPlanetDirectoryPro=AQIC5wM2LY4SfcwdqY7%2BPPnxBedAYBIVChfcOZgbM6mrNgg%3D%40AAJTSQACMDE%3D%23;'
        res = self.session.post(
            gtrurl, data=data)
        # res = self.session.post(gtrurl, data=data)

        # print(res.decode('GbK',errors='ignore'))
        # res = self.session.get(gtrurl)
        #print(res.content.decode('GBK'))
        soup = BeautifulSoup(res.text, "lxml")
        table = soup.select_one('.datelist')
        keys = [i.text for i in table.find('tr').find_all('td')]
        scores = [
            dict(zip(
                keys, [i.text.strip() for i in tr.find_all('td')]))
            for tr in table.find_all('tr')[1:]]

        return scores

    # 获取成绩
    def GradeTestResults(self, year, xueqi):
        posturl = self.baseurl + \
                  '/xs_main.aspx?xh=' + self.student.id
        self.session.headers['Referer'] = self.baseurl + \
                                          '/xs_main.aspx?xh=' + self.student.id
        gtrurl = self.baseurl + '/xscjcx_dq.aspx?xh=' + self.student.id + \
                 '&xm=' + self.student.urlname + '&gnmkdm=N121605'
        gtrresponse = self.session.get(gtrurl).content.decode('GBK', errors='ignore')
        soup = BeautifulSoup(gtrresponse, "lxml")
        csrf_token = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        data = {
            '__EVENTTARGET': 'ddlxq',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': csrf_token,
            'ddlxn': year,
            'ddlxq': xueqi,
        }
        self.session.headers['Referer'] = gtrurl
        gtrresponse = self.session.post(gtrurl, data=data).content.decode('GBK', errors='ignore')
        soup = BeautifulSoup(gtrresponse, "lxml")
        csrf_token = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            # 'hidLanguage': '',
            '__VIEWSTATE': csrf_token,
            'ddlxn': year,
            'ddlxq': xueqi,
            # 'ddl_kcxz':'',
            'btnCX': ' 查  询 '.encode('gbk'),

        }
        res = self.session.post(gtrurl, data=data)
        # print(res.decode('GbK',errors='ignore'))
        # res = self.session.get(gtrurl)
        # print(res.content.decode('GBK'))
        soup = BeautifulSoup(res.text, "lxml")
        table = soup.select_one('.datelist')
        keys = [i.text for i in table.find('tr').find_all('td')]
        scores = [
            dict(zip(
                keys, [i.text.strip() for i in tr.find_all('td')]))
            for tr in table.find_all('tr')[1:]]
        # debug:
        # print(sorted([[i['成绩'], i['课程名称']] for i in scores], reverse=True))
        # print(scores)
        return scores

    def unpass(self):
        posturl = self.baseurl + \
                  '/xs_main.aspx?xh=' + self.student.id
        self.session.headers['Referer'] = posturl
        gtrurl = self.baseurl + '/xscjcx_dq.aspx?xh=' + self.student.id + \
                '&xm=' + self.student.urlname + '&gnmkdm=N121617'
        res = self.session.get(gtrurl)
        print(res.text)

        soup = BeautifulSoup(res.content.decode('GBK',errors='ignore'), "lxml")
        csrf_token = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        print(csrf_token)

        data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'hidLanguage': '',
            '__VIEWSTATE': csrf_token,
            'ddlXN': '',
            'ddlXQ': '',
            'ddl_kcxz': '',
            'Button2': '%CE%B4%CD%A8%B9%FD%B3%C9%BC%A8'
  }

        self.session.headers[
            'Referer'] = gtrurl

        # print(self.session.headers)
        # self.session.headers['Cookie'] += 'iPlanetDirectoryPro=AQIC5wM2LY4SfcwdqY7%2BPPnxBedAYBIVChfcOZgbM6mrNgg%3D%40AAJTSQACMDE%3D%23;'
        res = self.session.post(
            gtrurl, data=data)
        # res = self.session.post(gtrurl, data=data)

        # print(res.decode('GbK',errors='ignore'))
        # res = self.session.get(gtrurl)
        # print(res.content.decode('GBK'))
        soup = BeautifulSoup(res.text, "lxml")
        table = soup.select_one('.datelist')
        keys = [i.text for i in table.find('tr').find_all('td')]
        scores = [
            dict(zip(
                keys, [i.text.strip() for i in tr.find_all('td')]))
            for tr in table.find_all('tr')[1:]]

        return scores

if __name__ == '__main__':
    id = '202170811'
    password0 = '317474'
    password = 'ilovechenshun123'
    s = Who(id, password)
    pa = University(s, password0)
    pa.login()
    pa.getclass()
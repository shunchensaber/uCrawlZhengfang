from bs4 import BeautifulSoup
import re
class ResolvePage:
    soup = None
    schedule = []  #存放课表
    scheduleTime = []  #存放当前学年学期, 索引0为学年, 索引1为学期

    def __init__(self, pageCode):  #pageCode可以是爬取的源码也可以是源码的文件句柄
        self.soup = BeautifulSoup(pageCode, 'lxml')

    def getSchedule(self):
        return self.schedule
    def getScheduleYear(self):
        return self.scheduleTime[0]
    def getScheduleSemester(self):
        return self.scheduleTime[1]

    def resolveScheduleTime(self):  #获得课表所在学年与学期
        for option in self.soup.findAll('option'):
            if option.get('selected') == 'selected':
                self.scheduleTime.append(option.get('value'))

    def resolveScheduleContent(self):
        classes = []

        #取下包含了课表内容的源码
        rows = self.soup.findAll('tr')[4:17]
        for row in rows:
            columns = row.findAll('td')
            for column in columns:
                if column.get('align') == 'Center' and column.text != '\xa0':
                    classes.append(str(column))

        #去除无用部分,留下<\br>用来分隔各项
        for i in range(len(classes)):
            index = classes[i].find('>')+1
            classes[i] = classes[i][index:-5]
        #合为一个字符串
        classes = '<br/>'.join(classes)
        #按分隔符拆开为列表
        classes =re.split(r'<br/><br/>|<br/>', classes)  #按正则表达式分割, | 为或, 遵循短路原则, 所以 | 两边顺序不可变换

        #按科目拆开
        subject = []
        for i in range(len(classes)):
            subject.append(classes[i])
            if (i+1)%5 == 0:
                self.schedule.append(subject)
                subject = []


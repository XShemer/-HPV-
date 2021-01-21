import requests
import json
import time
import datetime
import tkinter
import tkinter.messagebox

def weekChange(week):
    if week == 1:
        return '周一'
    elif week == 2:
        return '周二'
    elif week == 3:
        return '周三'
    elif week == 4:
        return '周四'
    elif week == 5:
        return '周五'
    elif week == 6:
        return '周六'
    elif week == 7:
        return '周日'


f = open('test.txt')
tk = f.readline()
cookie = 'UM_distinctid=17700ac42240-0b33a11b9e4d68-20582e26-1fa400-17700ac42295b4; _xzkj_= ' + tk + '; _xxhm_=%7B%22address%22%3A%22%E5%AE%89%E4%B9%90%E9%95%87%E5%B0%8F%E5%8C%BA%22%2C%22awardPoints%22%3A0%2C%22birthday%22%3A750096000000%2C%22createTime%22%3A1589854819000%2C%22headerImg%22%3A%22http%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2FajNVdqHZLLD2pMRmmYaQaLBDChem66aoN9svAnicpZPDx2jP21aPaPtCHBljnfwxSu9Gwia5NBAUH1tj7xa4FbVA%2F132%22%2C%22id%22%3A5547063%2C%22idCardNo%22%3A%2237010519931009501X%22%2C%22isRegisterHistory%22%3A0%2C%22latitude%22%3A36.650768%2C%22longitude%22%3A117.118713%2C%22mobile%22%3A%2215066121027%22%2C%22modifyTime%22%3A1606914586000%2C%22name%22%3A%22%E8%B0%A2%E8%B6%85%22%2C%22nickName%22%3A%22%E1%83%A6Mr%E3%80%86%C2%B0%E8%B0%A2%22%2C%22openId%22%3A%22oWzsq5_KzifgG9-xnWt65oBLhRcc%22%2C%22regionCode%22%3A%22370105%22%2C%22registerTime%22%3A1606914586000%2C%22sex%22%3A1%2C%22source%22%3A1%2C%22uFrom%22%3A%22depa_vacc_detail%22%2C%22unionid%22%3A%22oiGJM6OGsfxJNteI_rfIzkf3Jh7k%22%2C%22wxSubscribed%22%3A1%2C%22yn%22%3A1%7D; CNZZDATA1261985103=596264046-1610954889-%7C1611020154'

headers = {
    'Cookie': cookie,
    'tk': tk
}

param = {'offset': '0',
         'limit': '1000',
         'name': '',
         'regionCode': 3701,
         'isOpen': 1,
         'longitude': '117.11876678466797',
         'latitude': '36.650978088378906',
         'sortType': 1,
         'vaccineCode': '',
         'customId': 2} # customId等于2是四价 等于52是两价


def request():
    while True:
        respone = requests.get('http://wx.scmttec.com/base/department/getDepartments.do', headers=headers, params=param)
        textJson = json.loads(respone.text)
        rowsList = textJson.get('data').get('rows')

        haveList = []
        for rowItem in rowsList:
            total = rowItem.get('total')
            if(total>0):
                haveList.append(rowItem)

        print('总共查询到' + str(len(rowsList)) + '家医院，其中有苗的医院有' + str(len(haveList)) + '家')
        for haveItem in haveList:
            name = haveItem.get('name')
            total = haveItem.get('total')
            print(name + '共有疫苗：' + str(total) + '只')

            depaCode = haveItem.get('code')
            vaccCode = haveItem.get('vaccineCode')
            vaccIndex = 3
            subsribeDate = time.strftime("%Y-%m-%d", time.localtime())
            departmentVaccineId = haveItem.get('depaVaccId')
            linkmanId = '7824969'

            workDayParam = {
                'depaCode': depaCode,
                'vaccCode': vaccCode,
                'vaccIndex': vaccIndex,
                'departmentVaccineId': departmentVaccineId,
                'linkmanId': linkmanId
            }

            # {"code":"0000","data":{"dateList":["2021-01-20","2021-01-21","2021-01-22","2021-01-23","2021-01-24","2021-01-25","2021-01-26"],"subscribeDays":7},"notOk":false,"ok":true}
            workDayRespone = requests.get('https://wx.scmttec.com/order/subscribe/workDays.do', headers=headers, params=workDayParam)
            workDayJson = json.loads(workDayRespone.text)
            workDayData = workDayJson.get('data')
            if('dateList' in workDayData) :
                workDayList = workDayData.get('dateList')
                workDayStr = ','.join(workDayList)
                workDayStr = workDayStr.replace('-', '')

                subscribeAmountParam = {
                    'depaCode': depaCode,
                    'vaccCode': vaccCode,
                    'vaccIndex': vaccIndex,
                    'departmentVaccineId': departmentVaccineId,
                    'days': workDayStr
                }
                # {"code":"0000","data":[{"maxSub":198,"day":"20210120"},{"maxSub":189,"day":"20210121"},{"maxSub":185,"day":"20210122"},{"maxSub":176,"day":"20210123"},{"maxSub":187,"day":"20210124"},{"maxSub":194,"day":"20210125"},{"maxSub":200,"day":"20210126"}],"notOk":false,"ok":true}
                subscribeAmountRespone = requests.get('https://wx.scmttec.com/order/subscribe/findSubscribeAmountByDays.do', headers=headers, params=subscribeAmountParam)

                subscribeAmountJson = json.loads(subscribeAmountRespone.text)
                dataList = subscribeAmountJson.get('data')
                for dataItem in dataList:
                    maxSub = dataItem.get('maxSub')
                    day = dataItem.get('day')
                    workDayDate = datetime.datetime.strptime(day, '%Y%m%d').date()
                    week = workDayDate.isoweekday()

                    if(week == 6 or week == 7):
                        weekStr = weekChange(week)
                        tkinter.messagebox.showinfo('提示', name + ',' + day + '(' + weekStr + ')' + '有疫苗')
            else:
                continue
            time.sleep(2)
        print('---------------' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '-------------')
        time.sleep(30)

try:
    request()

except TypeError:
    tkinter.messagebox.showerror('错误', '报错了')
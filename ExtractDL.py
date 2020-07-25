import requests
from lxml import html
import json

url = 'https://parivahan.gov.in/rcdlstatus/?pur_cd=101'

def get_captcha():
    captchaimg2 = tree.xpath('//img[@id="form_rcdl:j_idt34:j_idt41"]/@src')
    imgurl='https://parivahan.gov.in'+str(captchaimg2[0])
    r=requests.get(imgurl)
    open('Captcha.jpg', 'wb').write(r.content)
    captcha=input('Enter The Captcha : ')
    return captcha


while(True):
    try:
        DL= input('License No.\t: ') 
        DL=DL.upper()
        while(True):
            DOB=input('Date Of Birth\t: ')
            while(True):
                DOB=DOB.replace('/' ,'-').replace('.','-')
                r = requests.get(url=url)
                cookies = r.cookies
                tree = html.fromstring(r.content)
                viewstate2 = tree.xpath('//input[@name="javax.faces.ViewState"]/@value')
                viewstate=viewstate2[0]
                data= {
                    'javax.faces.partial.ajax': 'true',
                    'javax.faces.source': 'form_rcdl:j_idt46',
                    'javax.faces.partial.execute': '@all',
                    'javax.faces.partial.render': 'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl',
                    'form_rcdl:j_idt46': 'form_rcdl:j_idt46',
                    'form_rcdl': 'form_rcdl',
                    'form_rcdl:tf_dlNO': DL,
                    'form_rcdl:tf_dob_input': DOB,
                    'form_rcdl:j_idt34:CaptchaID':get_captcha(),
                    'javax.faces.ViewState':viewstate 
                }

                r = requests.post(url=url, data=data, cookies=cookies)
                tree = html.fromstring(r.content)
                t1key=tree.xpath('//table[@class="table table-responsive table-striped table-condensed table-bordered"]/tr/td[1]//text()')
                t1value=tree.xpath('//table[@class="table table-responsive table-striped table-condensed table-bordered"]/tr/td[2]//text()')
                error=tree.xpath('//span[@class="ui-messages-error-detail"]/text()')
                if(error==['Verification code does not match.']):
                    print(tree.xpath('//span[@class="ui-messages-error-detail"]/text()')[0])
                    continue
                else:
                    break
            if(error!=[]):
                print(tree.xpath('//span[@class="ui-messages-error-detail"]/text()')[0])
                continue
            else:
                break

        if(t1key==[]):
            print('No DL Details Found! TRY AGAIN.')
            continue
            
        DLStatus={}
        for i in range(len(t1key)):
            DLStatus[t1key[i][0:-1]]=t1value[i]

        DLDetails={}
        DLDetailsList=tree.xpath('//table[@class="table table-responsive table-striped table-condensed table-bordered data-table"]/tr/td//text()')

        DLDetails={
            DLDetailsList[0]:{
                        DLDetailsList[1][0:-2]:DLDetailsList[2],
                        DLDetailsList[3][0:-2]:DLDetailsList[4]
                        },
            DLDetailsList[5]:{
                        DLDetailsList[6][0:-2]:DLDetailsList[7],
                        DLDetailsList[8][0:-2]:DLDetailsList[9]
                        },
            DLDetailsList[10][0:-1]:DLDetailsList[11],
            DLDetailsList[12][0:-1]:DLDetailsList[13]
        }

        VehicleDetail=[[]]
        VehicleDetail[0]=[tree.xpath('//th[@id="form_rcdl:j_idt167:j_idt168"]/span/text()')[0],tree.xpath('//th[@id="form_rcdl:j_idt167:j_idt170"]/span/text()')[0],tree.xpath('//th[@id="form_rcdl:j_idt167:j_idt172"]/span/text()')[0]]

        i=1
        while(True):
            VehicleDetail.append(tree.xpath(f'//tbody[@id="form_rcdl:j_idt167_data"]/tr[{i}]/td/text()'))
            if(VehicleDetail[i]==[]):
                break
            i+=1

        DVehicleDetails={}
        for i in range(1,len(VehicleDetail)-1):
            DVehicleDetails[i]={
                    VehicleDetail[0][0]:VehicleDetail[i][0],
                    VehicleDetail[0][1]:VehicleDetail[i][1],
                    VehicleDetail[0][2]:VehicleDetail[i][2]
                    }

        DLFINAL={}
        DLFINAL=DLStatus
        DLFINAL["Class of Vehicle Details"]=DLDetails
        DLFINAL["Driving License Validity Details"]=DVehicleDetails

        jsonfile=json.dumps(DLFINAL,indent=10)
        print(jsonfile)
        break
    except:
break
    except:

        print('Opps Something went Wrong! Check Your Internet Connection and try again')

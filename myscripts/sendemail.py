'''
授权码:ncqkzticgiosdiad
'''

import smtplib
from email.mime.text import MIMEText

def sendresult(content,receiver):

    mail_host = 'smtp.qq.com'
    mail_user = '2579964438'
    mail_pswd = 'ncqkzticgiosdiad'


    receivers = [receiver]

    message = MIMEText(content,'plain','utf-8')
    message['Subject']='吸附计算结果'
    message['From'] = "2579964438@qq.com"
    message['To']=receivers[0]

    

    smtpObj = smtplib.SMTP_SSL(mail_host)
    smtpObj.login(mail_user,mail_pswd)
    smtpObj.sendmail("2579964438@qq.com",receivers,message.as_string())
    smtpObj.quit()




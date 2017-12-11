# coding=utf-8

import smtplib
from email.mime.text import MIMEText
msg_from = '1029645297@qq.com'  # 发送方邮箱
passwd = 'dbumqtpqdakubebc'  # 填入发送方邮箱的授权码
msg_to = '1029645297@qq.com'  # 收件人邮箱
subject = "python邮件测试"  # 主题
content = "这是我使用python smtplib及email模块发送的邮件"      # 正文
msg = MIMEText(content)
msg['Subject'] = subject
msg['From'] = msg_from    # 邮件上显示的发件人，最好写成和实际发件人一致
msg['To'] = msg_to    # 邮件上显示的收件人，最好写成和实际收件人一致
print msg.as_string()
try:
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)   # 邮件服务器及端口号
    # s.set_debuglevel(1)
    s.login(msg_from, passwd)
    s.sendmail(msg_from, msg_to, msg.as_string())
    print "发送成功"
except s.SMTPException as e:
    print "发送失败:", e
finally:
    s.quit()


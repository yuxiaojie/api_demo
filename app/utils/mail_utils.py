import smtplib
from email.mime.text import MIMEText


MAIL_USER = 'no-reply'
MAIL_PWD = 'Honestar2018'
MAIL_SENDER = 'no-reply@beesmartnet.com'


def send_mail(recv, title, content, mail_host='hwsmtp.qiye.163.com', port=994):

    msg = MIMEText(content)
    msg['Subject'] = title
    smtp = smtplib.SMTP_SSL(mail_host, port=port)
    smtp.login(MAIL_SENDER, MAIL_PWD)
    smtp.sendmail(MAIL_SENDER, recv, msg.as_string())
    smtp.quit()


def send_auth_email(chan, ver_info, rev):

    try:
        send_mail(rev, '[小蜜智联] 验证电子邮箱', '''
            亲爱的用户：

                您正在为渠道{}绑定邮箱，请点击这里确认绑定该邮箱：
                https://tmp.beesmartnet.com/api/chan/safe-email/{}

                该链接24小时候自动失效，如果该请求并不是您发起的，请忽略此邮件
            '''.format(chan, ver_info))
        return True
    except smtplib.SMTPRecipientsRefused:
        return False


if __name__ == '__main__':

    print('send', ('success' if send_auth_email('test', 'qqqqqqqqqqqqqq', 'jeff.yxj@beesmartnet.com') else 'failed'))

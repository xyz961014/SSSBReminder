import smtplib
import email
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# from email.mime.base import MIMEBase
# from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr
import argparse
import ipdb

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mail_to", type=str, nargs="+", required=True,
                        help="receiver email address")
    parser.add_argument("--title", type=str, default="SSSB Update!",
                        help="mail title")
    parser.add_argument("--content", type=str, default="SSSB Update content!",
                        help="mail content")

    args = parser.parse_args()
    return args




# username，通过控制台创建的发信地址
username = 'sssb@mail.thufootball.tech'
# password，通过控制台创建的SMTP密码
password = 'SSSBTHUfootball2022'
# 自定义的回信地址，与控制台设置的无关。邮件推送发信地址不收信，收信人回信时会自动跳转到设置好的回信地址。
replyto = 'sssb@mail.thufootball.tech'


def main(args):
    # 显示的To收信地址
    rcptto = args.mail_to
    # 显示的Cc收信地址
    rcptcc = []
    # Bcc收信地址，密送人不会显示在邮件上，但可以收到邮件
    rcptbcc = []
    # 全部收信地址，包含抄送地址，单次发送不能超过60人
    #receivers = rcptto + rcptcc + rcptbcc
    receivers = rcptto

    msg = build_message(rcptto, args.title, args.content, 
                        rcptcc=rcptcc, rcptbcc=rcptbcc)
    send_mail(receivers, msg)

def build_message(rcptto, title, content, rcptcc=[], rcptbcc=[]):
    
    # 构建alternative结构
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(title)
    msg['From'] = formataddr(["SSSB Reminder", username])  # 昵称+发信地址(或代发)
    # list转为字符串
    msg['To'] = ",".join(rcptto)
    msg['Cc'] = ",".join(rcptcc)
    msg['Reply-to'] = replyto
    msg['Message-id'] = email.utils.make_msgid()
    msg['Date'] = email.utils.formatdate()
    
    # 若需要开启邮件跟踪服务，请使用以下代码设置跟踪链接头。
    # 首先域名需要备案，设置且已正确解析了CNAME配置；其次发信需要打Tag，此Tag在控制台已创建并存在，Tag创建10分钟后方可使用；
    # 设置跟踪链接头
    # tagName = 'xxxxxxx'
    #
    # # OpenTrace对应值是字符串1，固定
    # trace = {
    #     "OpenTrace": '1',  #打开邮件跟踪
    #     "LinkTrace": '1',  #点击邮件里的URL跟踪
    #     "TagName": tagName  # 控制台创建的标签tagname
    # }
    # jsonTrace = json.dumps(trace)
    # base64Trace = str(base64.b64encode(jsonTrace.encode('utf-8')), 'utf-8')
    # # print(base64Trace)
    # msg.add_header("X-AliDM-Trace", base64Trace)
    
    
    # 构建alternative的text/plain部分
    # textplain = MIMEText('自定义TEXT纯文本部分', _subtype='plain', _charset='UTF-8')
    # msg.attach(textplain)
    
    # 构建alternative的text/html部分
    texthtml = MIMEText(content, _subtype='html', _charset='UTF-8')
    msg.attach(texthtml)
    
    #附件
    # files = [r'C:\Users\Downloads\test1.jpg', r'C:\Users\Downloads\test2.jpg']
    # for t in files:
    #     part_attach1 = MIMEApplication(open(t, 'rb').read())  # 打开附件
    #     part_attach1.add_header('Content-Disposition', 'attachment', filename=t.rsplit('\\', 1)[1])  # 为附件命名
    #     msg.attach(part_attach1)  # 添加附件

    return msg


def send_mail(receivers, msg):
    try:
        # 若需要加密使用SSL，可以这样创建client
        # client = smtplib.SMTP_SSL('smtpdm.aliyun.com', 465)
        # SMTP普通端口为25或80
        client = smtplib.SMTP('smtpdm.aliyun.com', 80)
        # 开启DEBUG模式
        client.set_debuglevel(0)
        # 发件人和认证地址必须一致
        client.login(username, password)
        # 备注：若想取到DATA命令返回值,可参考smtplib的sendmail封装方法:
        # 使用SMTP.mail/SMTP.rcpt/SMTP.data方法
        # print(receivers)
        client.sendmail(username, receivers, msg.as_string())  # 支持多个收件人，最多60个
        client.quit()
        print('邮件发送成功！')
    except smtplib.SMTPConnectError as e:
        print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPAuthenticationError as e:
        print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPSenderRefused as e:
        print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPRecipientsRefused as e:
        print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPDataError as e:
        print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPException as e:
        print('邮件发送失败, ', str(e))
    except Exception as e:
        print('邮件发送异常, ', str(e))


if __name__ == "__main__":
    args = parse_args()
    main(args)

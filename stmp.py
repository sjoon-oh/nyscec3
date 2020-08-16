# [Toy Project NYSCEC]
# 0.1.2va, 20.07.31. First launched.
# written by acoustikue(SukJoon Oh)
# 
# Legal stuff:
#   This simple code follows MIT license. 
# 
# MIT License
# Copyright (c) 2020 SukJoon Oh(acoustikue)

import config as cf

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


NYSCEC_ADMIN_ID = 'your_email'
NYSCEC_ADMIN_PW = 'your_stmp_password'

NYSCEC_SMTP_SERVER = 'smtp.gmail.com'
NYSCEC_SMTP_PORT = 465

def generate_content_2(updates):

    mail_content = ''

    for info in updates:
        mail_content += ( '<p> <b>{0}</b><br> <b>New instances:</b><br>'.format(info['name']) )
        if len(info['instances']) != 0:
            for instance in info['instances']: mail_content += ( '<i>{0}</i><br>'.format(instance) )
        else:
            mail_content += 'No updates.<br>'

        mail_content += ( '<b>New posts from /jinotechboard:</b><br>')
        if len(info['posts']) != 0:
            for post in info['posts']: mail_content += ( '<i>{0}</i><br>'.format(instance) )
        else:
            mail_content += 'No updates.<br>'

        #mail_content += '<br>'
    
    mail_content += '</p>'
    return mail_content



def send_mail(subject, content, updates):
        
    #msg = MIMEText(content, _charset='utf-8')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '[NYSCEC] {0}'.format(subject)
    msg['From'] = 'your_email'
    msg['To'] = 'your_email'

    html_frame_upper = '<!doctype html><html> <head> <meta name="viewport" content="width=device-width" /> <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> <title>Simple Notice Form</title> <style> img { border: none; -ms-interpolation-mode: bicubic; max-width: 100%; } body { background-color: #f6f6f6; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; } table { border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; } table td { font-family: sans-serif; font-size: 14px; vertical-align: top; } /* ------------------------------------- BODY & CONTAINER ------------------------------------- */ .body { background-color: #f6f6f6; width: 100%; } /* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */ .container { display: block; margin: 0 auto !important; /* makes it centered */ max-width: 580px; padding: 10px; width: 580px; } .content { box-sizing: border-box; display: block; margin: 0 auto; max-width: 580px; padding: 10px; } /* ------------------------------------- HEADER, FOOTER, MAIN ------------------------------------- */ .main { background: #ffffff; border-radius: 3px; width: 100%; } .wrapper { box-sizing: border-box; padding: 20px; } .content-block { padding-bottom: 10px; padding-top: 10px; } .footer { clear: both; margin-top: 10px; text-align: center; width: 100%; } .footer td, .footer p, .footer span, .footer a { color: #999999; font-size: 14px; text-align: center; } /* ------------------------------------- TYPOGRAPHY ------------------------------------- */ h1, h2, h3, h4 { color: #000000; font-family: sans-serif; font-weight: 400; line-height: 1.4; margin: 0; margin-bottom: 30px; } h1 { font-size: 35px; font-weight: 300; text-align: center; text-transform: capitalize; } p, ul, ol { font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; margin-bottom: 15px; } p li, ul li, ol li { list-style-position: inside; margin-left: 5px; } a { color: #3498db; text-decoration: underline; } /* ------------------------------------- BUTTONS ------------------------------------- */ .btn { box-sizing: border-box; width: 100%; } .btn > tbody > tr > td { padding-bottom: 15px; } .btn table { width: auto; } .btn table td { background-color: #ffffff; border-radius: 5px; text-align: center; } .btn a { background-color: #ffffff; border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; color: #3498db; cursor: pointer; display: inline-block; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-decoration: none; text-transform: capitalize; } .btn-primary table td { background-color: #3498db; } .btn-primary a { background-color: #3498db; border-color: #3498db; color: #ffffff; } /* ------------------------------------- OTHER STYLES THAT MIGHT BE USEFUL ------------------------------------- */ .last { margin-bottom: 0; } .first { margin-top: 0; } .align-center { text-align: center; } .align-right { text-align: right; } .align-left { text-align: left; } .clear { clear: both; } .mt0 { margin-top: 0; } .mb0 { margin-bottom: 0; } .preheader { color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0; } .powered-by a { text-decoration: none; font-size: 14px; } hr { border: 0; border-bottom: 1px solid #f6f6f6; margin: 20px 0; } /* ------------------------------------- RESPONSIVE AND MOBILE FRIENDLY STYLES ------------------------------------- */ @media only screen and (max-width: 620px) { table[class=body] h1 { font-size: 28px !important; margin-bottom: 10px !important; } table[class=body] p, table[class=body] ul, table[class=body] ol, table[class=body] td, table[class=body] span, table[class=body] a { font-size: 16px !important; } table[class=body] .wrapper, table[class=body] .article { padding: 10px !important; } table[class=body] .content { padding: 0 !important; } table[class=body] .container { padding: 0 !important; width: 100% !important; } table[class=body] .main { border-left-width: 0 !important; border-radius: 0 !important; border-right-width: 0 !important; } table[class=body] .btn table { width: 100% !important; } table[class=body] .btn a { width: 100% !important; } table[class=body] .img-responsive { height: auto !important; max-width: 100% !important; width: auto !important; } } /* ------------------------------------- PRESERVE THESE STYLES IN THE HEAD ------------------------------------- */ @media all { .ExternalClass { width: 100%; } .ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div { line-height: 100%; } .apple-link a { color: inherit !important; font-family: inherit !important; font-size: inherit !important; font-weight: inherit !important; line-height: inherit !important; text-decoration: none !important; } #MessageViewBody a { color: inherit; text-decoration: none; font-size: inherit; font-family: inherit; font-weight: inherit; line-height: inherit; } .btn-primary table td:hover { background-color: #34495e !important; } .btn-primary a:hover { background-color: #34495e !important; border-color: #34495e !important; } } </style> </head> <body class=""> <!-- <span class="preheader">This is preheader text. Some clients will show this text as a preview.</span> --> <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body"> <tr> <td>&nbsp;</td> <td class="container"> <div class="content"> <!-- START CENTERED WHITE CONTAINER --> <table role="presentation" class="main"> <!-- START MAIN CONTENT AREA --> <tr> <td class="wrapper"> <table role="presentation" border="0" cellpadding="0" cellspacing="0"> <tr> <td><p>Hi there, <br>there are some new updates.</p>'
    html_frame_lower = '<p>From NYSCEC.</p></td> </tr> </table> </td> </tr> <!-- END MAIN CONTENT AREA --> </table> <!-- END CENTERED WHITE CONTAINER --> <!-- START FOOTER --> <div class="footer"> <table role="presentation" border="0" cellpadding="0" cellspacing="0"> <tr> <td class="content-block"> <span class="apple-link">You are receiving this letter due to the agreement of subscription.</span><br> Send your information to <u><a href="mailto:">your_mail</a></u> to unsubscribe. </td> </tr> <tr> <td class="content-block powered-by"> Provided by <u><a href="">acoustikue</a></u> (SukJoon Oh). </td> </tr> </table> </div> <!-- END FOOTER --> </div> </td> <td>&nbsp;</td> </tr> </table> </body></html>'
    
    msg.attach(MIMEText(content, 'plain'))
    msg.attach(MIMEText(html_frame_upper + generate_content_2(updates) + html_frame_lower, 'html'))
    
    smtp_server = smtplib.SMTP_SSL(NYSCEC_SMTP_SERVER, NYSCEC_SMTP_PORT)
    smtp_server.login(NYSCEC_ADMIN_ID, NYSCEC_ADMIN_PW)

    smtp_server.sendmail(msg['From'], msg["To"].split(","), msg.as_string())

    del html_frame_upper
    del html_frame_lower



# 
# script
if __name__ == "__main__":
    pass

    
    
    
    
    
    
    

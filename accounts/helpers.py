
# from django.core.mail import send_mail

# from django.conf import settings 
import http.client

# def send_forget_password_mail(email , token ):
#     subject = 'Your forget password link'
#     message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/change-password/{token}/'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message, email_from, recipient_list)
#     return True

def send_forget_password_mail(email , token):
    email =email
    token = token

    print(email , token)
    conn = http.client.HTTPSConnection("api.msg91.com")
    payload = "{\n  \"to\": [\n{\n\"name\":\"mathewsoninfotech\",\n\"email\":   \""+email+"\" \n }\n  ],\n  \"from\": {\n\"name\":\"Mathewsoninfotech\",\n    \"email\": \"thajudheen@mathewsoninfotech.com\" },\n  \"domain\": \"mstestndemo.mathewsoninfotech.com\", \r\n\"mail_type_id\": \"1\",				\r\n\"template_id\":			\"MST-DIGITAL\",\n  \"variables\": {\n    \"VAR1\": \"'Hi , click on the link to reset your password http://demorcmst.reelcats.com/change-password/"+token+"/'\" ,\"VAR2\": \""+email+"\" ,\"VAR3\": \""+token+"\" ,\"VAR4\": \"hello\" ,\n    	\"VAR5\":\"hi\"  },\n  \"authkey\": \"375863AOJUpBOm52625d40baP1\"\n}"
#    payload = "{\n  \"to\": [\n{\n\"name\": "+ name1 +",\n\"email\": \"thajudheenac12@gmail.com\"\n }\n  ],\n  \"from\": {\n\"name\": \"mathewsoninfotech\",\n    \"email\": \"thajudheen@mathewsoninfotech.com\"\n  },\n  \"domain\": \"mstestndemo.mathewsoninfotech.com\", \r\n\"mail_type_id\": \"1\",        \r\n\"template_id\":        \"mathewsoninfotech_thank_you\",\n  \"variables\": {\n    \"VAR1\": \"'name'\" ,\n      \"VAR2\":\"'ms infotech'\"  },\n  \"authkey\": \"375863AOJUpBOm52625d40baP1\"\n}"

    print(payload)

    headers = {
        'Content-Type': "application/JSON",
        'Accept': "application/json"
        }

    conn.request("POST","/api/v5/email/send",payload,headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    return True

def subscriber_send_forget_password_mail(email , token):
    email =email
    token = token

    print(email , token)
    conn = http.client.HTTPSConnection("api.msg91.com")
    payload = "{\n  \"to\": [\n{\n\"name\":\"mathewsoninfotech\",\n\"email\":   \""+email+"\" \n }\n  ],\n  \"from\": {\n\"name\":\"Mathewsoninfotech\",\n    \"email\": \"thajudheen@mathewsoninfotech.com\" },\n  \"domain\": \"mstestndemo.mathewsoninfotech.com\", \r\n\"mail_type_id\": \"1\",				\r\n\"template_id\":			\"MST-DIGITAL\",\n  \"variables\": {\n    \"VAR1\": \"'Hi , click on the link to reset your password http://demorcmst.reelcats.com/Subscriber_ChangePassword/"+token+"/'\" ,\"VAR2\": \""+email+"\" ,\"VAR3\": \""+token+"\" ,\"VAR4\": \"hello\" ,\n    	\"VAR5\":\"hi\"  },\n  \"authkey\": \"375863AOJUpBOm52625d40baP1\"\n}"
#    payload = "{\n  \"to\": [\n{\n\"name\": "+ name1 +",\n\"email\": \"thajudheenac12@gmail.com\"\n }\n  ],\n  \"from\": {\n\"name\": \"mathewsoninfotech\",\n    \"email\": \"thajudheen@mathewsoninfotech.com\"\n  },\n  \"domain\": \"mstestndemo.mathewsoninfotech.com\", \r\n\"mail_type_id\": \"1\",        \r\n\"template_id\":        \"mathewsoninfotech_thank_you\",\n  \"variables\": {\n    \"VAR1\": \"'name'\" ,\n      \"VAR2\":\"'ms infotech'\"  },\n  \"authkey\": \"375863AOJUpBOm52625d40baP1\"\n}"

    print(payload)

    headers = {
        'Content-Type': "application/JSON",
        'Accept': "application/json"
        }

    conn.request("POST","/api/v5/email/send",payload,headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    return True
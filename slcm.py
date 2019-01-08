import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, context
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_game():
    #print("uid - ",context.System.user.userId)
    welcome_msg = "Ask me about your attendance or grades in any semester."
    return question(welcome_msg)

@ask.intent("grades_intent", convert={'semester': str})
def grades(semester):
    print("semester - "+semester)
    semester = convert(semester)
    if semester == None:
        return question("You have asked for an invalid semester, please try again.")
    token = context.System.user.accessToken.split("*")
    regno = token[1]
    password = token[0]
    s = requests.Session()
    s.post("https://slcm.manipal.edu/loginForm.aspx", data={'__VIEWSTATE': '/wEPDwULLTE4NTA1MzM2ODIPZBYCAgMPZBYCAgMPZBYCZg9kFgICAw8PFgIeB1Zpc2libGVoZGRkZQeElbA4UBZ/sIRqcKZDYpcgTP0=', '__VIEWSTATEGENERATOR': '6ED0046F', '__EVENTVALIDATION': '/wEdAAbdzkkY3m2QukSc6Qo1ZHjQdR78oILfrSzgm87C/a1IYZxpWckI3qdmfEJVCu2f5cEJlsYldsTO6iyyyy0NDvcAop4oRunf14dz2Zt2+QKDEIHFert2MhVDDgiZPfTqiMme8dYSy24aMNCGMYN2F8ckIbO3nw==', 'txtUserid': regno, 'txtpassword':password, 'btnLogin': 'Sign in'})
    page1 = s.post("https://slcm.manipal.edu/GradeSheet.aspx", data={'__VIEWSTATE': '/wEPDwUJOTEyNjE4NjM1D2QWAmYPDxYCHghmaWxlbmFtZWVkFgQCAw8WAh4FY2xhc3MFEndyYXBwZXJfZ2Jfc3R1ZGVudGQCBQ8WAh4HZW5jdHlwZQUTbXVsdGlwYXJ0L2Zvcm0tZGF0YRYUAgcPFgIeC18hSXRlbUNvdW50ZmQCCw8PFgIeBFRleHQFD1NIT1VSWUEgSkFJU1dBTGRkAg0PFgIfAwIFFgpmD2QWBGYPFQMDbGk1CnRhYi0xIHRhYnMTU3R1ZGVudFByb2ZpbGUuYXNweGQCAw8PFgQfBAURQWRtaXNzaW9uIFByb2ZpbGUeD0NvbW1hbmRBcmd1bWVudAUBNRYCHhNkYXRhLW9yaWdpbmFsLXRpdGxlBRFBZG1pc3Npb24gUHJvZmlsZWQCAQ9kFgRmDxUDBWxpMTE5CnRhYi0yIHRhYnMOQWNhZGVtaWNzLmFzcHhkAgMPDxYEHwQFEEFjYWRlbWljcyBEZXRhaWwfBQUDMTE5FgIfBgUQQWNhZGVtaWNzIERldGFpbGQCAg9kFgRmDxUDBGxpMzkKdGFiLTMgdGFicxJGZWVEZXRhaWxzTUlULmFzcHhkAgMPDxYEHwQFCkZpbmFuY2lhbHMfBQUCMzkWAh8GBQpGaW5hbmNpYWxzZAIDD2QWBGYPFQMEbGkyNwp0YWItNCB0YWJzASNkAgMPDxYEHwQFC0FwcGxpY2F0aW9uHwUFAjI3FgIfBgULQXBwbGljYXRpb25kAgQPZBYEZg8VAwRsaTU2CnRhYi01IHRhYnMBI2QCAw8PFgQfBAUSQXBwbGljYXRpb24gU3RhdHVzHwUFAjU2FgIfBgUSQXBwbGljYXRpb24gU3RhdHVzZAIPDxYCHgVzdHlsZQUOZGlzcGxheTpibG9jazsWAgIBDxYCHwMCBBYIZg9kFgQCAg8VAQVsaTEyMGQCAw8PFgQfBAUTSW1wb3J0YW50IERvY3VtZW50cx8FBQMxMjBkZAIBD2QWBAICDxUBBGxpNTNkAgMPDxYEHwQFElVwbG9hZGVkIERvY3VtZW50cx8FBQI1M2RkAgIPZBYEAgIPFQEEbGk3M2QCAw8PFgQfBAUORXZlbnQgQ2FsZW5kYXIfBQUCNzNkZAIDD2QWBAICDxUBBGxpODBkAgMPDxYEHwQFCEZlZWRCYWNrHwUFAjgwZGQCEQ8W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HwQFCElDVCAzMjYzZGQCAg9kFgICAQ8PFgIfBAUiTU9CSUxFIEFQUExJQ0FUSU9OIERFVkVMT1BNRU5UIExBQmRkAgMPZBYCAgEPDxYCHwRlZGQCBA9kFgICAQ8PFgIfBAUEMS4wMGRkAgUPZBYCAgEPDxYCHwUFCElDVCAzMjYzZGQCBw9kFgxmDw8WAh8EBQE3ZGQCAQ9kFgICAQ8PFgIfBAUITU1FIDMyODhkZAICD2QWAgIBDw8WAh8EBTNPUEVOIEVMRUNUSVZFIC0gSU5UUk9EVUNUSU9OIFRPIE9QRVJBVElPTlMgUkVTRUFSQ0hkZAIDD2QWAgIBDw8WAh8EZWRkAgQPZBYCAgEPDxYCHwQFBDMuMDBkZAIFD2QWAgIBDw8WAh8FBQhNTUUgMzI4OGRkAggPZBYMZg8PFgIfBAUBOGRkAgEPZBYCAgEPDxYCHwQFCENSQSA0MDA1ZGQCAg9kFgICAQ8PFgIfBAUhQklHIERBVEEgTU9ERUxMSU5HIEFORCBNQU5BR0VNRU5UZGQCAw9kFgICAQ8PFgIfBGVkZAIED2QWAgIBDw8WAh8EBQQzLjAwZGQCBQ9kFgICAQ8PFgIfBQUIQ1JBIDQwMDVkZAIJD2QWDGYPDxYCHwQFATlkZAIBD2QWAgIBDw8WAh8EBQhDUkEgNDAwNmRkAgIPZBYCAgEPDxYCHwQFI0JJRyBEQVRBIElOVEVHUkFUSU9OIEFORCBQUk9DRVNTSU5HZGQCAw9kFgICAQ8PFgIfBGVkZAIED2QWAgIBDw8WAh8EBQQzLjAwZGQCBQ9kFgICAQ8PFgIfBQUIQ1JBIDQwMDZkZAIKDw8WAh8IaGRkAhkPPCsAEQEMFCsAAGQYAwUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgYFK2N0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkcmFkaW9SZXZhbHVhdGlvbjEFK2N0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkcmFkaW9SZXZhbHVhdGlvbjEFJWN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkcmFkaW9NYWtlVVAFJWN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkcmFkaW9NYWtlVVAFK2N0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkcmFkaW9SZXZhbHVhdGlvbjIFK2N0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkcmFkaW9SZXZhbHVhdGlvbjIFKWN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkZ3J2R3JhZGVoaXN0b3J5D2dkBSdjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJGdydkdyYWRlU2hlZXQPPCsADAEIAgFkMJvtkQd2pniYdfJdGPAddYnTDk0=', '__VIEWSTATEGENERATOR': '47C4ACAC', '__EVENTVALIDATION': '/wEdAFKAz7hjZ41Iazuq1ZtHKrJ74scyquAGPWYxRC7AQqFe8kFS39u1uTaXWkiDzZax6zz2X1hra3NJ6193wdN/kGkOuQj35VuJlLYB+3MRQV31TndO3WifGEymedEpSvq+lrfdTDPKdpmCyNirXLp8qM8JXgSAHShyvA4nQip4ejYShnNgXbvcdh85b4KQMkeh06AszOq5RNfwcp9s+LKXSVEpf0POqZnCl08QonsMiDjeHHA/GvbGsMoGRSCIMWDhb2L1Or/rnQE7YpA0CbraUm1YvqsVXookrxCvLpZ4dYqAP+iGHhKo2e+YuxX7gQaaPW9a6YVOyGG3+HXcYlaVQcBbbKt+Gtctj10JekqNpm4F3IyEUr6cgUlf0pWRWfNxBE+eMqVJyUMjV9jE+FGjaYt05gukbjL0xZvsiaOA2pnDMtOJcs3yHzNw0VW7xO7VXwd9NFF9H0waYPEbRe/wPe3AifMzWDJy/l0Lda8FgXt6UzIBI3tvipCHlgce4INkTyljub+74p5cCirueEt0tx45EBzc/jGi/dBfvp/vDaJYXiRMw25lN5WJyQgt/zkg5YhJTjvxW/n76h1mFOv2GnCVl/3EyYtWMOHDXvh8k91DmN8WE2++4fdtwLEKb9itCx+G7QJFJM5ywKlPVwU6eBYe39nllV4H1nHNI0kf7llW5wpMEnR+BvFjyOxd75X7kJ5RTyYXRRdVtuIDiMcYuU37L50vp94dEmBFvV/nYLJiyNqru0vb3BGSqE6DOvG4X3+mkZ+27PZ4hoL0QRoFSp37dyBxOWWXrXGA83VQFrZ8OoZsv7QDKrZ/4CKZ+aBG2tCk5M8YWnNk4XvTW/Jq4vCas5P6Ogo4c7YVAIIXV+irgmkFjjcrkB14qSn/e96oShoJ7n7QjxhPb2/TnqRgnVevxwTM5fHN9NWAjNDV1o0C99jHAKnGdjctumOE7TPWZciA+wuXYJ7IWmy1djXS1OcHXg5hggEzAphOesdIYvVE6V2Zwqa6cF5c8lixuxb9SRKbmb6hjIrB0klOzZnH5NFMTI0eVHA1ON2ytfkNxVSeEGdXqIUPy/ClO98i4pDPsu2OR23qxwy91unCMG5r5ekSC76WwUoPDJWwBIph2DlkyjfijU83psZ2dj05z3RCPPTCXM7Ezeqq2aILOIdX53qzipXI2T1lnc4ObdtL5pZl5VRN2VQS+b91dA4Ff4BU2ia7d87Ayzv8hL1K4BNetYCIWQaAjlYG8TZxl9YVvj3DABGIGAy9Jnw7bCyg8q5t2wbM1ily2J7r8mzHE1xG9QoPvq92osnfqHU+uoHEcdJon/CbcOOWzq06jaFt4D1HRfEk8MLSOT6PgPaHLyaC4Jx3ACW9+4NNBQFqEggRzU+xVaReTghYt8O7gED5JMxYioT1AZFB+oylwXRK8gQNpaCUclXkZKmRiKN003n6qh4Jg54h0Xad2lIFbziye0Rmh/xuvfWYJUO5z7MqsUR4KA1Dn3oDWyw/jOWV91A2Kojyls4ywTNY1t5I37CRlkRFCjRDzJeMXqT2I4ErfjmHkadBQMwy9aPxy7MlwS0wBMUd7YDP7+BsQY4FjK9psE9o1IGilC5JMeMKkUbyq/BStZj9HF9FWu6z9kcZ8tU3qB6nkQ6xEfTSlA/28XG8u6Vpem0FratDcmLPI4yVFlF+h7PexJcdhTTKOKm2vn8K3uJnSmW3o7x/x4+eOTlccklWcbBByNv+cbujG8Z8lAVoANb1qCktCRoTfjKXZYiv0kXkrCcGezY=', 'ctl00$ContentPlaceHolder1$ddlSemester': semester})
    soup = BeautifulSoup(page1.content, 'html.parser')
    subject = []
    grade = []
    for j in range(10):
        a = soup.find("span", id ='ContentPlaceHolder1_grvGradeSheet_lblSubject_'+str(j))
        b = soup.find("span", id ='ContentPlaceHolder1_grvGradeSheet_lblGrade_'+str(j))
        if(a == None):
            break
        subject.append(a.text.replace("- I","1"))
        grade.append(b.text)

    reply = " "
    f = 0
    for i in range(len(subject)):
        f = 1
        reply += "Your grade in "+subject[i]+" is "+grade[i]+", "
    if f==0:
        return question("You have asked for an invalid semester, please try again.")
    reply+= " Do you want to know anything else?"
    return question(reply)

@ask.intent("attendance_intent")
def attendance():
    token = context.System.user.accessToken.split("*")
    regno = token[1]
    password = token[0]
    s = requests.Session()
    s.post("https://slcm.manipal.edu/loginForm.aspx", data={'__VIEWSTATE': '/wEPDwULLTE4NTA1MzM2ODIPZBYCAgMPZBYCAgMPZBYCZg9kFgICAw8PFgIeB1Zpc2libGVoZGRkZQeElbA4UBZ/sIRqcKZDYpcgTP0=', '__VIEWSTATEGENERATOR': '6ED0046F', '__EVENTVALIDATION': '/wEdAAbdzkkY3m2QukSc6Qo1ZHjQdR78oILfrSzgm87C/a1IYZxpWckI3qdmfEJVCu2f5cEJlsYldsTO6iyyyy0NDvcAop4oRunf14dz2Zt2+QKDEIHFert2MhVDDgiZPfTqiMme8dYSy24aMNCGMYN2F8ckIbO3nw==', 'txtUserid': regno, 'txtpassword':password, 'btnLogin': 'Sign in'})
    page2 = s.post("https://slcm.manipal.edu/Academics.aspx")
    s = BeautifulSoup(page2.content, 'html.parser')
    table = s.find('table',{'class':'table table-bordered'}, id = "tblAttendancePercentage")
    rows = table.find_all('tr')
    data = [[td.findChildren(text=True) for td in tr.find_all("td")] for tr in rows]
    reply = " "
    for i in range(1,len(data)):
        reply += "Your attendance in "+str(data[i][1][0])+" is "+str(data[i][7][0])+"%, "
    reply+= " Do you want to know anything else?"
    return question(reply)

@ask.intent("yes_intent")
def yes():
    welcome_msg = "What's your question?"
    return question(welcome_msg)

@ask.intent("AMAZON.FallbackIntent")
def fallback():
    return question("I am not sure what you mean. Do you want to try again?").reprompt("Knock knock, you there ?") 

@ask.intent("AMAZON.StopIntent")
def stop():
    print("Stop")
    return statement("Okay. Goodbye") 

@ask.intent("AMAZON.CancelIntent")
def cancel():
    print("Cancel")
    return statement("Okay. Goodbye") 

@ask.intent("AMAZON.HelpIntent")
def help():
    msg = "I can answer your queries relating to your attendance and grades. So ask me your questions."
    return question(msg) 

def convert(num):
    if num=='1st' or num=='first':
        return 'I'
    if num=='2nd' or num=='second':
        return 'II'
    if num=='3rd' or num=='third':
        return 'III'
    if num=='4th' or num=='fourth':
        return 'IV'
    if num=='5th' or num=='fifth':
        return 'V'
    if num=='6th' or num=='sixth':
        return 'VI'
    if num=='7th' or num=='seventh':
        return 'VII'
    if num=='8th' or num=='eighth':
        return 'VIII'
    return None

if __name__ == '__main__':
    app.run(debug=True)

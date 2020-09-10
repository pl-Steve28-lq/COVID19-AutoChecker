import requests, json, Finder

class COVIDcheck:
    def __init__(self, name, birth, schoolID, region):
        school = Finder.schoolFinder(schoolID, region)
        try: self.url = {"서울": "https://senhcs.eduro.go.kr/",
"경기": "https://goehcs.eduro.go.kr/",
"대전": "https://djehcs.eduro.go.kr/",
"대구": "https://dgehcs.eduro.go.kr/",
"부산": "https://penhcs.eduro.go.kr/",
"인천": "https://icehcs.eduro.go.kr/",
"광주": "https://genhcs.eduro.go.kr/",
"울산": "https://usehcs.eduro.go.kr/",
"세종": "https://sjehcs.eduro.go.kr/",
"충북": "https://cbehcs.eduro.go.kr/",
"충남": "https://cnehcs.eduro.go.kr/",
"경북": "https://gbehcs.eduro.go.kr/",
"경남": "https://gnehcs.eduro.go.kr/",
"강원": "https://kwehcs.eduro.go.kr/",
"전북": "https://jbehcs.eduro.go.kr/",
"전남": "https://jnehcs.eduro.go.kr/",
"제주": "https://jjehcs.eduro.go.kr/"}[region]
        except: print("지역명을 올바르게 입력해주세요 : [서울, 경기, 대전, 대구, 부산, 인천, 광주, 울산, 세종, 충북, 충남, 경북, 경남, 강원, 전북, 전남, 제주]"); return None
        if not school: print("학교명을 올바르게 입력해주세요 : 학교 이름이 중첩 될 수 있습니다.\nex) 가림초등학교 => 인천가림초등학교 와 같이 바꾸어 실행하시기 바랍니다."); return None
        self.school = school
        self.info = self.encrypt(name,birth)
        self.subURL = ['loginwithschool', 'checkpw', 'secondlogin', 'selectGroupList', 'userrefresh', 'registerServey']

    def encrypt(self,name,birth):
        url = "http://hw3235.herokuapp.com/"
        result = json.loads(requests.get(url, params={"pName":name,"frnoRidno":birth}).text)
        return result if type(name)==type(birth)==str else None

    def login(self):
        return self.doLogin(self.subURL[0])

    def submit(self, token):
        return self.doSubmit(self.subURL[5], token)

    def doLogin(self, url):
        headers = {'Content-Type': 'application/json'}
        data = {"orgcode":self.school, "name":self.info["pName"], "birthday":self.info["frnoRidno"]}
        result = requests.post(self.url + url, headers=headers, data=json.dumps(data))
        return json.loads(result.text)["token"]

    def doSubmit(self, url, token):
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        data = {'rspns01': '1', 'rspns02': '1', 'rspns07': '0', 'rspns08': '0', 'rspns09': '0', 'rspns00': 'Y', 'deviceuuid': ''}
        result = requests.post(self.url + url, headers = headers, data=json.dumps(data)).text
        return result

    def check(self):
        a = None
        b = None
        try: a = self.submit(self.login())
        except Exception as ex: b = "값이 잘못 설정되었습니다" if str(ex)=="token" else "오류가 발생하였습니다"
        if a and not b: print("성공! : {}".format(json.loads(a)["registerDtm"])); return True
        else: print("에러! : {}".format(b))

with open("./Info.txt", encoding="UTF-8") as c:
    a = json.loads(''.join(c.readlines()))
    COVIDcheck(a["name"], a["birth"], a["school"], a["region"]).check()

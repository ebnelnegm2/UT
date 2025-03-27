import os
while True:
    try:
        import re
        import random
        import string
        from base64 import b64decode
        import requests
        import sys
        import time
        from datetime import datetime
        from requests import get
        from base64 import b64decode
        from time import sleep
        from random import choice, randint
        from fake_useragent import UserAgent
        from telethon import TelegramClient, sync, errors, types, functions
        from telethon.tl.functions.account import CheckUsernameRequest, UpdateUsernameRequest
        from telethon.tl.functions.channels import JoinChannelRequest
        break
    except ImportError as e:
        os.system(f'pip install {e.name}')
        # os.system('cls' if os.name == 'nt' else 'clear')
        continue

class ChackUserName:
    def __init__(self, ses):
        self.Client = ses
        self.names = set()
        self.generate_username()
        
    def user_gen(self, pattern):
        # الأنماط الجديدة المطلوبة
        new_patterns = [
            "[A-Z]_[A-Z]_[0-9]",       # مثل T_G_1
            "[A-Z]_[A-Z]_[A-Z]",       # مثل T_G_A
            "[A-Z]_[0-9]_[A-Z]",  # مثل A_B_1
            #"[A-Z][A-Z]_[0-9]",    # مثل AB_1
            #"[A-Z]_[A-Z][0-9]",    # مثل A_B1
            #"[A-Z][A-Z][0-9]",     # مثل AB1
        ]
        
        # اختيار عشوائي بين الأنماط القديمة والجديدة
        if random.choice([True, False]):  # 50% فرصة لاستخدام الأنماط الجديدة
            pattern = random.choice(new_patterns)
            
        fixed_digits = {}
        fixed_letters = {}
        result = []
        repeat_pattern = re.compile(r'(\w|\#|\*)\[(\d+)\]')
        
        def process_char(char):
            if char == '0':
                return str(random.randint(0, 9))
            elif char in ['1', '2', '3']:
                if char not in fixed_digits:
                    fixed_digits[char] = str(random.randint(0, 9))
                return fixed_digits[char]
            elif char == 'a':
                return random.choice(string.ascii_letters + string.digits)
            elif char == '#':
                if '#' not in fixed_letters:
                    fixed_letters['#'] = random.choice(string.ascii_letters)
                return fixed_letters['#']
            elif char == '*':
                if '*' not in fixed_letters:
                    fixed_letters['*'] = random.choice(string.ascii_letters)
                return fixed_letters['*']
            elif char == 'b':
                if 'b' not in fixed_letters:
                    fixed_letters['b'] = random.choice(string.ascii_letters)
                return fixed_letters['b']
            else:
                return char        
                
        i = 0
        while i < len(pattern):
            if pattern[i] == '[':
                # معالجة الأنماط الجديدة [A-Z] أو [0-9]
                close_bracket = pattern.index(']', i)
                options = pattern[i+1:close_bracket]
                if '-' in options:
                    start, end = options.split('-')
                    if start.isdigit() and end.isdigit():
                        result.append(str(random.randint(int(start), int(end))))
                    else:
                        result.append(chr(random.randint(ord(start), ord(end))))
                else:
                    result.append(random.choice(options))
                i = close_bracket + 1
            else:
                match = repeat_pattern.match(pattern, i)
                if match:
                    char = match.group(1)
                    repeat_count = int(match.group(2))
                    result.extend([process_char(char)] * repeat_count)
                    i += len(match.group(0))
                else:
                    result.append(process_char(pattern[i]))
                    i += 1
        return ''.join(result)
        
    def generate_username(self):
        numb = 0
        while True:
            user = self.user_gen(random.choice(["xxxx",
                #"aaaa",
                #"aaaa",
                #"qqqq",
                #"wwww",
                #"AaAA",
                #"ssss",
                #"saass",
                "#b##b",
                "#b#b#",
                "#b[3]#",
                "*b**b*",
                "#b[4]",
                "*b*b*b"
            ]))
            if user.lower() not in self.names:
                self.names.add(user.lower())
                try:
                    Fragment = self.Chack_UserName_Fragment(user)
                except:
                    self.names.discard(user)
                    continue
                numb += 1
                if Fragment == "taken":
                    print(f"-[{numb}] UserName is Taken [@{user}]")
                elif Fragment == "available":
                    print(f"-[{numb}] UserName is Sold [@{user}]")
                elif Fragment == "Unavailable":
                    print(f"-[{numb}] UserName is Unavailable [@{user}]")
                    self.Chack_UserName_TeleGram(user)
                elif Fragment == "unknown":
                    print(f"-[{numb}] UserName is unknown [@{user}]")
                    self.names.discard(user)
                else:
                    print(f"-[{numb}] Error is [{Fragment}]")

    def Chack_UserName_TeleGram(self, user):
        try:
            tele = self.Client(CheckUsernameRequest(username=user))
            if tele:
                print(f"- UserName is Good (CheckUsernameRequest) [{user}]")
                self.save_username_to_channel(user)
                Fragment = self.Chack_UserName_Fragment(user)
                if Fragment == "taken":
                    st_claim = True
                else:
                    st_claim = False
                text = f"• New UserName,Claim : {st_claim} .\n• UserName : @{user} ."
                self.Client.send_message('me', text)
                chack_flood = self.Chack_UserName_Flood(user)
                if chack_flood:
                    print(f"- UserName is Flood [@{user}]")
                    self.Client.send_message('me', f"- UserName is Flood [@{user}]")
            else:
                print(f"- UserName is Bad (CheckUsernameRequest) [{user}] Taken.")
        except errors.rpcbaseerrors.BadRequestError:
            print(f"- UserName is Band [@{user}]")
            return
        except errors.FloodWaitError as timer:
            num = int(timer.seconds)
            print(f"- Error Account Flood (CheckUsernameRequest) Time [{num}]\n- UserName [{user}]\n")
            while num > 0:
                print(f"The flood will end after: [{num}]", end="\r")
                time.sleep(1)
                num -= 1
            self.names.discard(user)
            return
        except errors.UsernameInvalidError:
            print(f"- UserName is Invalid [@{user}]")
            return
        
    def Chack_UserName_Flood(self, user):
        all_chat = self.Client.get_dialogs()
        for chat in all_chat:
            if chat.name == f"CLAIM-[{user}]" and not chat.entity.username:
                self.Client(functions.channels.DeleteChannelRequest(channel=chat.entity))
                return True
        return False
                
    def save_username_to_channel(self, user):
        r = self.Client(functions.channels.CreateChannelRequest(
            title=f"CLAIM-[{user}]",
            about=f"""\nMe • @ebn_elnegm\nDATA CLAIM • {datetime.now().strftime("%H:%M:%S")}\n""",
            megagroup=False
        ))
        try:
            self.Client(functions.channels.UpdateUsernameRequest(channel=r.chats[0], username=user))
            messages = self.Client.get_messages(user, limit=1)
            if messages:
                self.Client.delete_messages(user, messages[0].id)
            video_message_id = random.choice([7,8,9,10,11,12,13,14,15,16,36,18,19,20,21,22,23,24,25,28,37,38,39,40,41,42,43,44,45,46,50,51,52,53,54,55,56,57,58,59,60,61,62])
            video_message = self.Client.get_messages('DCKKKK', ids=video_message_id)
            if video_message and video_message.media:
                video_path = self.Client.download_media(video_message.media, file='VideoStar.mp4')
                time.sleep(1.5)
            bio_list = [
                "تحَبون بَس مو من صدگ هَنيالكُم .",
                "بعَدني شمآ عثر بية الزمن اقوة ..",
                "مُعزتنة وكضت چا بعد شَمتانين؟",
                "بيها گلشي الدنيّا بَـس مابيها منك .",
                ": صرت اخاف على مزاجي اكثر من مستقبلي. ",
                "نِستحي نِسولف بِغيرك وَ انتَ كِلهُم .",
                "أودُ تَقْبيلُ كُلَّ رِمْشٍ فِيّ عَينْاهُ .",
                "وكُلّ نُجُومُ السَمَاءِ أنتِ .",
                "‏فضلنا نخبي الحزن جوانا لحد ما ملامحنا إنطفت .",
                "المكتفي بنفسه ، ما يهمه من راح ومن بقى .",
                "‏ - عِيناك خمرٌ مباح \n- ولكن خِـمرك لغِيري مُحرّم . ‏",
                "قلبها طفل وعقلها رجل وجسدها انثى تلك هي اصعب النساء",
                "تركت چم ناس تندلني واجيت متيه لدربك..",
                "ليس وحيداً من يستمتع بصحبة نفسه."
            ]
            bio = random.choice(bio_list)
            self.Client.send_file(user, file='VideoStar.mp4', caption=(
                f'• Done Claim UserName • [@{user}] .\n'
                f'• Owner UserName : @ebn_elnegm .\n\n'
                f'• Bio • {bio}'
            ))
            self.Client.send_message(user, f' — Claim DataTime  - {datetime.now().strftime("%Y:%H:%M:%S")}')
            return
        except Exception as e:
            if "You're admin of too many public channels, make some channels private to change the username of this channel" in str(e):
                print(f"- Error (too many public channels) save_username_to_channel, UserName: [@{user}]\n Error : [{e}]")
                self.Client.send_message('me', f"- Error (too many public channels) save_username_to_channel, UserName: [@{user}]\n- Error : [{e}]")
                return
            elif "A wait" in str(e):
                time_flood = e.seconds
                print(f"- Error Account Flood (caused by UpdateUsernameRequest) Time [{time_flood}]\n- UserName [{user}]\n")
                while time_flood > 0:
                    print(f"The flood will end after: [{time_flood}]", end="\r")
                    time.sleep(1)
                    time_flood -= 1
                time.sleep(2.5)
                try:
                    self.Client(functions.channels.UpdateUsernameRequest(channel=r.chats[0], username=user))
                    return
                except Exception as e:
                    if "You're admin of too many public channels, make some channels private to change the username of this channel" in str(e):
                        print(f"- Error (too many public channels) save_username_to_channel, UserName: [@{user}]\n Error : [{e}]")
                        self.Client.send_message('me', f"- Error (too many public channels) save_username_to_channel, UserName: [@{user}]\n- Error : [{e}]")
                        return
                    else:
                        print(f"- Error save_username_to_channel, UserName: [@{user}]\n Error : [{e}]")
                    return
            else:
                print(f"- Error save_username_to_channel, UserName: [@{user}]\n Error : [{e}]")
                self.Client.send_message('me', f"- Error save_username_to_channel, UserName: [@{user}]\n- Error : [{e}]")
                return
                
    def Chack_UserName_Fragment(self, user):
        try:
            response = requests.get(f"https://fragment.com/username/{user}", timeout=15).text
            if '<span class="tm-section-header-status tm-status-taken">Taken</span>' in response:
                return "taken"
            elif '<span class="tm-section-header-status tm-status-unavail">Sold</span>' in response:
                return "available"
            elif '<div class="table-cell-status-thin thin-only tm-status-unavail">Unavailable</div>' in response:
                return "Unavailable"
            else:
                return "unknown"
        except Exception as e:
            return e
            
    @staticmethod
    def Get_Session():
        while True:
            phone = '+201068597388'  # Your phone number 
            #if phone == '':
                #phone = input("> Enter Phone Number Telegram :")
            client = TelegramClient("SG_Client", b64decode("MjUzMjQ1ODE=").decode(), b64decode("MDhmZWVlNWVlYjZmYzBmMzFkNWYyZDIzYmIyYzMxZDA=").decode())
            try:
                client.start(phone=phone)
            except:
                continue
            os.system('cls' if os.name == 'nt' else 'clear')
            return client

if __name__ == "__main__":
    Client = ChackUserName.Get_Session()
    ChackUserName(Client)
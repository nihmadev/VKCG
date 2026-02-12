import os
import sys
import time
import threading
import webbrowser
import browser_cookie3
import json
from datetime import datetime
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    WHITE = '\033[97m'

class Loader:
    def __init__(self):
        self.running = False
        self.thread = None
        self._stop_event = threading.Event()
        
    def _animate(self):
        chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        i = 0
        
        while not self._stop_event.is_set():
            progress = "█" * (i % 8) + "░" * (8 - (i % 8))
            sys.stdout.write(f'\r{Colors.CYAN}{chars[i % len(chars)]} Поиск куков VK... [{progress}]{Colors.ENDC}')
            sys.stdout.flush()
            if self._stop_event.wait(0.1):
                break
            i += 1
    
    def start(self):
        if not self.running:
            self.running = True
            self._stop_event.clear()
            self.thread = threading.Thread(target=self._animate)
            self.thread.daemon = True
            self.thread.start()
    
    def stop(self):
        if self.running:
            self.running = False
            self._stop_event.set()
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=1.0)
            sys.stdout.write('\r' + ' ' * 60 + '\r')
            sys.stdout.flush()

def show_ascii_art():
    art = f"""
{Colors.CYAN}
                                               
                   ,──.                        
               ,──╱  ╱│  ,────..    ,────..    
       ,───.,───,': ╱ ' ╱   ╱   ╲  ╱   ╱   ╲   
      ╱__.╱│:   : '╱ ╱ │   :     :│   :     :  
 ,───.;  ; ││   '   ,  .   │  ;. ╱.   │  ;. ╱  
╱___╱ ╲  │ │'   │  ╱   .   ; ╱──` .   ; ╱──`   
╲   ;  ╲ ' ││   ;  ;   ;   │ ;    ;   │ ;  __  
 ╲   ╲  ╲: │:   '   ╲  │   : │    │   : │.' .' 
  ;   ╲  ' .│   │    ' .   │ '___ .   │ '_.' : 
   ╲   ╲   ''   : │.  ╲'   ; : .'│'   ; : ╲  │ 
    ╲   `  ;│   │ '_╲.''   │ '╱  :'   │ '╱  .' 
     :   ╲ │'   : │    │   :    ╱ │   :    ╱   
      '───" ;   │,'     ╲   ╲ .'   ╲   ╲ .'    
            '───'        `───`      `───`      
"""
    print(art)

def close_all_browsers():
    print(f"{Colors.YELLOW}[!] Закрытие всех браузеров...{Colors.ENDC}")
    
    browsers_to_close = ['chrome', 'firefox', 'opera', 'edge', 'brave', 'yandex', 'safari', 'vivaldi', 'amigo']
    
    for browser in browsers_to_close:
        try:
            if sys.platform == "win32":
                os.system(f'taskkill /f /im {browser}.exe >nul 2>&1')
            elif sys.platform == "darwin":
                os.system(f'pkill -f "{browser}.app" > /dev/null 2>&1')
            else:
                os.system(f'pkill -f {browser} > /dev/null 2>&1')
        except:
            pass
    
    time.sleep(2)

def open_vk_and_wait():
    print(f"{Colors.BLUE}[+] Открытие VK.com...{Colors.ENDC}")
    
    try:
        webbrowser.open('https://vk.com')
        print(f"{Colors.GREEN}[+] Браузер открыт. Пожалуйста, войди в VK если нужно.{Colors.ENDC}")
        print(f"{Colors.YELLOW}[!] Ожидание 10 секунд для загрузки страницы...{Colors.ENDC}")
        time.sleep(10)
    except Exception as e:
        print(f"{Colors.RED}[!] Ошибка при открытии браузера: {e}{Colors.ENDC}")
        return False
    
    return True

def extract_cookies():
    loader = Loader()
    loader.start()
    
    all_vk_cookies = []
    browsers = ['chrome', 'firefox', 'opera', 'edge', 'brave', 'yandex', 'safari', 'vivaldi', 'amigo']
    found_messages = []
    
    try:
        for browser_name in browsers:
            try:
                if browser_name == 'chrome':
                    cookies = browser_cookie3.chrome(domain_name='vk.com')
                elif browser_name == 'firefox':
                    cookies = browser_cookie3.firefox(domain_name='vk.com')
                elif browser_name == 'opera':
                    cookies = browser_cookie3.opera(domain_name='vk.com')
                elif browser_name == 'edge':
                    cookies = browser_cookie3.edge(domain_name='vk.com')
                elif browser_name == 'brave':
                    cookies = browser_cookie3.brave(domain_name='vk.com')
                elif browser_name == 'yandex':
                    cookies = browser_cookie3.yandex(domain_name='vk.com')
                elif browser_name == 'safari':
                    cookies = browser_cookie3.safari(domain_name='vk.com')
                elif browser_name == 'vivaldi':
                    cookies = browser_cookie3.vivaldi(domain_name='vk.com')
                elif browser_name == 'amigo':
                    cookies = browser_cookie3.amigo(domain_name='vk.com')
                
                browser_cookies = list(cookies)
                if browser_cookies:
                    found_messages.append(f"{Colors.GREEN}[+] Найдено {len(browser_cookies)} куков в {browser_name}{Colors.ENDC}")
                    all_vk_cookies.extend(browser_cookies)
                    
            except:
                continue
    
    finally:
        loader.stop()
    
    for message in found_messages:
        print(message)
    
    return save_cookies(all_vk_cookies)

def save_cookies(cookies):
    if not cookies:
        print(f"{Colors.RED}[!] Куки VK не найдены{Colors.ENDC}")
        return None
    
    current_dir = Path(__file__).parent
    results_dir = current_dir / f"results_VK_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    results_dir.mkdir(exist_ok=True)
    
    cookie_file = results_dir / "Cookies.txt"
    
    json_file = results_dir / "Cookies.json"
    
    header_file = results_dir / "Cookies_Header.txt"
    
    cookie_list = []
    header_parts = []
    
    with open(cookie_file, 'w', encoding='utf-8') as f:
        
        for cookie in cookies:
            if hasattr(cookie, 'domain') and hasattr(cookie, 'name') and hasattr(cookie, 'value'):
                domain = cookie.domain or ''
                path = cookie.path or '/'
                secure = cookie.secure or False
                expiration = int(cookie.expires) if cookie.expires else 0
                name = cookie.name or ''
                value = cookie.value or ''
                f.write(f"{domain}\tTRUE\t{path}\t{str(secure).lower()}\t{expiration}\t{name}\t{value}\n")
                
                cookie_dict = {
                    'name': name,
                    'value': value,
                    'domain': domain,
                    'path': path,
                    'secure': secure,
                    'expires': expiration,
                    'httpOnly': getattr(cookie, 'httpOnly', False),
                    'sameSite': getattr(cookie, 'sameSite', None)
                }
                cookie_list.append(cookie_dict)
                
                header_parts.append(f"{name}={value}")
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(cookie_list, f, indent=4, ensure_ascii=False)
    
    header_string = "Cookie: " + "; ".join(header_parts)
    with open(header_file, 'w', encoding='utf-8') as f:
        f.write(header_string)
    
    print(f"{Colors.GREEN}[+] Успешно! Найдено {len(cookies)} куков VK{Colors.ENDC}")
    print(f"{Colors.CYAN}[+] Netscape формат: {cookie_file}{Colors.ENDC}")
    print(f"{Colors.CYAN}[+] JSON формат: {json_file}{Colors.ENDC}")
    print(f"{Colors.CYAN}[+] Header String формат: {header_file}{Colors.ENDC}")
    return len(cookies), cookie_file, json_file, header_file

def main():
    show_ascii_art()
    print(f"{Colors.YELLOW}[!] Этот скрипт закроет все браузеры и откроет VK.com{Colors.ENDC}")
    
    input(f"\n{Colors.BLUE}[?] Нажми Enter для продолжения...{Colors.ENDC}")
    close_all_browsers()
    if not open_vk_and_wait():
        input(f"\n{Colors.RED}[!] Нажми Enter для выхода...{Colors.ENDC}")
        return
    cookie_file = extract_cookies()
    
    input(f"\n{Colors.BLUE}[?] Нажми Enter для выхода...{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Программа прервана тобой{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}[!] Ошибка: {e}{Colors.ENDC}")
        input(f"{Colors.BLUE}[?] Нажмите Enter для выхода...{Colors.ENDC}")
        
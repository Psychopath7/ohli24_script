#coding:utf8
#title_en: Ohli24
#comment:https://a24.ohli24.com
#author: rickmiron, Psychopath7

from utils import Downloader,clean_title,LazyUrl
from m3u8_tools import M3u8_stream
import requests
from bs4 import BeautifulSoup
import re
import logging
from typing import List, Tuple, Optional

BASE_URL = 'https://a24.ohli24.com'
UAT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
HEADERS = {'User-Agent': UAT}

class Downloader_ohli24(Downloader):
    type = 'ohli24'
    URLS=['ohli24.com']
    display_name='Ohli24'
    MAX_PARALLEL=2
    MAX_CORE=2
    icon='base64:iVBORw0KGgoAAAANSUhEUgAAAEwAAABMCAMAAADwSaEZAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAB7FBMVEUAAABEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotJEotL///+I0xiUAAAAonRSTlMAAAMRBSZ34eN2JQhq0PzOaHrv7nliYMTBI/rz29b0+XTxGQkYh/bXGh3YzwYHHCIBb9zwsk9A6uYVsTWD/mYPhJogxUznexKj++RfPsqTJPU4oPJDEGTV3xcCPLqkK4BWVMflWLCXrURdbN7ibQsxOgRTy4iPVTu1pS7D2f1uFL/ti1sMKhZwOeyUIWXTMEbNLKngqy0TeKc9YXx+adFFJ3HSnOCkAAAAAWJLR0Sjx9rvGgAAAAd0SU1FB+QJBw8cNWped78AAAKISURBVFjD7dj5WxJBGAfwfZerWsEUKiWBAMsLiCKzMrrMY+0i0TIzOq0sKtEuM7P7sMvu+9q/tNmdATskdnnnt/j+BM8+z+fZ2Xnf2ZkVhFJKyRsA0YSMCMAss8Vqm4eKbf4Cs6aBVGZ3KMg4yhdKoFoVlVhKjdNFNFjExSLaYhAsS/hYilJVLVjd6o+lNR5Earyq4VsmaJbfFZCCRUeqXb5CVdyCdod19YAq1IZGjaFYUwiHhZt+w3A9FCphuUAostIULTw5ejAIr1odW9NceKp1YWtbyMV1rvUAHLAyn9YnG1oLDFUXtpEudHHPps2AxrZkV03/1m3/GqoxTHG0bQ8CL0xR2js6gRumeLtaRcBicls34zw78gxVP+bd2bwrTrXK3XvmnAf9WGIvVPckqSZX9c7VD4Yw6Nu3nw21v+MA4DABBg4OsslIHEr91Q/GMLIfCRxup1q88UgYUBj5Ix495qbc8RN/3JthjAzV0sOGOmRCYxA4KVPsVB8Sg4HTg2yYsWFAYaQ6zpxl1ZE+dx43AXChK0Yp39BIBlUaEB4dYx2VvNiALNrIJSdb1uyXg6h28l4ZucpKwj9+Ddno8sT1SWrZbkxhl6Bs5Ju9GfTiyHLrdj2vZXty7M5dXi+UxPi9KK9XXbf1Pv4l/EDbHsgTeZ+8Eexhmlx8NP2Yy8Yl8yTtezoscdlSkc3es+eRDJ/Nnu7wxWY4YuK0ukDZ+WDw4uWr/tdvuBx3BIi+TaXIjkvDPAEclg09Ilpriz4iSubZrn2nacmiD6915e9Hc5XI4Vjd8iGLwUcnFnN/ymFSBVaTP+ceGkhfvuI+kji/zdYChL7jPt/8MP9SWNgPSzqWlVL+8/wEmVmqzHr2JDEAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjAtMDktMDdUMTU6Mjg6NTMrMDI6MDA3vHR4AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIwLTA5LTA3VDE1OjI4OjUzKzAyOjAwRuHMxAAAAFd6VFh0UmF3IHByb2ZpbGUgdHlwZSBpcHRjAAB4nOPyDAhxVigoyk/LzEnlUgADIwsuYwsTIxNLkxQDEyBEgDTDZAMjs1Qgy9jUyMTMxBzEB8uASKBKLgDqFxF08kI1lQAAAABJRU5ErkJggg=='
    ACCEPT_COOKIES=[r'(.*\.)?(ohli24)\.(com)']
    
    def read(self):
        dix=['']
        self.single=True
        self.title,self.urls=process_urls([self.url],dix)
        dix[0]=self.dir

def is_list_url(url: str) -> bool:
    return "/c/" in url

def fetch_content(url: str, headers: dict) -> Optional[BeautifulSoup]:
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        logging.error(f"{url}에서 콘텐츠를 불러오는 중 오류 발생: {e}")
        raise

def extract_video_links(list_url: str) -> List[Tuple[str, str]]:
    soup = fetch_content(list_url, HEADERS)
    if not soup:
        return []

    links = [
        (a_tag.get_text(strip=True), BASE_URL + a_tag.find('a').get('href'))
        for a_tag in soup.find_all('div', class_='wr-subject')
        if a_tag.find('a') and a_tag.find('a').get('href')
    ]
    
    logging.info("영상 목록을 성공적으로 불러왔습니다.")
    return list(reversed(links))

def extract_video_id_and_title(url: str) -> Tuple[Optional[str], str]:
    soup = fetch_content(url, HEADERS)
    if not soup:
        return None, "default_video_name",None

    title_tag = soup.find('div', class_='view-title').find('h1')
    title = title_tag.get_text(strip=True) if title_tag else "default_video_name"

    iframe = soup.find('iframe')
    if iframe and iframe.get('src'):
        src = iframe.get('src')
        
        if 'index.php?data=' in src:
            video_id = src.split('index.php?data=')[-1]
        else:
            video_id = src.split('/')[-1]
        
        return video_id, title,soup
    else:
        logging.warning("iframe 태그 또는 src 속성을 찾을 수 없습니다.")
        return None, title,soup

def extract_domain(soup) -> Optional[str]:
    if not soup:
        return None

    iframe = soup.find('iframe')
    if iframe and iframe.get('src'):
        referer = '/'.join(iframe.get('src').split('/')[:3])
        return referer
    else:
        logging.warning("iframe 태그 또는 src 속성을 찾을 수 없습니다.")
        return None

def get_secured_video_link(video_id: str, referer: str) -> Optional[str]:
    """getVideo 엔드포인트에서 securedLink를 가져옵니다."""
    video_url = f"{referer}/player/index.php?data={video_id}&do=getVideo"
    headers = {**HEADERS, 'X-Requested-With': 'XMLHttpRequest', 'Referer': referer}
    
    try:
        response = requests.post(video_url, headers=headers)
        response.raise_for_status()
        
        # JSON 응답인지 확인하기 위해 예외 처리 추가
        try:
            data = response.json()
        except ValueError:
            # JSON 형식이 아닐 경우 본문 내용 로그 출력
            logging.error(f"JSON 응답이 아닙니다. 응답 본문: {response.text}")
            return None

        # securedLink 확인
        secured_link = data.get('securedLink')
        
        if secured_link:
            logging.info("고유 securedLink를 성공적으로 가져왔습니다.SL")
            return secured_link
        else:
            logging.warning("JSON 응답에서 'securedLink'를 찾을 수 없습니다.")
            return None
    except requests.exceptions.RequestException as e:
        logging.error("securedLink 가져오는 중 오류 발생:", exc_info=True)
        return None

def get_subtitle_url(video_id: str, referer: str) -> Optional[str]:
    video_url = f"{referer}/player/index.php?data={video_id}&do=getVideo"
    soup = fetch_content(video_url, {**HEADERS, 'Referer': referer})
    if not soup:
        return None
    subtitle_match = re.search(r'playerjsSubtitle\s*=\s*".*?(https://[^\s]+\.srt)', soup.prettify(), re.DOTALL)
    if subtitle_match:
        subtitle_url = subtitle_match.group(1)
        return subtitle_url
    return None

def download_subtitle(subtitle_url: str, output_filename: str) -> None:
    try:
        response = requests.get(subtitle_url, headers=HEADERS)
        response.raise_for_status()
        
        subtitle_filename = f"{output_filename}.srt"
        with open(subtitle_filename, "wb") as subtitle_file:
            subtitle_file.write(response.content)
    except requests.exceptions.RequestException as e:
        logging.error("자막 다운로드 요청 오류:", exc_info=True)

def download_single_video(video_url: str,dx) -> None:
    urls=[]
    video_id, title,soup = extract_video_id_and_title(video_url)
    title = clean_title(title)
    if not video_id:
        return

    referer = extract_domain(soup)
    if not referer:
        return

    secured_link = get_secured_video_link(video_id, referer)
    if not secured_link:
        return

    subtitle_url = get_subtitle_url(video_id, referer)
    #if subtitle_url:
    #    urls.append(subtitle_url)
    #    names[subtitle_url]=title+".srt"
        #download_subtitle(subtitle_url, title)
    res=requests.get(secured_link)
    urls.append(Video(res.text.split()[-1],title,subtitle_url,dx).url)
    return title,urls

def process_urls(urls: List[str],dx) -> None:

    list_urls = [url for url in urls if is_list_url(url)]
    single_urls = [url for url in urls if not is_list_url(url)]

    all_selected_videos = []
    for list_url in list_urls:
        video_links = extract_video_links(list_url)

        if video_links:
            lisx=[]
            for title, video_url in video_links:
                if all_selected_videos:
                    lisx.append(video_url.replace(' ','%20'))
                all_selected_videos.append((title, video_url))
            ui.edit.setText(', '.join(lisx))
            ui.downButton.click()
    for title, video_url in all_selected_videos:
        titlex,urlx=download_single_video(video_url,dx)
        break

    for single_url in single_urls:
        titlex,urlx=download_single_video(single_url,dx)
    return titlex,urlx#, not is_list_url(urls[0])

class Video:
    def __init__(self,url,name,sub,dx):
        self.dx=dx
        self.sub=sub
        self.filename=name+'.mp4'
        self.name=name
        m=M3u8_stream(url, n_thread=4)
        if getattr(m,'live',None) is not None:
            m=m.live
        self.url=LazyUrl(' ',lambda _: m,self,pp=self.pp)

    def pp(self,filename):
        if self.sub:
            download_subtitle(self.sub,self.dx[0]+'/'+self.name)
        return filename

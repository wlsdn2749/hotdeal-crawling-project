from datetime import datetime, timedelta
import json
import os
import re

DIR_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

def convert_to_datetime(input_str):
    try:
        # 시간 형식인지 확인하고 변환
        time_obj = datetime.strptime(input_str, '%H:%M').time()
        date_obj = datetime.now().date()  # 현재 날짜를 기본으로 사용
    except ValueError:
        try:
            # 날짜 형식인지 확인하고 변환
            date_obj = datetime.strptime(input_str, '%Y.%m.%d').date()
            time_obj = datetime.min.time()  # 최소 시간을 기본으로 사용
        except ValueError:
            try:
                # 시간 날짜 형식인지 확인하고 변환 
                date_time_obj = datetime.strptime(input_str, '%Y.%m.%d %H:%M').date()
                return date_time_obj.strftime('%Y-%m-%d %H:%M')
            except ValueError:
                date_obj = datetime.now().date()  # 현재 날짜를 기본으로 사용
                time_obj = datetime.min.time()  # 최소 시간을 기본으로 사용

    # datetime 객체를 원하는 형식으로 조합
    datetime_combined = datetime.combine(date_obj, time_obj)

    # 원하는 출력 형식으로 변환
    output_str = datetime_combined.strftime('%Y-%m-%d %H:%M')

    return output_str

def convert_to_datetime_detail(time_str: str) -> str:
    now = datetime.now()
    if "분전" in time_str or "minutes ago" in time_str:
        minutes = int(time_str.replace("분전", "").replace("minutes ago", "").strip())
        result_time = now - timedelta(minutes=minutes)
    elif "시간전" in time_str or "hours ago" in time_str:
        hours = int(time_str.replace("시간전", "").replace("hours ago", "").strip())
        result_time = now - timedelta(hours=hours)
        
    else:
        return time_str
    
    return result_time.strftime("%Y-%m-%d %H:%M")

class FmUtils:
    @staticmethod
    def adjust_time(dt_str):
        # 문자열을 datetime 객체로 변환 (포맷은 'YYYY-MM-DD HH:MM'로 가정)
        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
        
        # 현재 시간
        now = datetime.now()
        
        # 시간 비교를 위해 현재 날짜와 주어진 날짜의 시간을 사용
        # FM에서는 하루가 지나면, 즉 24hrs가 지나면 날짜로 표기되며 여기서는 00:00으로 처리되므로 아래는 동작하지 않음
        current_time = now.time()
        given_time = dt.time()
        
        # 주어진 시간이 현재 시간보다 더 크다면 하루를 빼줌
        if given_time > current_time:
            dt -= timedelta(days=1)
        
        # datetime 객체를 문자열로 변환
        adjusted_dt_str = dt.strftime('%Y-%m-%d %H:%M')
        return adjusted_dt_str
            
    
class ArcaUtils:
    @staticmethod
    def convert_iso_to_str(iso_string):
        # 문자열을 datetime 객체로 변환
        datetime_obj = datetime.strptime(iso_string, '%Y-%m-%dT%H:%M:%S.%fZ')
        
        # 원하는 형식으로 변환
        formatted_string = datetime_obj.strftime('%Y-%m-%d %H:%M')
        
        return formatted_string
    
    @staticmethod
    def convert_fromisoformat(date_string):
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))

class DataUtils:
    @staticmethod
    def find_root_dir(path):
        while True:
            parent = os.path.dirname(path)
            if parent == path:
                return path
            path = parent
        
    @staticmethod
    def get_site_category(site):
        with open(f"{DIR_PATH}/static/categories_{site}.json", 'r', encoding='utf-8') as f:
            return json.load(f)
        
    @staticmethod
    def remove_parentheses(content):
        if not isinstance(content, str):
            try:
                content = str(content)
            except:
                return "0"
        
            
        return content.replace("[", "").replace("]", "")
        
class QzUtils:
    
    @staticmethod
    def convert_timeformat(date):
        return datetime.strptime(date, '%Y.%m.%d %H:%M').strftime('%Y-%m-%d %H:%M')
    
    @staticmethod
    def extract_product_name(title):
        return re.sub(r'\[.*?\]', '', title).strip()
    
    
class RuliUtils:
    
    @staticmethod
    def convert_timeformat(date):
        return datetime.strptime(date, '%Y.%m.%d (%H:%M:%S)').strftime('%Y-%m-%d %H:%M')
    
    @staticmethod
    def extract_product_name(title):
        return re.sub(r'\[.*?\]', '', title).strip()
    
    @staticmethod
    def remove_whitespace_views(view):
        return view.replace("조회", "").replace("\t", "").strip()
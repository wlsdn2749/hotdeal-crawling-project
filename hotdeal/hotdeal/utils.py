from datetime import datetime

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
            date_obj = datetime.now().date()  # 현재 날짜를 기본으로 사용
            time_obj = datetime.min.time()  # 최소 시간을 기본으로 사용

    # datetime 객체를 원하는 형식으로 조합
    datetime_combined = datetime.combine(date_obj, time_obj)

    # 원하는 출력 형식으로 변환
    output_str = datetime_combined.strftime('%Y-%m-%d %H:%M')

    return output_str
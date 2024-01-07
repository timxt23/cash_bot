from datetime import datetime, timedelta


def get_dates():
    today = datetime.now().date()

    one_day_ago = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)

    date_list = [
        today.strftime('%d.%m.%Y'),
        one_day_ago.strftime('%d.%m.%Y'),
        two_days_ago.strftime('%d.%m.%Y')
    ]
    return date_list

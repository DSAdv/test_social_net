import datetime

from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from server.models import PostLikeModel

DATE_PATTERN = "%Y-%m-%d"

_date_parser = RequestParser()
_date_parser.add_argument(
    "date_from",
    type=str,
    required=True,
    help="Start date for statistics, this field cannot be blank"
)
_date_parser.add_argument(
    "date_to",
    type=str,
    required=True,
    help="End date for statistics, this field cannot be blank"
)


def make_date_range(start_date, end_date):
    days_len = int((end_date - start_date).days)
    return [(start_date + datetime.timedelta(n)).date() for n in range(days_len)]


class LikeAnalytics(Resource):
    def get(self):
        json_data = _date_parser.parse_args()
        start_date = datetime.datetime.strptime(json_data.get("date_from"), DATE_PATTERN)
        end_date = datetime.datetime.strptime(json_data.get("date_to"), DATE_PATTERN)
        return {
            "statistics": {
                str(date): PostLikeModel.get_day_count(date) for date in make_date_range(start_date, end_date)
            }
        }




if __name__ == '__main__':
    print(make_date_range(
        datetime.datetime.strptime("2020-06-01", DATE_PATTERN),
        datetime.datetime.strptime("2020-06-07", DATE_PATTERN)
    ))
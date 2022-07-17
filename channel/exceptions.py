from rest_framework.exceptions import APIException


class AlreadySusbcribed(APIException):
    status_code = 400
    default_detail = "You have already susbcribed this channel"
    default_code = "already_subscribed"


class NotSubscribed(APIException):
    status_code = 400
    default_detail = "You have not subscribed this channel"
    default_code = "not_subscribed"

from rest_framework.exceptions import APIException


class AlreadyRead(APIException):
    status_code = 400
    default_detail = "You already read this post"
    default_code = "already_read"


class NotReadYet(APIException):
    status_code = 400
    default_detail = "You have not read this post yet"
    default_code = "not_read_yet"


class AlreadyBookmarked(APIException):
    status_code = 400
    default_detail = "You have already bookmarked this post"
    default_code = "already_bookmarked"


class NotBookmarkedYet(APIException):
    status_code = 400
    default_detail = "You have not bookmarked this post yet"
    default_code = "not_bookmarked_yet"

from enum import Enum


class FormattedURLs(Enum):
    BASE_URL = 'https://www.digikala.com/ajax/product/comments/{}/?mode=newest_comment&page={}'


class ErrorMessages(Enum):
    INT_TYPE_ERROR = 'The value of max_product_id variable must be integer.'


class ConstantVariables(Enum):
    HTML_PARSER = 'html.parser'


class StatusCodes(Enum):
    OK_STATUS_CODE = 200
    NOT_FOUND_STATUS_CODE = 404


class Selectors(Enum):
    COMMENTS_CONTAINER = 'div.c-comments__container div.c-comments__content-section div#product-comment-list'
    COMMENT_ITEMS = "c-comments__item"
    COMMENT_TITLE = "c-comments__title"
    COMMENT_CONTENT = "c-comments__content"
    POSITIVE_COMMENTS = "c-comments__modal-evaluation-item--positive"
    NEGATIVE_COMMENTS = "c-comments__modal-evaluation-item--negative"
    # COMMENT_TITLES = 'div.comments__item div.c-comments__row span.c-comments__title'


class CommentObject(Enum):
    TITLE = 'title'
    CONTENT = 'content'
    POSITIVITIES = 'positivities'
    NEGATIVITIES = 'negativities'

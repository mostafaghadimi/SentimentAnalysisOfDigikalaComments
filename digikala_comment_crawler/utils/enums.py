from enum import Enum


class FormattedURLs(Enum):
    BASE_URL = 'https://www.digikala.com/ajax/product/comments/{}/?mode=newest_comment&page={}'
    DOMAIN_NAME = 'https://www.digikala.com{}'


class Messages(Enum):
    INT_TYPE_ERROR = 'The value of max_product_id variable must be integer.'
    PAGINATION_ERROR = 'This product doesn\'t have pagination.'
    NO_COMMENTS_ERROR = 'This product doesn\'t have any comments.'
    CRAWLER_INIT_INFO = 'Digikala Crawler instance have been created.'
    URL_CREATION_INFO = 'Generating URLs from product ID {} to {}'
    NOT_OK_STATUS_CODE = '{} status code has been occurred.'
    ADD_PAGINATION_INFO = 'The other comment pages of this product have been added'
    START_CRAWLING_URL_INFO = 'Start crawling and retrieving comments of {} URL.'
    SAVING_DATAFRAME_INFO = 'Saving data as {} in {} directory'


class ConstantVariables(Enum):
    HTML_PARSER = 'html.parser'
    URL_FORMATS = '/ajax/product/'


class StatusCodes(Enum):
    OK_STATUS_CODE = 200
    NOT_FOUND_STATUS_CODE = 404


class Selectors(Enum):
    COMMENT_PAGES = "c-pager__item"
    COMMENT_ITEMS = "c-comments__item"
    COMMENT_TITLE = "c-comments__title"
    COMMENT_CONTENT = "c-comments__content"
    COMMENT_HELPFULNESS_SCORE = "c-comments__helpful-yes"
    POSITIVE_COMMENTS = "c-comments__modal-evaluation-item--positive"
    NEGATIVE_COMMENTS = "c-comments__modal-evaluation-item--negative"
    COMMENTS_CONTAINER = 'div.c-comments__container div.c-comments__content-section div#product-comment-list'


class CommentObject(Enum):
    TITLE = 'title'
    CONTENT = 'content'
    POSITIVITIES = 'positivities'
    NEGATIVITIES = 'negativities'
    HELPFULNESS_SCORE = 'helpfulness score'

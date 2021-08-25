import requests
from bs4 import BeautifulSoup

from utils.enums import FormattedURLs, ErrorMessages, ConstantVariables, StatusCodes, CSSSelectors


def get_raw_urls(max_product_id):
    if not isinstance(max_product_id, int):
        raise ValueError(ErrorMessages.INT_TYPE_ERROR.value)
    urls = list()
    page_no = 1
    for product_id in range(3, max_product_id):
        urls.append(
            FormattedURLs.BASE_URL.value.format(product_id, page_no)
        )
    return urls


def get_text_of_comments(comment_detail, class_name):
    try:
        return comment_detail.find(class_=class_name).get_text()
    except AttributeError:
        return None


def crawl_web_page(to_be_crawled_urls, crawled_urls):
    for to_be_crawled_url in to_be_crawled_urls:
        if to_be_crawled_url not in crawled_urls:
            response = requests.get(to_be_crawled_url)
            if response.status_code == StatusCodes.OK_STATUS_CODE.value:
                parsed_response = BeautifulSoup(response.content, ConstantVariables.HTML_PARSER.value)
                comments_container = parsed_response.select(CSSSelectors.COMMENTS_CONTAINER.value)[0]

                for comment_detail in comments_container.find_all(class_=):
                    comment_title = get_text_of_comments(comment_detail, class_name="c-comments__title")
                    comment_content = get_text_of_comments(comment_detail, class_name="c-comments__content")
                    comment_positivities = get_text_of_comments(comment_detail, class_name="c-comments__modal-evaluation-item--positive")
                    comment_negativities = get_text_of_comments(comment_detail, class_name="c-comments__modal-evaluation-item--negative")


if __name__ == '__main__':
    crawled_urls = set()
    to_be_crawled_urls = get_raw_urls(4)
    crawl_web_page(to_be_crawled_urls, crawled_urls)

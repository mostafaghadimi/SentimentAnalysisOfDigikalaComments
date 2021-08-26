import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

from utils.enums import FormattedURLs, ErrorMessages, ConstantVariables, StatusCodes, Selectors, CommentObject


class DigikalaCrawler:
    def __init__(self, max_product_id):
        self.dataframe = pd.DataFrame()
        self.crawled_urls = set()
        self.to_be_crawled_urls = self._get_raw_urls(max_product_id)

    @staticmethod
    def _get_raw_urls(max_product_id):
        if not isinstance(max_product_id, int):
            raise ValueError(ErrorMessages.INT_TYPE_ERROR.value)
        urls = list()
        page_no = 1
        for product_id in range(3868296, max_product_id + 1):
            urls.append(
                FormattedURLs.BASE_URL.value.format(product_id, page_no)
            )
        return urls

    @staticmethod
    def get_text_of_comments(comment_detail, class_name):
        try:
            return comment_detail.find(class_=class_name).get_text()
        except AttributeError:
            return None

    def update_to_be_crawled_urls(self, comment_detail):
        try:
            comment_pages = comment_detail.find_all(class_=Selectors.COMMENT_PAGES.value)
            for comment_page in comment_pages:
                comment_page_url = comment_page['href']
                if comment_page_url.startswith(ConstantVariables.URL_FORMATS.value):
                    full_comment_page_url = FormattedURLs.DOMAIN_NAME.value.format(comment_page_url)
                    if full_comment_page_url not in self.to_be_crawled_urls:
                        self.to_be_crawled_urls.append(full_comment_page_url)
        except AttributeError:
            pass

    def crawl_web_pages(self):
        for to_be_crawled_url in self.to_be_crawled_urls:
            if to_be_crawled_url not in self.crawled_urls:
                response = requests.get(to_be_crawled_url)
                if response.status_code == StatusCodes.OK_STATUS_CODE.value:
                    parsed_response = BeautifulSoup(response.content, ConstantVariables.HTML_PARSER.value)
                    try:
                        comments_container = parsed_response.select(Selectors.COMMENTS_CONTAINER.value)[0]
                    except IndexError:
                        continue

                    self.update_to_be_crawled_urls(comments_container)

                    comment_details = comments_container.find_all(class_=Selectors.COMMENT_ITEMS.value)
                    for comment_detail in comment_details:
                        comment_title = self.get_text_of_comments(comment_detail,
                                                                  class_name=Selectors.COMMENT_TITLE.value)
                        comment_content = self.get_text_of_comments(comment_detail,
                                                                    class_name=Selectors.COMMENT_CONTENT.value)
                        comment_positivities = self.get_text_of_comments(comment_detail,
                                                                         class_name=Selectors.POSITIVE_COMMENTS.value)
                        comment_negativities = self.get_text_of_comments(comment_detail,
                                                                         class_name=Selectors.NEGATIVE_COMMENTS.value)
                        comment_helpfulness_score = self.get_text_of_comments(
                            comment_detail,
                            class_name=Selectors.COMMENT_HELPFULNESS_SCORE.value
                        )


                        comment_df = {
                            CommentObject.TITLE.value: comment_title,
                            CommentObject.CONTENT.value: comment_content,
                            CommentObject.POSITIVITIES.value: comment_positivities,
                            CommentObject.NEGATIVITIES.value: comment_negativities,
                            CommentObject.HELPFULNESS_SCORE.value: comment_helpfulness_score,
                        }

                        self.dataframe = self.dataframe.append(comment_df, ignore_index=True)

    def save_dataframe(self, file_format='csv', save_path='.'):
        if file_format == 'csv':
            self.dataframe.to_csv(os.path.join(save_path, 'dataset.{}'.format(file_format)))


if __name__ == '__main__':
    digikala_crawler = DigikalaCrawler(3868296)
    digikala_crawler.crawl_web_pages()
    digikala_crawler.save_dataframe()

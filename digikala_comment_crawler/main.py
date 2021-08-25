import os
import requests
import pandas as pd
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
        for product_id in range(3, max_product_id):
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

    def crawl_web_pages(self):
        print(self.to_be_crawled_urls)
        for to_be_crawled_url in self.to_be_crawled_urls:
            if to_be_crawled_url not in self.crawled_urls:
                response = requests.get(to_be_crawled_url)
                if response.status_code == StatusCodes.OK_STATUS_CODE.value:
                    parsed_response = BeautifulSoup(response.content, ConstantVariables.HTML_PARSER.value)
                    try:
                        comments_container = parsed_response.select(Selectors.COMMENTS_CONTAINER.value)[0]
                    except IndexError:
                        continue

                    for comment_detail in comments_container.find_all(class_=Selectors.COMMENT_ITEMS.value):
                        comment_title = self.get_text_of_comments(comment_detail,
                                                                  class_name=Selectors.COMMENT_TITLE.value)
                        comment_content = self.get_text_of_comments(comment_detail,
                                                                    class_name=Selectors.COMMENT_CONTENT.value)
                        comment_positivities = self.get_text_of_comments(comment_detail,
                                                                         class_name=Selectors.POSITIVE_COMMENTS.value)
                        comment_negativities = self.get_text_of_comments(comment_detail,
                                                                         class_name=Selectors.NEGATIVE_COMMENTS.value)
                        comment_df = {
                            CommentObject.TITLE.value: comment_title,
                            CommentObject.CONTENT.value: comment_content,
                            CommentObject.POSITIVITIES.value: comment_positivities,
                            CommentObject.NEGATIVITIES.value: comment_negativities,
                        }

                        self.dataframe = self.dataframe.append(comment_df, ignore_index=True)
                    print(self.dataframe.head())

    def save_dataframe(self, file_format='csv', save_path='.'):
        if file_format == 'csv':
            self.dataframe.to_csv(os.path.join(save_path, 'dataset.{}'.format(file_format)))


if __name__ == '__main__':
    digikala_crawler = DigikalaCrawler(10)
    digikala_crawler.crawl_web_pages()
    digikala_crawler.save_dataframe()
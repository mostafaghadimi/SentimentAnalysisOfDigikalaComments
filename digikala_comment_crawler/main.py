import os

import pandas as pd
import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup

from utils.enums import FormattedURLs, Messages, ConstantVariables, StatusCodes, Selectors, CommentObject
from utils.logger import get_global_logger


class DigikalaCrawler:
    logger = get_global_logger(__name__)

    def __init__(self, max_product_id):
        self.logger.info(Messages.CRAWLER_INIT_INFO.value)
        self.dataframe = pd.DataFrame()
        self.crawled_urls = set()
        self.to_be_crawled_urls = self._get_raw_urls(max_product_id, self.logger)

    @staticmethod
    def _get_raw_urls(max_product_id, logger):
        if not isinstance(max_product_id, int):
            raise ValueError(Messages.INT_TYPE_ERROR.value)
        urls = list()
        first_product_id = 1
        page_no = 1
        logger.info(Messages.URL_CREATION_INFO.value.format(first_product_id, max_product_id))
        for product_id in range(first_product_id, max_product_id + 1):
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
            self.logger.info(Messages.ADD_PAGINATION_INFO.value)
        except AttributeError:
            self.logger.error(Messages.PAGINATION_ERROR.value)

    async def crawl_web_pages(self):
        for to_be_crawled_url in self.to_be_crawled_urls:
            if to_be_crawled_url not in self.crawled_urls:
                async with aiohttp.ClientSession() as session:
                    async with session.get(to_be_crawled_url) as response:
                        if response.status == StatusCodes.OK_STATUS_CODE.value:
                            self.logger.info(Messages.START_CRAWLING_URL_INFO.value.format(to_be_crawled_url))
                            response_content = await response.text()
                            parsed_response = BeautifulSoup(response_content, ConstantVariables.HTML_PARSER.value)
                            try:
                                comments_container = parsed_response.select(Selectors.COMMENTS_CONTAINER.value)[0]
                            except IndexError:
                                self.logger.error(Messages.NO_COMMENTS_ERROR.value)
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
                            else:
                                self.logger.error(Messages.NOT_OK_STATUS_CODE.value.format(response.status))
                        self.crawled_urls.add(to_be_crawled_url)

    def save_dataframe(self, file_format='csv', save_path='.'):
        if file_format == 'csv':
            self.dataframe.to_csv(os.path.join(save_path, 'dataset.{}'.format(file_format)))
        self.logger.info(Messages.SAVING_DATAFRAME_INFO.value.format(file_format, save_path))


if __name__ == '__main__':
    digikala_crawler = DigikalaCrawler(6221912)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(digikala_crawler.crawl_web_pages())
    # digikala_crawler.crawl_web_pages()
    digikala_crawler.save_dataframe()

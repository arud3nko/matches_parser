from typing import List, Generator

from bs4 import BeautifulSoup

from ..types import Match, BaseHTTPClient, BaseMatchInfoParser


class MatchParser:
    def __init__(self, url: str, client: BaseHTTPClient, match_info_parser: BaseMatchInfoParser):
        """
        Инициализация

        :param url: Ссылка на Lite версию сайта
        :param client: HTTP-клиент
        :param match_info_parser: Парсинг информации о матчах
        """
        self._url = url
        self._client = client
        self._match_info_parser = match_info_parser

    def parse(self, date: int) -> Generator[Match, None, None]:
        """
        Парсинг информации о матчах

        :param date: Число дней, которое прибавляется/убавляется от сегодняшней даты.
            Example: date = 6 => датой будет Сегодня + 6 дней
        :return: Генератор матчей
        """
        matches = self._parse_matches_list(
            self._get_source_soup(date))

        for match in matches:
            match.team1_goals, match.team2_goals = self._match_info_parser.parse(
                base_url=self._url,
                match=match)

            yield match

    def _get_source_soup(self, date: int) -> BeautifulSoup:
        """
        Парсит страницу матчей с мобильной версии

        :return: Soup
        """
        params = {"d": date} if date else None

        response = self._client.get(
            url=self._url,
            params=params
        )

        return BeautifulSoup(response.text, 'html.parser')

    @staticmethod
    def _parse_matches_list(soup: BeautifulSoup) -> List[Match]:
        """
        Парсит список матчей

        :param soup: Soup
        :return: Список матчей
        """
        matches = []

        for match_data in soup.find_all('div', id='score-data'):
            for match_elem in match_data.find_all('span', recursive=False):
                league = match_elem.find_previous('h4').text.strip()
                time = match_elem.text.strip()

                title = match_elem.next_sibling.strip().split("-")
                teams = (title[0][:-1] if title[0].endswith(" ") else title[0],
                         title[-1][1:] if title[-1].startswith(" ") else title[-1])

                url_element = match_elem.find_next('a')
                url = url_element["href"]
                score = url_element.text.strip()

                match = Match(league=league, teams=teams, time=time, url=url, score=score)
                matches.append(match)

        return matches

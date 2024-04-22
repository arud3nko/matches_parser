import re

from typing import Tuple

from .utils import generate_headers
from ..types import Match, BaseHTTPClient, BaseMatchInfoParser


class MatchInfoParser(BaseMatchInfoParser):
    def __init__(self, url: str, client: BaseHTTPClient):
        """
        Инициализация
        :param url: URL к API (возможно, URL когда-то изменится, но АПИ вряд ли, поэтому останется только
        поменять URL)
        :param client: HTTP-клиент
        """
        self._url = url
        self._client = client

    def parse(self, base_url: str, match: Match) -> Tuple[str, str]:
        """

        Парсинг дополнительной информации по матчу

        :param base_url: Базовый URL сайта
        :param match: Матч
        :return:
        """

        try:
            info = self._fetch_api(base_url=base_url, match_url=match.url)
        except ValueError:
            print("ERROR")
            return "0:0", "0:0"

        return self._find_goal_ratio(match.teams[0], match.teams[1], info)

    def _fetch_api(self, base_url: str, match_url: str) -> str:
        """
        Отправляет запрос к API на получение таблицы с информацией.
        Достает из ответа два параметра - соотношение голов первой и второй команд.

        :param base_url: Базовый URL
        :param match_url: Идентификатор матча
        :return: Кортеж с параметрами
        """
        headers = generate_headers(url=base_url)

        match_id = re.search(r'/match/([^/?#]+)', match_url)
        match_id = match_id.group(1)

        response = self._client.get(
            url=f"{self._url}/df_to_1_{match_id}_1",
            headers=headers
        )

        if response.status_code != 200:
            raise ValueError

        return response.text

    @staticmethod
    def _find_goal_ratio(team1_name, team2_name, data) -> Tuple[str, str]:
        """
        Вычленяет из ответа API данные о соотношениях голов для двух команд

        :param team1_name: Команда 1
        :param team2_name: Команда 2
        :param data: Данные
        :return:
        """
        team_records = re.split(r'TN÷', data)
        team1_goals = "0:0"
        team2_goals = "0:0"
        for record in team_records:
            if record.startswith(team1_name):
                pattern_team1 = r'TG÷([\d:]+)'
                team1_goals_match = re.search(pattern_team1, record)
                if team1_goals_match:
                    team1_goals = team1_goals_match.group(1)
            elif record.startswith(team2_name):
                pattern_team2 = r'TG÷([\d:]+)'
                team2_goals_match = re.search(pattern_team2, record)
                if team2_goals_match:
                    team2_goals = team2_goals_match.group(1)
        return team1_goals, team2_goals

from datetime import datetime, timedelta

from match_parser import MatchParser, MatchInfoParser
from match_parser.parsers import RequestsClient
from match_parser.types import Match as MatchInfo

from db import DatabaseHandler, Match


def main(date: int):
    client = RequestsClient()

    db = DatabaseHandler('mysql+mysqlconnector://root:root@localhost:3306/football_matches')

    match_info_parser = MatchInfoParser(
        url="",
        client=client)

    matches_parser = MatchParser(
        url="",
        client=client,
        match_info_parser=match_info_parser
    )

    for match in matches_parser.parse(date=date):
        db.add_record(
            dataclass_to_db_model(match, date))


def dataclass_to_db_model(match: MatchInfo, date: int) -> Match:
    return Match(
        date=str(datetime.now().date() + timedelta(days=date)),
        league=match.league,
        team1_name=match.teams[0],
        team2_name=match.teams[1],
        match_time=match.time,
        match_url=match.url,
        match_score=match.score,
        team1_goals=match.team1_goals,
        team2_goals=match.team2_goals
    )


if __name__ == '__main__':
    main(0)

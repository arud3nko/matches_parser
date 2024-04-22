from dataclasses import dataclass

from typing import Optional, Tuple


@dataclass
class Match:
    """
    Дата-класс матча
    """

    league: str
    """Лига"""
    teams:  Tuple[str, str]
    """Команды матча"""
    time: str
    """Время"""
    url: str
    """Ссылка на матч"""
    score:  Optional[str] = None
    """Счет (отсутствует у не состоявшихся)"""
    team1_goals: Optional[str] = None
    team2_goals: Optional[str] = None
    """Соотношения голов"""

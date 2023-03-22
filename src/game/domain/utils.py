from .. import models


def get_latest_one_player_game_turns(
    game: models.OnePlayerGame, max_num_turns: int
) -> list[models.OnePlayerGameTurn]:
    """
    Return the latest turns in a one-player game.
    """

    # Since we can't use negative indexes on QuerySets, we just flip the order, get the
    # turns we want, then flip the selected turns back again
    game_turns = models.OnePlayerGameTurn.objects.filter(game=game).order_by(
        "-created_at"
    )
    return reversed(game_turns[:max_num_turns])

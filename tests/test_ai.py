from othello.game_engine import ai_game_loop

def test_ai_outperforms_random_moves():
    ai_win_rate = 0
    games = 50

    for _ in range(games):
        if ai_game_loop(random_moves=True) == "Light":
            ai_win_rate += 1

    ai_win_percentage = (ai_win_rate / games)
    assert ai_win_percentage >= 0.80
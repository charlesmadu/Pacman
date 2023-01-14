from player import *
player = Player()

while player.game_loop:
    player.clock.tick(fps)
    # MENU SCREEN OPTIONS
    player.close_game_event()
    if player.state == "log_in_screen":
        player.log_in_screen()
    if player.state == "menu":
        player.menu_draw_screen()
    if player.state == "singleplayer" or player.state == "gameover_singleplayer":
        player.singleplayer_draw_screen()
    if player.state == "singleplayer":
        player.singleplayer_event_manager()
    if player.state == "multiplayer" or player.state == "gameover_multiplayer":
        player.multiplayer_event_manager()
        player.multiplayer_draw_screen()
    if player.state == "leaderboard":
        player.leaderboard_draw_screen()
    if player.state == "about":
        player.about_draw_screen()
    if player.state == "quit":
        quit()

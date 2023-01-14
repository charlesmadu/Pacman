import socket
from _thread import *
import json
import copy

PORT = 50001
HOST = "192.168.0.4"

# [PLAYER[0], PLAYER[1], GHOSTS, TIME, LIVES, IS_ALIVE, LEVEL_OVER, LEVEL, IS_WAITING, HAS_STARTED]
# ORDER IS [CENTER_POSITION[0], CENTER_POSITION[1], DIRECTION[0], DIRECTION[1], SCORE, PLAYER_NUMBER, IS_PAUSED]
# GHOST ORDER: RED, BLUE, BLACK, ORANGE
# DATA ORDER IN GHOSTS: [PIXEL_POS[0], PIXEL_POS[1], DIRECTION[0], DIRECTION[1], CENTER_POS[0], CENTER_POS[1], IS_FRIGHTENED, IS_ALIVE, ID_NUMBER]
positions = [[238, 350, 0, 0, 5, 0, False], [294, 350, 0, 0, 5, 1, False], [[252, 224, 0, 0, 266, 238, False, True, 0], [224, 280, 0, 0, 238, 294, False, True, 1], [280, 280, 0, 0, 294, 294, False, True, 2], [252, 280, 0, 0, 266, 294, False, True, 3]], 0, 3, True, False, 1, True, False]


def client(connection, player, game_id):

    ##### client #######
    # Parameters : dots_list:List, fruit_positions:List, fruit_pictures:List
    # Return Type : None
    # Purpose :- Threaded client that occurs when a player joins the network. Data is both sent, updated and received here.
    ##########################

    connection.send(str.encode(json.dumps((game_data[game_id][player], game_data[game_id][3], game_data[game_id][8]))))
    # SENDS INITIAL DATA UPON FIRST CONNECTING

    while True:
        try:
            receive_data = json.loads(connection.recv(2048).decode())

            if game_id in game_data:
                player_data = game_data[game_id]
            # TRY TO RECEIVE DATA

                if not receive_data:
                    print("you have disconnected")
                    # IF YOU COULD NOT RECEIVE DATA BREAK AND DISCONNECT

                else:
                    if player_data[8]:
                        # IF WAITING
                        if player == 1:
                            # IF IT IS PLAYER TWO

                            player_data[8] = False
                            # UPDATE WAITING TO FALSE

                    if receive_data == "wait":
                        # IF PLAYER ONE IS WAITING

                        sending_data = player_data[8]
                        connection.sendall(str.encode(json.dumps(sending_data)))
                        # SEND WAITING VARIABLE FROM GAME DATA

                    if len(receive_data) == 2:
                        # UPDATE PAUSED VARIABLES

                        player_data[9] = receive_data[0]
                        player_data[3] = receive_data[1]
                    if len(receive_data) == 7:
                        # DATA IS FOR THE GHOSTS AND SOME GLOBAL VARIABLES

                        player_data[2] = receive_data[0]
                        player_data[3] = receive_data[1]
                        if player_data[4] != receive_data[2]:
                            player_data[4] = receive_data[2]
                        if player_data[5] != receive_data[4]:
                            player_data[5] = receive_data[4]
                        if player_data[6] != receive_data[5]:
                            player_data[6] = receive_data[5]
                        if player_data[7] != receive_data[3]:
                            player_data[7] = receive_data[3]
                        if player_data[9] != receive_data[6]:
                            player_data[9] = receive_data[6]
                        print("received and updating:", receive_data)
                        # UPDATE IT

                    elif len(receive_data) == 6:
                        # DATA RECEIVED FROM ONE PLAYER

                        player_data[player][0] = receive_data[0]
                        player_data[player][1] = receive_data[1]
                        if player_data[player][2] != receive_data[2]:
                            player_data[player][2] = receive_data[2]
                        if player_data[player][3] != receive_data[3]:
                            player_data[player][3] = receive_data[3]
                        player_data[player][4] = receive_data[4]

                        if player_data[player][6] != receive_data[5]:
                            player_data[player][6] = receive_data[5]

                        if player == 0:
                            sending_data = player_data[1], player_data[2], player_data[3], player_data[4], player_data[5], player_data[6], player_data[7], player_data[9]
                        if player == 1:
                            sending_data = player_data[0], player_data[2], player_data[3], player_data[4], player_data[5], player_data[6], player_data[7], player_data[9]
                        # print("received:", receive_data)
                        # print("sending:", sending_data)
                        connection.sendall(str.encode(json.dumps(sending_data)))
                        # SEND THE DATA OF THE OPPOSITE PLAYER AS WELL AS SOME GLOBAL VARIABLES

                        # SEND [OPPOSITE_PLAYER_LOCATION, GHOSTS, LIVES, IS_ALIVE, LEVEL_OVER, LEVEL]
            else:
                break
        except:
            break

            # IF SOMETHING GOES WRONG BREAK AND DISCONNECT

    print("the connection has been lost")
    try:
        print("Game", game_id, "is closing")
        # del game_data[game_id]
    except:
        pass

    connection.close()
# CONNECTION LOST CLOSE THE SERVER


current_player = 0
game_data = {}
game_id = 0
# INITIAL VARIABLES


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_variable:
    try:
        # CREATES SERVER
        socket_variable.bind((HOST, PORT))
        socket_variable.listen()
        # LISTEN FOR CONNECTION

    except socket.error as e:
        str(e)
        # SOCKET ERROR

    print("Server Is Up")
    # OUTPUT TO SHOW THE SERVER IS UP
    while True:
        connection, address = socket_variable.accept()
        # WHEN A USER JOINS GETS CONNECTION AND ADDRESS

        print("Conntected to:", address)
        # OUTPUT TO SHOW ADDRESS

        start_new_thread(client, (connection, current_player, game_id))
        # START NEW PLAYER THREAD
        if current_player == 1:
            game_id += 1
            current_player = 0
        else:
            current_player += 1
            game_data[game_id] = copy.deepcopy(positions)
            # MAKE A COPY OF POSITIONS LIST

        # ADD 1 TO NEW CURRENT PLAYER SO WHEN A NEW PLAYER JOINS THEIR ID IS DIFFERENT

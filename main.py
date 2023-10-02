import phoenix
from time import sleep
import json
import time
import threading
import getports
import classes as cl
import ctypes
import random
import emoji
from player import Player

def initializeApi(Player):
    Player.port = getports.returnCorrectPort(Player.name)
    Player.api = phoenix.Api(Player.port)
    
def packetLogger(Player):
    # Logs all the packets that are sent/received from the client
    while Player.api.working():
        if not Player.api.empty():
            msg = Player.api.get_message()
            json_msg = json.loads(msg)

            # catches send and recieve packets and appends 0 or 1 to the beggining of them
            if str(json_msg["type"]) == "0" or str(json_msg["type"]) == "1":
                packet = str(str(json_msg["type"]) + " " + json_msg["packet"])
                if packet.startswith("1 at "+str(Player.id)):
                    splitPacket = packet.split()
                    Player.pos = [int(splitPacket[4]), int(splitPacket[5])]
                if packet.startswith("0 walk"):
                    splitPacket = packet.split()
                    Player.pos = [int(splitPacket[2]), int(splitPacket[3])]
                if packet.startswith("1 in 2"):
                    splitPacket = packet.split()
                    vnum = splitPacket[3]
                    npc_id = splitPacket[4]
                    x = splitPacket[5]
                    y = splitPacket[6]
                    if vnum == "2110":
                        cl.npcs.steve_stuff_id = npc_id
                        cl.npcs.steve_stuff_pos[0] = x
                        cl.npcs.steve_stuff_pos[1] = y

            # catches player_information query
            if str(json_msg["type"]) == "16":
                player_info = json_msg["player_info"]
                Player.id = player_info["id"]
                Player.pos[0] = player_info["x"]
                Player.pos[1] = player_info["y"]

            # catches inventory query
            if str(json_msg["type"]) == "17":
                inventory = json_msg["inventory"]
                for item in inventory["etc"]:
                    if item["vnum"] == 2800:
                        Player.gold_aot_medals_amount += int(item["quantity"])
                    if item["vnum"] == 2801:
                        Player.silver_aot_medals_amount += int(item["quantity"])
                for item in inventory["main"]:
                    if item["vnum"] == 5889:
                        Player.gold_boxes_pos = int(item["position"])
                        Player.gold_boxes_amount = int(item["quantity"])
                    if item["vnum"] == 5890:
                        Player.silver_boxes_pos = int(item["position"])
                        Player.silver_boxes_amount = int(item["quantity"])
                    if item["vnum"] in [5899, 5898, 5897, 5896, 5895, 5894, 5893, 5892]:
                        Player.medals_to_use.append([int(item["position"]), int(item["quantity"])])
        else:
            sleep(0.01)
    Player.api.close()

def getRandomDelay(min,max):
    randomizedDelay = random.randint(min*1000,max*1000)/1000
    return(randomizedDelay)

def select_target(Player,target,entity_type):
    api = Player.api
    if int(target) == 0:
        pass
    else:
        api.target_entity(target, entity_type)

if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleTitleW("AOT medals bot by stradiveri")
    players = []
    players_names = []

    # this if statement is there in case you are using a config to load characters beforehand
    if cl.user_settings.characters != "":
        splitCharactes=cl.user_settings.characters.split(",")

        for name in splitCharactes:
            player = Player()
            player.name = name
            initializeApi(player)
            t = threading.Thread(target=packetLogger, args=(player,))
            t.start()
            players.append(player)
    else:
        print(emoji.emojize(":sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun:"))
        print(emoji.emojize(":sun::bird:PHOENIX BOT API EXTENSION BY STRADI:frog: :sun:"))
        print(emoji.emojize(":sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun::sun:"))
        print("")
        print(emoji.emojize(":1st_place_medal:Your characters :clown_face:: "))
        ports_and_names_unsorted = getports.returnAllPorts()

        # Sort the array based on the first element of each sub-array
        ports_and_names = sorted(ports_and_names_unsorted, key=lambda x: x[0])

        for i in range(len(ports_and_names)):
            ports_and_names[i].append(i+1)

        for i in range(len(ports_and_names)):
            print(str(ports_and_names[i][2])+") "+str(ports_and_names[i][0]))

        print("")
        print(emoji.emojize(":fire:Leave empty and press Enter, to stop:stop_sign:"))
        print(emoji.emojize(":pregnant_man:Type cepik to select all:monkey:"))
        print("")

        # while loop that runs until you press leave empty and press enter or until you use the keyword "cepik" to select all characters
        while True:
            print(emoji.emojize(":keyboard:Type name(or index:input_numbers:) of your character: "), end="")
            index = input()
            if str(index)=="":
                    break
            if str(index)=="cepik":
                for i in range(len(ports_and_names)):
                    index = ports_and_names[i][0]
                    if index in players_names:
                        print(emoji.emojize(index+" already in the list.:eggplant:"))
                    else:
                        player = Player()
                        player.name = index
                        initializeApi(player)
                        t = threading.Thread(target=packetLogger, args=(player,))
                        t.start()
                        players_names.append(index)
                        players.append(player)
                break
  
            for element in ports_and_names:
                if str(index) == str(element[0]) or index == str(element[2]):
                    index = str(element[0])
                    if index in players_names:
                        print(emoji.emojize(index+" already in the list.:eggplant:"))
                    else:
                        player = Player()
                        player.name = index
                        initializeApi(player)
                        t = threading.Thread(target=packetLogger, args=(player,))
                        t.start()
                        players_names.append(index)
                        players.append(player)
                else:
                    pass
        print("")
    print(emoji.emojize(":1st_place_medal::2nd_place_medal::3rd_place_medal:AOT medals bot sucesfully started at: "+str(time.strftime('%H:%M:%S')+":1st_place_medal::2nd_place_medal::3rd_place_medal:")))
    print("selected characters("+str(len(players))+"): ", end="")
    for i in range(len(players)-1):
        print(players[i].name, end=", ")
    print(players[-1].name)
    print("")
    
    # main part of the code, made into a function to allow threading
    def do(pl):
        # query to get player id and position as seen in the packetlogger function
        pl.api.query_player_information()
        time.sleep(0.1)
        pl.api.query_inventory()
        time.sleep(0.1)
        pl.api.send_packet("n_run 18")
        time.sleep(getRandomDelay(0.5,1.5))
        pl.api.send_packet("n_run 17 0 1 "+str(pl.id))
        time.sleep(getRandomDelay(0.5,1.5))
        pl.api.send_packet("#arena^0^1")
        time.sleep(getRandomDelay(0.5,1.5))
        
        # walk to the npc
        npc_pos_x = random.randint(35,41)
        npc_pos_y = random.randint(45,47)
        pl.api.player_walk(npc_pos_x, npc_pos_y)
        pl.api.pets_walk(npc_pos_x, npc_pos_y)
        while pl.pos != [npc_pos_x, npc_pos_y]:
            pl.api.player_walk(npc_pos_x, npc_pos_y)
            pl.api.pets_walk(npc_pos_x, npc_pos_y)
            time.sleep(0.2)

        # calculate for how many boxes you have medlas
        gold_medals_boxes = int(pl.gold_aot_medals_amount/8)
        silver_medals_boxes = int(pl.silver_aot_medals_amount/24)
        
        # if you have enough medals for atleast one box, this gets executed
        if (gold_medals_boxes + silver_medals_boxes) > 0:
            select_target(players[i], int(cl.npcs.steve_stuff_id), 2)
            time.sleep(getRandomDelay(0.5,1.5))
            pl.api.send_packet("npc_req 2 "+(cl.npcs.steve_stuff_id))
            time.sleep(getRandomDelay(0.3,0.7))
            pl.api.send_packet("n_run 14 17 2 "+(cl.npcs.steve_stuff_id))
            time.sleep(getRandomDelay(0.3,0.7))

            #loop that always opens window, starts dancing, sends all the required packets finishes crafting and repeat
            pl.api.send_packet("pdtse 1 5889")
            for k in range(gold_medals_boxes):
                pl.api.send_packet("pdtse 1 5889")
                time.sleep(getRandomDelay(0.3,0.7))
                pl.api.send_packet("guri 2")
                for j in range(5):
                    pl.api.send_packet("guri 5 1 "+str(pl.id)+" "+str(j*20)+" -2")
                    time.sleep(1)
                pl.api.send_packet("guri 5 1 "+str(pl.id)+" 100 -2")
                time.sleep(0.1)
                pl.api.send_packet("pdtse 0 5889 -1 -1 0")
                time.sleep(1)
                pl.api.send_packet("n_run 14 17 2 "+(cl.npcs.steve_stuff_id))
                time.sleep(1)

            time.sleep(1)
            #loop that always opens window, starts dancing, sends all the required packets finishes crafting and repeat
            for k in range(silver_medals_boxes):
                pl.api.send_packet("pdtse 1 5890")
                time.sleep(getRandomDelay(0.3,0.7))
                pl.api.send_packet("guri 2")
                for j in range(5):
                    pl.api.send_packet("guri 5 1 "+str(pl.id)+" "+str(j*20)+" -2")
                    time.sleep(1)
                pl.api.send_packet("guri 5 1 "+str(pl.id)+" "+str(j*20)+" -2")
                time.sleep(0.1)
                pl.api.send_packet("pdtse 0 5890 -1 -1 0")
                time.sleep(1)
                pl.api.send_packet("n_run 14 17 2 "+(cl.npcs.steve_stuff_id))
                time.sleep(1)
        
        # thanks to Zanou for shop_end 1 packet to close the window after
        pl.api.recv_packet("shop_end 1")

        # query to see how many boxes you got now
        pl.api.query_inventory()
        time.sleep(0.2)
        
        #loops for opening the new boxes
        for l in range(pl.gold_boxes_amount):
            pl.api.send_packet("u_i 1 "+str(pl.id)+" 1 "+str(pl.gold_boxes_pos)+" 0 0")
            time.sleep(getRandomDelay(0.75,1))
        for l in range(pl.silver_boxes_amount):
            pl.api.send_packet("u_i 1 "+str(pl.id)+" 1 "+str(pl.silver_boxes_pos)+" 0 0")
            time.sleep(getRandomDelay(0.75,1))

        # medals_to_use variable gets set back to [] to avoid having duplicites
        pl.medals_to_use = []
        # query to see how many medals you got, could be done in a better way withouth needing to call invetory query again
        pl.api.query_inventory()
        time.sleep(0.1)

        # loop to use the new medals
        for medal in pl.medals_to_use:
            for m in range(medal[1]):
                time.sleep(getRandomDelay(0.75,1))
                pl.api.send_packet("u_i 2 "+str(pl.id)+" 1 "+str(medal[0])+" 0 0")
        print(emoji.emojize(str(pl.name)+" done:thumbs_up:"))
        time.sleep(cl.user_settings.char_delay)

    # loop that runs each character in seperate thread, so they can run simultaneously
    threads_list = []
    for i in range(len(players)):
        t = threading.Thread(target=do, args=[players[i], ])
        t.start()
        threads_list.append(t)
        sleep_for = getRandomDelay(2.5,25)
        time.sleep(sleep_for)
    
    #checking if all the threads are finishhed
    for thread in threads_list:
        thread.join()
    
    print("")
    print(emoji.emojize(":OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand:"))
    print(emoji.emojize(":OK_hand:BOT FINISHED YOU CAN CLOSE THE WINDOW NOW :OK_hand:"))
    print(emoji.emojize(":OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand::OK_hand:"))

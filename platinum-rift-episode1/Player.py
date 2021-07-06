import sys
import math
import random


# Zone class has 5 attributes
# zid: zone id
# platinum_bar: number of platinum bars zone has
# owner: id of zone owner
# links: list of link(connections with other zone) ids of zone. initially -1(neutral)
# pods: list of pods of every player have inside of zone. [player0, player1, player2, player3]
class Zone:

    def __init__(self, zid, platinum_bar, ):
        self.zid = zid
        self.platinum_bar = platinum_bar
        self.owner = -1
        self.links = []
        self.pods = [0, 0, 0, 0]

    def add_links(self, links):
        self.links = links

    def add_pods(self, owner, pods):
        self.owner = owner
        self.pods = pods


# returns purchasable pod number
def get_max_pods(num):
    return num // 20


# player_count: the amount of players (2 to 4)
# my_id: my player ID (0, 1, 2 or 3)
# zone_count: the amount of zones on the map
# link_count: the amount of links between all zones
player_count, my_id, zone_count, link_count = [int(i) for i in input().split()]
zone_list = {}  # list of all zones
pri_list = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [],
            6: []}  # priority dict based on number of platinum bars, value of key 0 is list of zones has 0 platinum
my_zones = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [],
            6: []}  # dict of my zones, value of key 0 is list of my zones has 0 platinum
for i in range(zone_count):
    # zone_id: this zone's ID (between 0 and zoneCount-1)
    # platinum_source: the amount of Platinum this zone can provide per game turn
    zone_id, platinum_source = [int(j) for j in input().split()]
    zone_list[i] = Zone(zid=zone_id, platinum_bar=platinum_source)  # adding zones to zone_list
    pri_list[platinum_source].append(zone_id)  # adding zones to pri_list
for i in range(link_count):
    zone_1, zone_2 = [int(j) for j in input().split()]
    zone_list[zone_1].links.append(zone_2)  # adding link info of zone_1 to zone object inside of zone_list
    zone_list[zone_2].links.append(zone_1)  # adding link info of zone_2 to zone object inside of zone_list
isFirst = True  # shows is it first turn, initially True
# game loop
while True:
    platinum = int(input())  # my available Platinum
    for i in range(zone_count):
        # z_id: this zone's ID
        # owner_id: the player who owns this zone (-1 otherwise)
        # pods_p0: player 0's PODs on this zone
        # pods_p1: player 1's PODs on this zone
        # pods_p2: player 2's PODs on this zone (always 0 for a two player game)
        # pods_p3: player 3's PODs on this zone (always 0 for a two or three player game)
        z_id, owner_id, pods_p0, pods_p1, pods_p2, pods_p3 = [int(j) for j in input().split()]
        zone_list[z_id].add_pods(owner_id, [pods_p0, pods_p1, pods_p2, pods_p3])  # updating info inside of zone_list
        if zone_list[z_id].owner == my_id:
            my_zones[zone_list[z_id].platinum_bar].append(z_id)  # updating info inside my_zones

    # commands: current command string
    # max_pod: purchasable pod
    # pod: number of purchased pods
    # zid: zone id
    # adds new command to commands string and updates max_pod
    def add_spawn_command(commands, max_pod, pod, zid):
        commands = commands + f"{pod} {zid} "
        max_pod = max_pod - pod
        return commands, max_pod  # returns updated commands and max_pod

    # checks is game in late phase
    # if every zone has owner(no neutral zone) then returns True, otherwise returns False
    def is_late_game():
        for zid in range(zone_count):
            if zone_list[zid].owner == -1:
                return False
        return True

    # adds 2 pods to the most prioritized zones and if side(neighbor) zone has 3+ platinum then,
    # adds 1 pods to the side zone but not more than 2 times because,
    # spreading is just as important as the platinum bars
    # after 2 times adds 1 pods to the other prioritized zones
    def side_zone_control_spawn(commands, max_pod):
        count = 0  # number of times that pod purchase to the side zones(most 2)
        for i in reversed(range(7)):  # most prioritized 6 to less prioritized 0
            for zid in pri_list.get(i):  # for every zid(zone id) that has priority i
                if max_pod > 0 and count < 2:  # if purchasable pod number greater than 0 and count is lesser than 2
                    commands, max_pod = add_spawn_command(commands, max_pod, 2,
                                                          zid)  # adds 2 pod to the current most prioritized zone
                    count = count + 1
                    # choosing most prioritized side(neighbor) zone
                    side_zone = [0, 0]  # id, platinum bar
                    for links in zone_list[zid].links:  # for links of stated(by zid) zone
                        if zone_list[links].platinum_bar > side_zone[1]:
                            side_zone[0] = links
                            side_zone[1] = zone_list[links].platinum_bar
                    if side_zone[1] > 3:  # checking is side zone's platinum is greater than 3 or not
                        commands, max_pod = add_spawn_command(commands, max_pod, 1, side_zone[0])
                elif max_pod > 0 and count >= 2:  # if count is greater than 2 then adding 1 pod to prioritized zone
                    commands, max_pod = add_spawn_command(commands, max_pod, 1, zid)
                else:
                    return commands, max_pod
        return commands, max_pod  # returns updated commands and max_pod

    # This is first turn strategy and this method will be used, if number of players is greater than 2.
    # For this method priority for first turn changes 4 so I spawn pods to zones that
    # has 4 or lesser platinum bars. If the number of zones with 5 and 6 platinum bar is higher than 6,
    # I use side zone control strategy. If not then I spawn 2 pods to most prioritized zones
    def high_zone_number_based_spawn(commands, max_pod):
        # checks number of zones that has 5 and 6 platinum bar is higher than 6
        if len(pri_list.get(6)) + len(pri_list.get(5)) >= 6:
            # uses side zone control strategy (explained in side_zone_control_spawn() method)
            for i in reversed(range(5)):  # most prioritized is zones that has 4 platinum bar
                count = 0
                for zid in reversed(pri_list.get(i)):
                    if max_pod > 0:
                        if count > 2:
                            commands, max_pod = add_spawn_command(commands, max_pod, 1, zid)
                        else:
                            commands, max_pod = add_spawn_command(commands, max_pod, 2, zid)
                            count += 1
                    else:
                        return commands, max_pod
        else:
            # adding 2 pods to most prioritized zones
            for i in reversed(range(5)):  # most prioritized is zones that has 4 platinum bar
                for zid in reversed(pri_list.get(i)):
                    if max_pod > 0:
                        commands, max_pod = add_spawn_command(commands, max_pod, 2, zid)
                    else:
                        return commands, max_pod
        return commands, max_pod

    # this is a late game spawn strategy, it checks from most prioritized to lesser zones. If zone has a link with
    # enemy zone then I spawn 1 pod to this zone. if we still have purchasable pods, additionally I add 1 pod to the
    # zones that has link with enemy zones which has enemy pods.
    def late_game_spawn(commands, max_pod):
        for i in reversed(range(7)):
            for zid in my_zones.get(i):
                # checks that if zone has a link with enemy zone
                add_pod = False
                for links in zone_list[zid].links:
                    if zone_list[links].owner != my_id:
                        add_pod = True
                if add_pod:
                    commands, max_pod = add_spawn_command(commands, max_pod, 1, zid)
        if max_pod > 0:
            for i in reversed(range(7)):
                for zid in my_zones.get(i):
                    # checks that if zone has enemy zones which has enemy pods
                    for links in zone_list[zid].links:
                        if max_pod > 0 and zone_list[links].owner != my_id and zone_list[links].owner != -1 and \
                                zone_list[links].pods[zone_list[links].owner] > 0:
                            commands, max_pod = add_spawn_command(commands, max_pod, 1, zid)
        return commands, max_pod

    # this is a mid game spawn strategy, it checks from most prioritized to lesser zones. If my zone has a link with
    # enemy zones that has enemy pods, I add 1 pod to the my zone. Then if I had purchasable pods I add 1 pod to the
    # this neutral zones from most prioritized to lesser zones. If there is still purchasable pods, then I add pods to
    # the my zones from most prioritized to lesser zones.
    def mid_game_spawn(commands, max_pod):
        for i in reversed(range(7)):
            for zid in my_zones.get(i):
                # checks thatIf my zone has a link with enemy zones that has enemy pods
                for links in zone_list[zid].links:
                    if max_pod > 0 and zone_list[links].owner != my_id and zone_list[links].owner != -1 and \
                            zone_list[links].pods[zone_list[links].owner] > 0:
                        commands, max_pod = add_spawn_command(commands, max_pod, 1, zid)
        if max_pod > 0:
            # adds 1 pod to the most prioritized neutral zones
            for i in reversed(range(7)):
                for zid in pri_list.get(i):
                    if max_pod > 0:
                        if zone_list.get(zid).owner == -1:
                            commands, max_pod = add_spawn_command(commands, max_pod, 1, zid)
                    else:
                        return commands, max_pod
        # adds pods to the my zones
        while max_pod > 0:
            if len(my_zones[6]) != 0:
                rand_id = random.choice(my_zones[6])
            elif len(my_zones[5]) != 0:
                rand_id = random.choice(my_zones[5])
            elif len(my_zones[4]) != 0:
                rand_id = random.choice(my_zones[4])
            elif len(my_zones[3]) != 0:
                rand_id = random.choice(my_zones[3])
            elif len(my_zones[2]) != 0:
                rand_id = random.choice(my_zones[2])
            elif len(my_zones[1]) != 0:
                rand_id = random.choice(my_zones[1])
            else:
                rand_id = random.choice(my_zones[0])
            commands, max_pod = add_spawn_command(commands, max_pod, 1, rand_id)
        return commands, max_pod

    # this is main pod movement method, firstly checks that my_zones that has pods and looks possible zone captures that
    # pod can do and captures(moves) to the most prioritized zone, if there are zones that has same priority then
    # chooses enemy zones over neutral ones. If there is no possible zones,
    # then it will move to the another ally zone randomly
    def move_command():
        commands = ""  # command string
        for i in reversed(range(7)):
            for zid in my_zones[i]:
                if zone_list[zid].pods[my_id] > 0:  # checks that is zone has pods or not
                    side_zones = [-1, -1, -1]  # zone id, platinum, owner
                    #  checks every link
                    for links in zone_list[zid].links:
                        #  if there is possible capture updates side_zones
                        if zone_list[links].owner != my_id and zone_list[links].platinum_bar >= side_zones[1]:
                            # if platinum bars equals with current prioritized and if new one is enemy then changes to
                            # the enemy zone
                            if zone_list[links].platinum_bar == side_zones[1] and side_zones[2] != -1:
                                side_zones[0] = links
                                side_zones[1] = zone_list[links].platinum_bar
                                side_zones[2] = zone_list[links].owner
                            # if it is greater then current prioritized, then changes to the new one
                            if zone_list[links].platinum_bar > side_zones[1]:
                                side_zones[0] = links
                                side_zones[1] = zone_list[links].platinum_bar
                                side_zones[2] = zone_list[links].owner
                    if side_zones[0] > -1:  # checks is there any possible zone capture
                        commands = commands + f"{1} {zid} {side_zones[0]} "
                        zone_list[zid].pods[my_id] -= 1
                    else:  # no possible captures
                        link_id = random.choice(zone_list[zid].links)
                        commands = commands + f"{1} {zid} {link_id} "
                        zone_list[zid].pods[my_id] -= 1
        return commands

    # this is main pod spawn method, this method chooses which strategy(method) will be used
    def spawn_command():
        max_pod = get_max_pods(platinum)  # gets purchasable pod number
        commands = ""  # command string
        if max_pod > 0:  # checks is there any purchasable pod
            global isFirst
            if isFirst:  # checks is it first turn
                isFirst = False
                if player_count <= 2:  # checks player count
                    commands, max_pod = side_zone_control_spawn(commands, max_pod)
                else:
                    commands, max_pod = high_zone_number_based_spawn(commands, max_pod)
                return commands
            elif is_late_game():  # checks is it late game
                commands, max_pod = late_game_spawn(commands, max_pod)
                return commands
            else:  # mid game
                commands, max_pod = mid_game_spawn(commands, max_pod)
                return commands


    spawn_cmd = spawn_command()
    move_cmd = move_command()
    if move_cmd is not None and len(move_cmd.split()) != 0:  # checks that is there any command
        move_cmd = move_cmd[:-1]  # removes last letter of command which is ' '(space)
    else:  # if not changes '' to the 'WAIT'
        move_cmd = "WAIT"
    if spawn_cmd is not None and len(spawn_cmd.split()) != 0:  # checks that is there any command
        spawn_cmd = spawn_cmd[:-1]  # removes last letter of command which is ' '(space)
    else:
        spawn_cmd = "WAIT"

    # first line for movement commands, second line for POD purchase (see the protocol in the statement for details)
    print(move_cmd)
    print(spawn_cmd)

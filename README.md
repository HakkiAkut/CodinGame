# coding-game-HakkiAkut
coding-game-HakkiAkut created by GitHub Classroom

## **Rank**
The current rank was Gold League, 61/256

## **Strategy**
There is two type of operations which is moving pods and purchasing pods. Player firstly moves then purchases pods so new purchased pods cannot be moved.

### **Movement**
I have priority dictionary(pri_list) based on number of platinum bars, value of key 0 is list of zones that has 0 platinum.
Movement method firstly checks that my zones that has pods, if zone has pods then checks that is there any captures. Method picks most prioritized zone by checking pri_list
if there are zones that has same priority then chooses enemy zones over neutral ones, eliminating the enemy is more important. Also there is chance that
there is not possible captures then it will move to the another ally zone randomly(I tried to do path finding but there is a time limit and path finding for every pod consumes
too much time).

### **Purchase**
In my opinion game has 3 phases which is early, mid and late game. Early game is basically first turn, even it is only one turn, this is the most important and winner deciding turn
Mid game is from second turn to turn that there is no neutral zone(every zone has owner). Late game is starts from  the turn that there is no neutral zone. I used 4 different
spawn(purchase) strategies. 2 different in early game, 1 in mid game and 1 in late game.

#### **Early Game Purchase Strategies**
Number of players is important if there is more than one enemy player than, i didn't focus on zones that has 5 and 6 platinum bars. Because generally players focusng on them and
my pods will eliminated instantly so game becomes unwinnible. 

If there is one enemy player then I use side_zone_control_spawn strategy which is
adding 2 pods to the most prioritized zones(which includes zones that has 5 and 6 platinum bar) and if side(neighbor) zone has 3+ platinum then, I adds 1 pods to the side zone but
not more than 2 times because spreading is just as important as the platinum bars after 2 times adds 1 pods to the other prioritized zones.

If there is more than one enemy then I use high_zone_number_based_spawn strategy. I focus on zones that has 4 platinum and lesser but even I didn't focus on zones that has
5 and 6 platinum bars, there is chance that there could be no zones that has 5 and 6 platinum bars. So Most prioritized ones becomes zones that has 4 platinum so my game will
be ruined again so Method will check the number of zones that has 5 and 6 platinum bars. If it is greater than 6 then I will use the strategy that same as side_zone_control_spawn
but this one will focus on zones that has 4 platinum and lesser(which not zones that has 5 and 6 platinum bar). If number of that has 5 and 6 platinum bars lesser than 6,
then method will send 2 pods to every prioritized zone and make sure that i will live another round and gain something. Changing my focus to more lesser zones is not good because
it would be valueless.

#### **Mid Game Purchase Strategies**
it checks from most prioritized to lesser zones. If my zone has a link with enemy zones that has enemy pods, I add 1 pod to the my zone because protecting my zones are more valuable
than spreading. Then if I had purchasable pods I add 1 pod to the neutral zones from most prioritized to lesser zones. If there is still purchasable pods, then I add pods to the my zones from most prioritized to lesser zones.

#### **Late Game Purchase Strategies**
 it checks from most prioritized to lesser zones. If zone has a link with enemy zone then I spawn 1 pod to this zone.
 if we still have purchasable pods, I add 1 pod to the zones that has link with enemy zones which has enemy pods.

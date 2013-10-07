import random

# War card game simulator
# The purpose of this program is to explore different "strategies" in the card game war. While some would call it a 0 player game, the players actually have a tiny input
# on the game's outcome: card ordering. Every time a "battle" or "war" is concluded, the victor takes the cards, but it is rarely specified in what order these cards must be taken.
# By running thousands of games with players using different card sorting "strategies", we can determine which are the strongest.
#
#
#
# First and foremost, we'll explain the play styles.
print ("Let's simulate some games of WAR! After each battle, the victor places the spoils under their deck according to their play style.\n")
print ("0 -  Sorts the cards ascending, so the lowest card will be played first.")
print ("1 -  Sorts the cards descending, so the highest card will be played first.")
print ("2 -  Preserves play order, placing own cards first.")
print ("3 -  Preserves play order, placing opponent's cards first.")
print ("4 -  Shuffles the cards randomly.\n")
# Then we'll ask the user to specify which two play styles will be opposed.
style1 = int(input ("How should Player 1 play?\t"))
style2 = int(input ("How should Player 2 play?\t"))
# And how many games should be played.
gamestoplay = int(input ("How many games would you like played?\n"))
# And finally, initialize the number of wins for each side.
wins1 = 0
wins2 = 0
infinitegames = 0

# The gameplay will rely on two support functions.
# The first is code that creates a shuffled deck of cards. First, it populates a list with the numbers 1-13, four times each. (These represent the full deck)
# It then pulls a random card from the pile, and adds it to the finished deck, looping this proccess until the deck is fully randomized.
def reset_deck(deck):
	rawdeck = []
	for i in range (0,4):
		for j in range(1,14):
			rawdeck.append(j)
	del deck[:]
	while rawdeck != []:
		# Note that when we pull a random card, we need to be careful to not let it pull from past the end of the remaining deck.
		i = random.randint(1,len(rawdeck))
		# We also take care to remove the cards that we've already moved into the new deck, so we don't get an irregular deck.
		deck.append(rawdeck.pop(i-1))

		
# The second support function determines the playing strategies available. It is responsible for taking the two players' play piles and adding them to the winner's deck.
def take_loot(playstyle,selfloot,otherloot,playerdeck):
	# The first sorts the whole pile of cards in ascending order.
	if playstyle == 0:
		loot = selfloot + otherloot
		loot.sort()
		playerdeck.extend(loot)
	# The second sorts the whole pile, and then reverses it.
	elif playstyle == 1:
		loot = selfloot + otherloot
		loot.sort()
		loot.reverse()
		playerdeck.extend(loot)
	# The third simply adds the victors' cards, and then their opponents'.
	elif playstyle == 2:
		loot = selfloot + otherloot
		playerdeck.extend(loot)
	# The fourth simply adds the oppenents' cards before the victors'.
	elif playstyle == 3:
		loot = otherloot + selfloot
		playerdeck.extend(loot)
	# The fifth adds them randomly.
	elif playstyle == 4:
		loot = otherloot + selfloot
		while (loot != []):
			i = random.randint(1,len(loot))
			playerdeck.append(loot.pop(i-1))

# Support code out of the way, we initialize the two players' decks, and their respective play stacks.			
player1 = []
player2 = []
warstack1 = []
warstack2 = []
turnsrecord = []
warsrecord = []

# The actual playing is a series of nested while loops. The outer one represents full games played, and counts up until the requested number of games have been played.
while (wins1+wins2) < gamestoplay:
	# At the beginning of each game, the decks should be shuffled, and the turn counter should be set to 0.
	reset_deck(player1)
	reset_deck(player2)
	turns = 0
	wars = 0
	# The first nested while loop accounts for turns of the game. Turns will continue to be played until one of the decks is empty, thereby crowning a victor.
	# Alternatively, games end by running too long. This is due to the fact that infinite games of war do very much exist. The longest games of war tend to last around 10,000 turns,
	# so 50,000 is a safe cap.
	while ((player1 != []) and (player2 != [])) and turns < 50000:
		turns += 1
		# At the beginning of each turn, the play stacks are reset, and then the top cards of the players decks are played.
		del warstack1[:]
		del warstack2[:]
		warstack1.append(player1.pop(0))
		warstack2.append(player2.pop(0))
		# The code then checks to see if we have a WAR!. If so, it adds three more cards to the stack, in the correct playing order, and checks again until the cards are different.
		# Note that if one of the players has too few cards, this code does not produce an error. In fact, it will draw as many cards as it can, and do no more, which is consistent
		# with the rules of WAR! That is to say, if a player runs out of cards, their final card represents their active combatant, while the other player continues to play cards.
		while warstack1[-1]== warstack2[-1]:
			wars += 1
			warstack1.extend(player1[0:4])
			del player1[0:4]
			warstack2.extend(player2[0:4])
			del player2[0:4]
		# Once a victor is determined, they take the spoils, which is handled in the support code take_loot.
		if warstack1[-1] > warstack2[-1]:
			take_loot(style1,warstack1,warstack2,player1)
		else:
			take_loot(style2,warstack2,warstack1,player2)
	# Once the above while loop terminates, it means the game is "over". If the turn tracker is less than 50,000, someone has won and gets a point.
	if turns < 50000:
		if player1 == []:
			wins1 += 1
		else:
			wins2 += 1
		# For each game, we also print a "progress bar" that shows the two players' winning precentages using + signs.
		turnsrecord.append(turns)
		warsrecord.append(wars)
		print("+"*round(40*wins1/(wins1+wins2)),"+"*round(40*wins2/(wins1+wins2)),wins1+wins2,"games complete.")
	# If the turn tracker was over 50,000, we found an infinite game.
	else:
		infinitegames += 1
		print("Woah, nelly! An infinite game!",infinitegames,"infinite games found.")

# Finally, we print the statistics, and finish.
print ("\nGames complete. Final tally:")
print ("Player 1:",wins1,"   ","Player 2:",wins2,"Infinite Games:","   ",infinitegames,"\n")
print ("Average number of turns in finite games:",sum(turnsrecord)/float(len(turnsrecord)))
print ("Greatest number of turns  in a game:", max(turnsrecord),"Least:",min(turnsrecord),"\n")
print ("Average number of wars in finite games:",sum(warsrecord)/float(len(warsrecord)))
print ("Greatest number of wars in a game:", max(warsrecord),"Least:",min(warsrecord))
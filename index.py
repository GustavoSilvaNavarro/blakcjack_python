import random

#! CREATING CARD CLASS
class Card:
  def __init__(self, suit, rank):
    self.suit = suit
    self.rank = rank

  def __str__(self): #* Way to print stuff
    return f'{self.rank["rank"]} of {self.suit}'

#! CREATE A DECK CLASS
class Deck:
  def __init__(self):
    self.cards = [];
    suits = ['spades', 'clubs', 'hearts', 'diamonds']
    ranks = [
      { 'rank': '2', 'value': 2 },
      { 'rank': '3', 'value': 3 },
      { 'rank': '4', 'value': 4 },
      { 'rank': '5', 'value': 5 },
      { 'rank': '6', 'value': 6 },
      { 'rank': '7', 'value': 7 },
      { 'rank': '8', 'value': 8 },
      { 'rank': '9', 'value': 9 },
      { 'rank': '10', 'value': 10 },
      { 'rank': 'J', 'value': 10 },
      { 'rank': 'Q', 'value': 10 },
      { 'rank': 'K', 'value': 10 },
      { 'rank': 'A', 'value': 11 }
    ]

    for suit in suits:
      for rank in ranks:
        self.cards.append(Card(suit, rank))

  # SHUFFLING THE DECK
  def shuffle(self):
    if len(self.cards) > 0:
      random.shuffle(self.cards)

  # Dealing a card from the deck
  def deal(self, number):
    cards_dealt = []
    for i in range(number):
      if len(self.cards) > 0:
        cards_dealt.append(self.cards.pop())

    return cards_dealt

#? HAND CLASS
class Hand:
  def __init__(self, dealer = False):
    self.cards = []
    self.value = 0
    self.dealer = dealer

  def addCard(self, cardList):
    self.cards.extend(cardList)

  def calculateValue(self):
    self.value = 0
    hasAce = False

    for card in self.cards:
      cardValue = int(card.rank['value'])
      self.value += cardValue

      if card.rank['rank'] == 'A':
        hasAce = True

    if hasAce and self.value > 21:
      self.value -= 10

  def getValue(self):
    self.calculateValue()
    return self.value

  def isBlackjack(self):
    return self.getValue() == 21

  def display(self, showDealerCards = False):
    print(f'''{"Dealer's" if self.dealer else "Your"} hand:''')
    for index, card in enumerate(self.cards): # enumerate to access index and item
      if index == 0 and self.dealer and not showDealerCards and not self.isBlackjack():
        print('hidden')
      else:
        print(card)

    if not self.dealer:
      print(f'Value: {self.getValue()}')

    print()

#? GAME CLASS
class Game:
  def play(self):
    gameNumber = 0
    gameToPlay = 0

    while gameToPlay <= 0:
      try:
        gameToPlay = int(input('How many games do you want to play?'))
      except:
        print('You must enter a number')

    while gameNumber < gameToPlay:
      gameNumber += 1

      deck = Deck()
      deck.shuffle()

      playerHand = Hand()
      dealerHand = Hand(True)

      for i in range(2):
        playerHand.addCard(deck.deal(1))
        dealerHand.addCard(deck.deal(1))

      print()
      print('*' * 30)
      print(f'Game {gameNumber} of {gameToPlay}')
      print('*' * 30)
      playerHand.display()
      dealerHand.display()

      if self.checkWinner(playerHand, dealerHand):
        continue

      choice = ''
      while playerHand.getValue() < 21 and choice not in ['s', 'stand']:
        choice = input("Please choose 'Hit' or 'Stand': ").lower()
        print()

        while choice not in ['h', 's', 'hit', 'stand']:
          choice = input("Please enter 'Hit' or 'Stand' (or H/S) ").lower()
          print()

        if choice in ['h', 'hit']:
          playerHand.addCard(deck.deal(1))
          playerHand.display()

      if self.checkWinner(playerHand, dealerHand):
        continue

      playerHandValue = playerHand.getValue()
      dealerHandValue = dealerHand.getValue()

      while dealerHandValue < 17:
        dealerHand.addCard(deck.deal(1))
        dealerHandValue = dealerHand.getValue()

      dealerHand.display(True)

      if self.checkWinner(playerHand, dealerHand):
        continue

      print('Final Results')
      print(f'Your hand: {playerHandValue}')
      print(f"Dealer's hand: {dealerHandValue}")

      self.checkWinner(playerHand, dealerHand, True)

    print('\nThanks for playing!')

  def checkWinner(self, playerHand, dealerHand, gameIsOver = False):
    if not gameIsOver:
      if playerHand.getValue() > 21:
        print('You busted. Dealer wins! 😭')
        return True
      elif dealerHand.getValue() > 21:
        print('Dealer busted. You win! 😊')
        return True
      elif dealerHand.isBlackjack() and playerHand.isBlackjack():
        print('Both players have Blackjack! Tie! 🙄')
        return True
      elif playerHand.isBlackjack():
        print('You have Blackjack!. You win! 😊')
        return True
      elif dealerHand.isBlackjack():
        print('Dealer have Blackjack!. Dealers win! 😭')
        return True
    else:
      if playerHand.getValue() > dealerHand.getValue():
        print('You win! 😊')
      elif playerHand.getValue() == dealerHand.getValue():
        print('Tie! 🙄')
      else:
        print('Dealers wins! 😭')
      return True
    return False

g = Game()
g.play()
Yi Xian Simulator
===================

This is a mock game engine for [Yi Xian: The Cultivation Card Game](https://store.steampowered.com/app/1948800/Yi_Xian_The_Cultivation_Card_Game/).


Code Examples
----------------

The majority of the game's logic is defined in the implementation of the cards which can be found in the [card logic](yxsim/cards/logic) folder.
The following will be examples of card implementations.

### Normal Attack

Here we are creating the [default card](yxsim/cards/logic/normal_attack.py) which does 3 damage when played.
The only import we need are `Card` which is the class that we inherit from and `Action` which is the class we use to define and execute logic from.
We then define a `CardType` class which is the required name needed for these implementation files.
For display purposes we define an `id` variable to the class.
The actual logic then gets implemented with the `play` function which needs to return a boolean value to show if the card was played successfully or not.
Finally we create an `Action` with `source` as the attacker and `target` as the defender and a `damage` value of 3.
We then return the boolean value from the `execute` method to show if the card was played successfully or not.

```python
from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect


class CardType(Card):
    display_name = 'Normal Attack'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(card=self, source=attacker, target=defender, damage=3).execute()
```

### Card That Change Resources

As an example of cards that change resources we will use [Guard Qi](yxsim/cards/logic/guard_qi.py) as an example.
In addition to our default imports we also need to import [Resource](yxsim/resources.py) to have access to the various `Resource` Enum.
We then define an `Action` with `resource_changes` to a dict where the keys are `Resource` and values are `int`.
This will then be used to update the `resources` attribute on the `Player`.

```python
from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Resource, Sect


class CardType(Card):
    display_name = 'Guard Qi'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={
                Resource.DEF: 5, Resource.QI: 1
            }
        ).execute()
```

### Attack with Injured

Here we look at the card [Thunder Sword](yxsim/cards/logic/thunder_sword.py) which does 5 damage and if that damage injures the target it does an additional 6 damage.
To get that functionality we create our `Action` with 5 damage and then specify the `injured_action` to a new `Action` which does 6 damage.
We can then simply call the `execute` method on the top `Action`.

```python
from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect


class CardType(Card):
    display_name = 'Thunder Sword'
    phase = 1
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=5,
            injured_action=Action(card=self, source=attacker, target=defender, damage=6)
        ).execute()
```

### Continuous Cards

We will be using [Cloud Citta Dharma](yxsim/cards/logic/cloud_citta_dharma.py) as an example of how to implement a continuous card.
First, separately from the `CardType` definition we need to make our listener using the base `OnPlayCard`.
Second, that class needs to override the function `handle` which will contain all of it's functionality.
For this specific card we only need to check if the card played has `cloud_sword` equal to `True` and if that is the case we make an `Action` to heal the player for 2.
It is important to note that in the `Action` we are passing `card=self.source_card` as this value will reference the `Cloud Citta Dharma` card.
After defining our listener we can create the `CardType` and within the play function we simply call the `add_listener` function from the attacker and pass in a `CloudCittaDHarmaOnPlayCard` object.
To note, we will also need to set `exhausted` to `True` and return `True` to say that the card was successfully played.

```python
from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect
from yxsim.events import OnPlayCard


class CloudCittaDharmaOnPlayCard(OnPlayCard):
    def handle(self, card: Card, attacker: Player, defender: Player, **kwargs):
        if card.cloud_sword is True:
            Action(card=self.source_card, source=attacker, target=attacker, healing=2).execute()


class CardType(Card):
    display_name = 'Cloud Citta Dharma'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        self.exhausted = True
        attacker.add_listener(CloudCittaDharmaOnPlayCard(self, priority=0))
        return True
```
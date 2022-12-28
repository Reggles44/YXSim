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


class CardType(Card):
    display_name = 'Normal Attack'

    def play(self, attacker: 'Player', defender: 'Player', **kwargs) -> bool:\n        return Action(card=self, source=attacker, target=defender, damage=3).execute()
```

### Card That Change Resources

As an example of cards that change resources we will use [Guard Qi](yxsim/cards/logic/guard_qi.py) as an example.
In addition to our default imports we also need to import [Resource](yxsim/resources.py) to have access to the various `Resource` Enum.
We then define an `Action` with `resource_changes` to a dict where the keys are `Resource` and values are `int`.
This will then be used to update the `resources` attribute on the `Player`.

```python
from yxsim.resources import Resource
from yxsim.action import Action
from yxsim.cards.base import Card


class CardType(Card):
    display_name = 'Guard Qi'

    def play(self, attacker, **kwargs) -> bool:
        return Action(
            card=self, source=attacker,
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


class CardType(Card):
    display_name = 'Thunder Sword'

    def play(self, attacker: 'Player', defender: 'Player', **kwargs) -> bool:\n        return Action(
            card=self, source=attacker,
            target=defender,
            damage=5,
            injured_action=Action(card=self, source=attacker, target=defender, damage=6)
        ).execute()
```
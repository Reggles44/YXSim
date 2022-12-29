Yi Xian Simulator
===================

This is a mock game engine for [Yi Xian: The Cultivation Card Game](https://store.steampowered.com/app/1948800/Yi_Xian_The_Cultivation_Card_Game/).


Code Examples
----------------

The majority of the game's logic is defined in the implementation of the cards which can be found in the [card logic](yxsim/cards/logic) folder.
The following will be examples of card implementations.

### Defining a Card

To explain the method to define a card we will use the example of [Normal Attack](yxsim/cards/logic/normal_attack.py) which does 3 damage when played.
A card is defined by a `CardType` class which needs to inherit from `Card`.
The actual logic then gets implemented with the `play` function which needs to return a boolean value to show if the card was played successfully or not.
Within the `play` function most logic can be defined within an `Action` object and then `executed` to preform the changes defined.
Finally, the `execte` function will return a boolean if it was successful which should then be returned from the `play` function.

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
        return Action(
            card=self, 
            source=attacker, 
            target=defender,
            damage=3
        ).execute()
```

### Resource Changes

Many cards also provide various [Resource](yxsim/resources.py) changes which is the basis for many combos.
As an example of a card the changes resources is [Guard Qi](yxsim/cards/logic/guard_qi.py) which provides 5 defense and 1 Qi.
When looking at the `play` function there is still an `Action` but this time it defines `resource_changes` as a dict of all resource changes to be done to the `target`.

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

### Nested Actions

`Actions` can also be nested to create more complex logic.
A simple example of nested `Action`s is [Thunder Sword](yxsim/cards/logic/thunder_sword.py) which does 5 damage and if that damage injures the target it does an additional 6 damage.
Similar to the previous example we can define an `Action` for the initial 5 damage.
It's then possible to pass in another `Action` into `injured_action` which will be executed on the `injured` condition is met.

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
            injured_action=Action(
                card=self,
                source=attacker, 
                target=defender,
                damage=6
            )
        ).execute()
```

Another example of `Action` nesting is [Flying Spirit Shade Sword](yxsim/cards/logic/flying_spirit_shade_sword.py) which does four attacks at one damage each and for each injured you gain 1 Qi.
This can be defined as an `Action` with `related_actions` as a list of the 4 attack `Action`s where each of those attacks has an `injured_action` to give 1 Qi.

```python
from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Flying Spirit Shade Sword'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(
                    card=self,
                    source=attacker,
                    target=defender,
                    damage=1,
                    injured_action=Action(
                        card=self,
                        source=attacker,
                        target=attacker,
                        resource_changes={Resource.QI: 1}
                    )
                ) for _ in range(4)
            ]
        ).execute()
```


### Reference Values

For some cards the value is not defined but a reference to something that will occur.
The example we will use is [Earth Evil Sword](yxsim/cards/logic/earth_evil_sword.py) which does 8 damage and if that injurs the opponent the attacker gains that much defense.
To start we can create the 8 damage `Action` and then define an `injured_action` for the defense gain.
We will then need to use [ReferenceValue](yxsim/util.py) to define that we will calculate that value later.
Importantly, the `ReferenceValue` will take a `callable` and that `callable` will need to return a value that makes the type of the field it's replacing.

```python
from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue


class CardType(Card):
    display_name = 'Earth Evil Sword'
    phase = 2
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=8,
            injured_action=Action(
                card=self, 
                source=attacker, 
                target=attacker, 
                resource_changes=ReferenceValue(
                    lambda parent: {Resource.DEF: parent.damage_to_health}
                )
            )
        ).execute()
```

### Continuous Cards

Some card also require creating a `continuous` effect such as [Cloud Citta Dharma](yxsim/cards/logic/cloud_citta_dharma.py) which heals the player everytime they play a `cloud_sword` card.
First, separately from the `CardType` definition we need to make our listener using the base `OnPlayCard`.
Second, that class needs to override the function `handle` which will contain all of its functionality.
For this specific card the logic will check if the card played has `cloud_sword` equal to `True` and if that is the case we make an `Action` to heal the player for 2.
It is important to note that in the `Action` the `card` is set to `self.source_card` as this value will reference the `Cloud Citta Dharma` object that created the listener.
Then within the `play` function the listener can be passed into the `add_listener` method on the `Player`.

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
        attacker.add_listener(CloudCittaDharmaOnPlayCard(source=attacker, source_card=self, priority=0))
        return Action(card=self, source=attacker, target=attacker).execute()
```
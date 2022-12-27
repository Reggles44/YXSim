from yxsim.config import configure_logging
from yxsim.cards.logic import registry as card_registry
from yxsim.characters.logic import registry as character_registry
from yxsim.destinies.logic import registry as destiny_registry
from yxsim.stats.logic import registry as stat_registry

configure_logging()
card_registry.autoregister()
character_registry.autoregister()
destiny_registry.autoregister()
stat_registry.autoregister()
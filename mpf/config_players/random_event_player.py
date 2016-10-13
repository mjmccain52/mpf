"""Random event config player."""
import random

from mpf.core.config_player import ConfigPlayer
from mpf.core.randomizer import Randomizer
from mpf.core.utility_functions import Util


class RandomEventPlayer(ConfigPlayer):

    """Plays a random event based on config."""

    config_file_section = 'random_event_player'
    show_section = 'random_events'
    device_collection = None

    def __init__(self, machine):
        super().__init__(machine)
        self._machine_wide_dict = {}

    def _get_randomizer(self, settings, context, calling_context):
        key = "random_{}.{}".format(context, calling_context)
        if settings['scope'] == "player":
            if not self.machine.game.player[key]:
                self.machine.game.player[key] = Randomizer(settings['events'])
            return self.machine.game.player[key]
        else:
            if key not in self._machine_wide_dict:
                self._machine_wide_dict[key] = Randomizer(settings['events'])
            return self._machine_wide_dict[key]

    def play(self, settings, context, calling_context, priority=0, **kwargs):
        """Play a random event from list based on config."""
        del priority
        randomizer = self._get_randomizer(settings, context, calling_context)
        next = randomizer.get_next()
        self.machine.events.post(next, **kwargs)

    def validate_config_entry(self, settings, name):
        """Validate one entry of this player."""
        config = self._parse_config(settings, name)
        return config

    def get_express_config(self, value):
        """Parse express config."""
        return {"events": self.get_list_config(Util.string_to_list(value))}

    def get_list_config(self, value):
        """Parse list."""
        return {"events": value}


player_cls = RandomEventPlayer

from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

from .actions.Stopwatch.Stopwatch import Stopwatch

class StopwatchPlugin(PluginBase):
    def __init__(self):
        super().__init__()

        self.stopwatch_holder = ActionHolder(
            plugin_base=self,
            action_base=Stopwatch,
            action_id_suffix="Stopwatch",
            action_name="Stopwatch",
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.stopwatch_holder)

        self.register()

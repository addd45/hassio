from area import Area
from globals import GlobalEvents, HouseModes
import datetime
'''
Implements melkers room specific automations

Use-cases:

- Turn off tv att nigt by turn off the power of the chromecast and use TV built in 
  power savings (not have remote in that room)

'''
class MelkersRoom(Area):
    def initialize(self) -> None:
        super().initialize()

        self._tv_switch = self.properties.get('tv_switch', str)
        self._minutes_before_turn_on_switch = int(self.properties.get('minutes_before_turn_on_switch', 8))
        self._time_to_turn_off_tv = datetime.datetime.strptime(self.properties['time_to_turn_off_tv'], "%H:%M:%S") 

        
        # Set callback when it is nighttime on days when go to bed late
        self.run_daily(
            self.__on_time_for_turn_off_tv,
            self._time_to_turn_off_tv.time()
            )

    def __on_time_for_turn_off_tv(self, kwargs: dict) -> None:
        """Time to set the house mode to day."""
        self.log("TURN OFF MELKERS TV")
        self.turn_off(self._tv_switch)

        self.run_in(self.__on_time_for_turn_on_tv, self._minutes_before_turn_on_switch*60) #*60
 
    def __on_time_for_turn_on_tv(self, kwargs: dict) -> None:
        self.log("TURN ON MELKERS TV")
        self.turn_on(self._tv_switch)
        
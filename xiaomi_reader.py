from mitemp_bt_poller import MiTempBtPoller
from btlewrap.gatttool import GatttoolBackend

poller = MiTempBtPoller('58:2D:34:38:3C:E2', GatttoolBackend)

print(poller.parameter_value("temperature"))
print(poller.parameter_value("humidity"))
print(poller.parameter_value("battery"))

from thebest.common.start_service_command import StartServiceCommand
from thebest.application import APPLICATION


class Service1Command(StartServiceCommand):  # pylint: disable=too-few-public-methods
    DEFAULT_PORT = 10001

    def __init__(self, app, app_args):
        super(Service1Command, self).__init__(app, app_args, APPLICATION)

    def get_description(self):
        return "the best"

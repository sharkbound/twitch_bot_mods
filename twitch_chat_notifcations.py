from threading import Thread
from queue import Queue, Empty

from twitchbot import Mod, Message, CONFIG_FOLDER, Config

try:
    from win10toast import ToastNotifier
except (ImportError, ModuleNotFoundError):
    print(
        'cannot find windows 10 toast notification library\nplease install it via pip:\n\tpip install --user --upgrade win10toast')
    exit(1)

notifier_cfg = Config(
    CONFIG_FOLDER / 'notifier_settings.json',
    title='Twitch',
    duration=3
)


class Notifier(Mod):
    name = 'notifier'

    async def loaded(self):
        self.queue = Queue()
        self.thread = Thread(target=self._notification_loop)
        self.toast = ToastNotifier()
        self.running = True

        self.thread.start()

    async def unloaded(self):
        self.kill_thread()

    def kill_thread(self):
        self.running = False

    def _notification_loop(self):
        while self.running:
            try:
                msg: Message = self.queue.get(block=True, timeout=5)
            except Empty:
                continue
            self.toast.show_toast(notifier_cfg.title, f'[{msg.channel_name}] {msg.author}: {msg.content}',
                                  duration=notifier_cfg.duration)

    async def on_privmsg_received(self, msg: Message):
        self.queue.put(msg)

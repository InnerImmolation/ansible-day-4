from __future__ import absolute_import
from ansible.plugins.callback import CallbackBase
from ansible.utils.color import colorize, hostcolor
import os
import datetime


class CallbackModule(CallbackBase):
    '''
    This is the default callback interface, which simply prints messages
    to stdout when new callback events are received.
    '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'demo'
    CALLBACK_NEEDS_WHITELIST = True

    module_name = ""

    def show(self, task, host, result, color):
        if self.module_name != "setup":
            res = {}
            for key, value in result.iteritems():
                if key[0] != "_" and key not in ["invocation"]:
                    res.update({
                        key: value
                    })
            self._display.display("{}[{}] | TASK: {} | VM: {} | {} | rc={} {}".format(
                color, str(datetime.datetime.now()),
                task._attributes.get("name", "name"), host, res.get('msg'), res.get('rc'), '\033[37m'
            ))
        else:
            self._display.display("{}{} => ok".format(color, host))

    def v2_playbook_on_start(self, playbook):
        print("[{}] | {}PLAYBOOK STARTED {}{}\nFILENAME: {}/{}\n".format(
            str(datetime.datetime.now()), '\033[32m', ">" * 31, '\033[37m', os.getcwd(), playbook._file_name
        ))

    def v2_playbook_on_play_start(self, play):
        print("{}[{}] | PLAY: '{}'\n".format('\033[34m', str(datetime.datetime.now()), play.name))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.show(result._task, result._host.get_name(), result._result, '\033[31m')
        if ignore_errors:
            self._display.display("...ignoring", '\033[31m')
        print("")

    def v2_runner_on_ok(self, result):
        self.show(result._task, result._host.get_name(), result._result, '\033[32m')
        print("")

    def v2_runner_on_skipped(self, result):
        self.show(result._task, result._host.get_name(), result._result, '\033[34m')
        print("")

    def v2_runner_on_unreachable(self, result):
        self.show(result._task, result._host.get_name(), result._result, '\033[31m')
        print("")

    def v2_playbook_on_stats(self, stats):
        print("{}[{}] | PLAYBOOK SUMMARY {}{}\n".format('\033[34m', str(datetime.datetime.now()), ">" * 31, '\033[37m',))

        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)

            self._display.display(u"%s : %s %s %s %s" % (
                hostcolor(h, t),
                colorize(u'ok', t['ok'], 'purple'),
                colorize(u'changed', t['changed'], 'blue'),
                colorize(u'unreachable', t['unreachable'], 'red'),
                colorize(u'failed', t['failures'], 'red')),
                                  screen_only=True
                                  )

            self._display.display(u"%s : %s %s %s %s" % (
                hostcolor(h, t, False),
                colorize(u'ok', t['ok'], 'green'),
                colorize(u'changed', t['changed'], None),
                colorize(u'unreachable', t['unreachable'], None),
                colorize(u'failed', t['failures'], None)),
                                  log_only=True
                                  )

        self._display.display("", screen_only=True)


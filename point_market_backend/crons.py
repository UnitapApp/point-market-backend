from django_cron import CronJobBase, Schedule

from market.management.commands.run_market import RunMarket
from core.management.commands.pull_zellular import PullZellular
from symbol.management.commands.scan import Scan


class MarketJob(CronJobBase):
    RUN_EVERY_MINS = 1  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'market'  # a unique code

    def do(self):
        RunMarket.run(0)


class ScanJob(CronJobBase):
    RUN_EVERY_MINS = 10  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'scan'  # a unique code

    def do(self):
        Scan.run()


class ZellularJob(CronJobBase):
    RUN_EVERY_MINS = 1  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'zellular'  # a unique code

    def do(self):
        PullZellular.perform()

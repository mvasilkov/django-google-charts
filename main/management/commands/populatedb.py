from datetime import datetime
from django.core.management.base import NoArgsCommand
from django.db.transaction import commit_on_success
from main.models import Payment
from random import randrange, uniform
from time import mktime

def any_amount():
    return str(uniform(2., 8.))

foo = mktime(datetime(2011, 1, 1).timetuple())
bar = mktime(datetime(2011, 4, 1).timetuple())

def any_datetime():
    return datetime.fromtimestamp(foo + randrange(bar - foo))

class Command(NoArgsCommand):
    @commit_on_success
    def handle_noargs(self, **options):
        for i in xrange(2400):
            Payment(amount=any_amount(), datetime=any_datetime()).save()
            self.stdout.write('.')
            self.stdout.flush()
        self.stdout.write('\n')

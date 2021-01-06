from django.core.management.base import BaseCommand, CommandError
import opml, feedparser
from django.contrib.auth.models import User
from myrss.models.subscription import Subscription

#sample opml file (download): https://raw.githubusercontent.com/microsoft/rss-reader-wp/master/RSSReader_WP7/sample-opml.xml

def _is_valid_rss_feed(url):
    if not url:
        return False
    try:
        news_feed = feedparser.parse(url)
    except:
        return False
    if news_feed.bozo:  # news_feed.bozo se setea cuando el parsing falla
        return False
    if not (news_feed.get('feed') and news_feed.get('feed').get('title')):
        return False
    return True

def _create_subscription_and_fetch_articles(user, url, name):
    with_this_link = Subscription.objects.filter(owner=user, link=url)
    if with_this_link.exists():
        return
    subscription = Subscription.objects.create(owner = user, link=url, name=name)
    subscription.save()
    subscription.get_last_articles()


class Command(BaseCommand):
    help = '''Imports OPML subscriptions to specified users. Use as:
    python manage.py importsubscriptions --subscriptions <opml file> --user_ids <userid> <userid> ... <userid>
    '''

    def add_arguments(self, parser):
        parser.add_argument('--subscriptions', nargs=1, help='link to subscription opml file')
        parser.add_argument('--user_ids', nargs='*', type=int, help='list of user ids')

    def handle(self, *args, **options):
        if options['subscriptions']:
            try:
                outline = opml.parse(options['subscriptions'][0])
            except:
                raise CommandError('Not a valid OPML file')
        else:
            raise CommandError('OPML file to import subscription is needed')
        if options['user_ids']:
            user_list = options['user_ids']
        else:
            user_list = [user.id for user in User.objects.all()]
        for user_id in user_list:
            self.stdout.write('Importing subscriptions for user %s' % user_id)
            try:
                user = User.objects.get(pk=user_id)
            except:
                raise CommandError('User "%s" does not exist' % user_id)
            for category in outline:
                if category:
                    category_title = category.title
                else:
                    category_title = "?"
                self.stdout.write('\tCategory: %s' % category_title)
                for entry in category:
                    self.stdout.write('\t\tSubscribing to: %s' % entry.title)
                    if _is_valid_rss_feed(entry.xmlUrl) and hasattr(entry, 'title'):
                        _create_subscription_and_fetch_articles(user, entry.xmlUrl, entry.title)
                        self.stdout.write(self.style.SUCCESS('\t\tSuccessfully suscribed user %s to %s' % (user_id, entry.title)))
                    else:
                        self.stdout.write(self.style.ERROR('\t\tCould not subscribe user %s to %s: not a valid rss feed' % (user_id, entry.title)))
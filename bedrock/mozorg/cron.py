# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import cronjobs
import feedparser
from django.conf import settings
from django.core.cache import cache

from bedrock.mozorg.util import TwitterAPI


@cronjobs.register
def update_feeds():
    for name, url in settings.FEEDS.items():
        feed_info = feedparser.parse(url)
        # Cache for a year (it will be set by the cron job no matter
        # what on a set interval)
        cache.set('feeds-%s' % name, feed_info, 60 * 60 * 24 * 365)


@cronjobs.register
def update_tweets():
    for account in settings.TWITTER_ACCOUNTS:
        try:
            tweets = TwitterAPI(account).user_timeline(screen_name=account)
        except:
            tweets = []

        # Cache for a year (it will be set by the cron job no matter
        # what on a set interval)
        cache.set('tweets-%s' % account, tweets, 60 * 60 * 24 * 365)

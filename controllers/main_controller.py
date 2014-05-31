import os
import logging
import datetime
import webapp2

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

import tba_config

from base_controller import CacheableHandler
from consts.event_type import EventType
from helpers.event_helper import EventHelper

from models.event import Event
from models.insight import Insight
from models.team import Team
from models.sitevar import Sitevar


def render_static(page):
    memcache_key = "main_%s" % page
    html = memcache.get(memcache_key)

    if html is None:
        path = os.path.join(os.path.dirname(__file__), "../templates/%s.html" % page)
        html = template.render(path, {})
        if tba_config.CONFIG["memcache"]:
            memcache.set(memcache_key, html, 86400)

    return html


class MainKickoffHandler(CacheableHandler):
    CACHE_VERSION = 3

    def __init__(self, *args, **kw):
        super(MainKickoffHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24
        self._cache_key = "main_kickoff"

    def _render(self, *args, **kw):
        kickoff_datetime_est = datetime.datetime(2014, 1, 4, 10, 30)
        kickoff_datetime_utc = kickoff_datetime_est + datetime.timedelta(hours=5)

        is_kickoff = datetime.datetime.now() >= kickoff_datetime_est - datetime.timedelta(days=1)  # turn on 1 day before

        path = os.path.join(os.path.dirname(__file__), "../templates/index_kickoff.html")
        return template.render(path, {'is_kickoff': is_kickoff,
                                      'kickoff_datetime_est': kickoff_datetime_est,
                                      'kickoff_datetime_utc': kickoff_datetime_utc,
                                      })


class MainBuildseasonHandler(CacheableHandler):
    CACHE_VERSION = 1

    def __init__(self, *args, **kw):
        super(MainBuildseasonHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_buildseason"

    def _render(self, *args, **kw):
        endbuild_datetime_est = datetime.datetime(2014, 2, 18, 23, 59)
        endbuild_datetime_utc = endbuild_datetime_est + datetime.timedelta(hours=5)

        path = os.path.join(os.path.dirname(__file__), "../templates/index_buildseason.html")
        return template.render(path, {'endbuild_datetime_est': endbuild_datetime_est,
                                      'endbuild_datetime_utc': endbuild_datetime_utc
                                      })


class MainChampsHandler(CacheableHandler):
    CACHE_VERSION = 1

    def __init__(self, *args, **kw):
        super(MainChampsHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24
        self._cache_key = "main_champs"

    def _render(self, *args, **kw):
        year = datetime.datetime.now().year
        event_keys = Event.query(Event.year == year, Event.event_type_enum.IN(EventType.CMP_EVENT_TYPES)).fetch(100, keys_only=True)
        events = [event_key.get() for event_key in event_keys]
        template_values = {
            "events": events,
        }

        insights = ndb.get_multi([ndb.Key(Insight, Insight.renderKeyName(year, insight_name)) for insight_name in Insight.INSIGHT_NAMES.values()])
        for insight in insights:
            if insight:
                template_values[insight.name] = insight

        path = os.path.join(os.path.dirname(__file__), '../templates/index_champs.html')
        return template.render(path, template_values)


class MainCompetitionseasonHandler(CacheableHandler):
    CACHE_VERSION = 5

    def __init__(self, *args, **kw):
        super(MainCompetitionseasonHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60
        self._cache_key = "main_competitionseason"

    def _render(self, *args, **kw):
        week_events = EventHelper.getWeekEvents()
        template_values = {
            "events": week_events,
        }

        path = os.path.join(os.path.dirname(__file__), '../templates/index_competitionseason.html')
        return template.render(path, template_values)


class MainInsightsHandler(CacheableHandler):
    CACHE_VERSION = 2

    def __init__(self, *args, **kw):
        super(MainInsightsHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24
        self._cache_key = "main_insights"

    def _render(self, *args, **kw):
        week_events = EventHelper.getWeekEvents()
        template_values = {
            "events": week_events,
        }

        insights = ndb.get_multi([ndb.Key(Insight, Insight.renderKeyName(2014, insight_name)) for insight_name in Insight.INSIGHT_NAMES.values()])
        for insight in insights:
            if insight:
                template_values[insight.name] = insight

        path = os.path.join(os.path.dirname(__file__), '../templates/index_insights.html')
        return template.render(path, template_values)


class MainOffseasonHandler(CacheableHandler):
    CACHE_VERSION = 2

    def __init__(self, *args, **kw):
        super(MainOffseasonHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24
        self._cache_key = "main_offseason"

    def _render(self, *args, **kw):
        week_events = EventHelper.getWeekEvents()
        template_values = {
            "events": week_events,
        }

        path = os.path.join(os.path.dirname(__file__), '../templates/index_offseason.html')
        return template.render(path, template_values)


class ContactHandler(CacheableHandler):
    CACHE_VERSION = 1

    def __init__(self, *args, **kw):
        super(ContactHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_contact"

    def _render(self, *args, **kw):
        path = os.path.join(os.path.dirname(__file__), "../templates/contact.html")
        return template.render(path, {})


class HashtagsHandler(CacheableHandler):
    CACHE_VERSION = 1

    def __init__(self, *args, **kw):
        super(HashtagsHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_hashtags"

    def _render(self, *args, **kw):
        path = os.path.join(os.path.dirname(__file__), "../templates/hashtags.html")
        return template.render(path, {})


class AboutHandler(CacheableHandler):
    CACHE_VERSION = 1

    def __init__(self, *args, **kw):
        super(AboutHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_about"

    def _render(self, *args, **kw):
        path = os.path.join(os.path.dirname(__file__), "../templates/about.html")
        return template.render(path, {})


class ThanksHandler(CacheableHandler):
    CACHE_VERSION = 1

    def __init__(self, *args, **kw):
        super(ThanksHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_thanks"

    def _render(self, *args, **kw):
        path = os.path.join(os.path.dirname(__file__), "../templates/thanks.html")
        return template.render(path, {})


class OprHandler(CacheableHandler):
    CACHE_VERSION = 1

    def __init__(self, *args, **kw):
        super(OprHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_opr"

    def _render(self, *args, **kw):
        path = os.path.join(os.path.dirname(__file__), "../templates/opr.html")
        return template.render(path, {})


class SearchHandler(webapp2.RequestHandler):
    def get(self):
        try:
            q = self.request.get("q")
            logging.info("search query: %s" % q)
            if q.isdigit():
                team_id = "frc%s" % q
                team = Team.get_by_id(team_id)
                if team:
                    self.redirect(team.details_url)
                    return None
            elif len(q) in {3, 4, 5}:  # event shorts are between 3 and 5 characters long
                year = datetime.datetime.now().year  # default to current year
                event_id = "%s%s" % (year, q)
                event = Event.get_by_id(event_id)
                if event:
                    self.redirect(event.details_url)
                    return None
        except Exception, e:
            logging.warning("warning: %s" % e)
        finally:
            self.response.out.write(render_static("search"))


class GamedayHandler(CacheableHandler):
    CACHE_VERSION = 1

    def __init__(self, *args, **kw):
        super(GamedayHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_gameday"

    def _render(self, *args, **kw):
        special_webcasts_future = Sitevar.get_by_id_async('gameday.special_webcasts')
        special_webcasts_temp = special_webcasts_future.get_result()
        if special_webcasts_temp:
            special_webcasts_temp = special_webcasts_temp.contents
        else:
            special_webcasts_temp = {}
        special_webcasts = []
        for webcast in special_webcasts_temp.values():
            toAppend = {}
            for key, value in webcast.items():
                toAppend[str(key)] = str(value)
            special_webcasts.append(toAppend)

        ongoing_events = []
        ongoing_events_w_webcasts = []
        week_events = EventHelper.getWeekEvents()
        for event in week_events:
            if event.within_a_day:
                ongoing_events.append(event)
                if event.webcast:
                    valid = []
                    for webcast in event.webcast:
                        if 'type' in webcast and 'channel' in webcast:
                            event_webcast = {'event': event}
                            valid.append(event_webcast)
                    # Add webcast numbers if more than one for an event
                    if len(valid) > 1:
                        count = 1
                        for event in valid:
                            event['count'] = count
                            count += 1
                    ongoing_events_w_webcasts += valid

        template_values = {'special_webcasts': special_webcasts,
                           'ongoing_events': ongoing_events,
                           'ongoing_events_w_webcasts': ongoing_events_w_webcasts}

        path = os.path.join(os.path.dirname(__file__), '../templates/gameday.html')
        return template.render(path, template_values)


class PageNotFoundHandler(webapp2.RequestHandler):
    def get(self, *args):
        self.error(404)
        self.response.out.write(render_static("404"))


class WebcastsHandler(CacheableHandler):
    CACHE_VERSION = 2

    def __init__(self, *args, **kw):
        super(WebcastsHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_webcasts"

    def _render(self, *args, **kw):
        year = datetime.datetime.now().year
        event_keys = Event.query(Event.year == year).order(Event.start_date).fetch(500, keys_only=True)
        events = ndb.get_multi(event_keys)

        template_values = {
            'events': events,
            'year': year,
        }

        path = os.path.join(os.path.dirname(__file__), '../templates/webcasts.html')
        return template.render(path, template_values)


class RecordHandler(CacheableHandler):
    CACHE_VERSION = 1

    def __init__(self, *args, **kw):
        super(RecordHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_record"

    def _render(self, *args, **kw):
        path = os.path.join(os.path.dirname(__file__), "../templates/record.html")
        return template.render(path, {})


class ApiDocumentationHandler(CacheableHandler):
    CACHE_VERSION = 1

    def __init__(self, *args, **kw):
        super(ApiDocumentationHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "api_docs"

    def _render(self, *args, **kw):
        path = os.path.join(os.path.dirname(__file__), "../templates/apidocs.html")
        return template.render(path, {})

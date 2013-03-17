# coding: utf-8
#
# Copyright 2013 Foo Bar
# Powered by cyclone
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import cyclone.escape
import cyclone.locale
import cyclone.web
import cyclone.sse

from twisted.internet import defer
from twisted.python import log

from deck.storage import DatabaseMixin
from deck.utils import BaseHandler
from deck.utils import TemplateFields


class IndexHandler(BaseHandler):
    def get(self):
        self.render("template.html", mode = "index")

class ControlHandler(BaseHandler):
    def get(self):
        self.render("template.html", mode = "control")


class Dispatcher(DatabaseMixin):
    audience = []

    def subscribe(self, c):
        self.audience.append(c)

    def unsubscribe(self, c):
        self.audience.remove(c)

    def broadcast(self, message):
        for eyes in Dispatcher.audience:
            eyes.sendEvent(message)

    def presence_count(self):
        r = len(self.audience)
        return r

class PresenceHandler(BaseHandler, Dispatcher):
    def get(self):
        r = self.presence_count()
        self.write("%s" % r)

class CurrentSlideHandler(BaseHandler, Dispatcher):
    @defer.inlineCallbacks
    def get(self):
        r = yield self.redis.get("CURRENT_SLIDE")
        self.write(r)

    @defer.inlineCallbacks
    def post(self):
        par = {}
        par['indexh'] = self.get_argument('indexh', None)
        par['indexv'] = self.get_argument('indexv', None)
        if par['indexv'] is not None and par['indexh'] is not None:
            p = cyclone.escape.json_encode(par)
            yield self.redis.set("CURRENT_SLIDE", p)
            self.broadcast(p)


class LiveHandler(cyclone.sse.SSEHandler, Dispatcher):
    def bind(self):
        self.subscribe(self)

    def unbind(self):
        self.unsubscribe(self)


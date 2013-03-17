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


import cyclone.locale
import cyclone.web

from deck import views
from deck import config
from deck.storage import DatabaseMixin


class Application(cyclone.web.Application):
    def __init__(self, config_file):
        conf = config.parse_config(config_file)
        static_path = conf["static_path"]

        handlers = [
            (r"/",              views.IndexHandler),
            (r"/control",       views.ControlHandler),
            (r"/event/presence",     views.PresenceHandler),
            (r"/event/live",     views.LiveHandler),
            (r"/event/currentslide",     views.CurrentSlideHandler),
            (r"/css/(.+)", cyclone.web.StaticFileHandler,
                {"path": "%s/css" % static_path}),
            (r"/img/(.+)", cyclone.web.StaticFileHandler,
                {"path": "%s/img" % static_path}),
            (r"/js/(.+)", cyclone.web.StaticFileHandler,
                {"path": "%s/js" % static_path}),
            (r"/font/(.+)", cyclone.web.StaticFileHandler,
                {"path": "%s/font" % static_path}),
            (r"/lib/(.+)", cyclone.web.StaticFileHandler,
                {"path": "%s/lib" % static_path}),
            (r"/plugin/(.+)", cyclone.web.StaticFileHandler,
                {"path": "%s/plugin" % static_path}),
        ]


        # Initialize locales
        if "locale_path" in conf:
            cyclone.locale.load_gettext_translations(conf["locale_path"],
                                                     "deck")

        # Set up database connections
        DatabaseMixin.setup(conf)

        #conf["login_url"] = "/auth/login"
        #conf["autoescape"] = None
        cyclone.web.Application.__init__(self, handlers, **conf)

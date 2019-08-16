# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.events import Events
import os

from uploaders import *

class CloudTimelapsePlugin(
        octoprint.plugin.SettingsPlugin,octoprint.plugin.EventHandlerPlugin,octoprint.plugin.TemplatePlugin, octoprint.plugin.RestartNeedingPlugin):

    @property
    def api_token(self):
        return self._settings.get(['api_token'])

    @property
    def cloud_provider(self):
        return self._settings.get(['cloud_provider'])

    @property
    def delete_after_upload(self):
        return self._settings.get_boolean(['delete_after_upload'])

    ##~~ SettingsPlugin mixin
    
    def get_settings_defaults(self):
        return dict(
            api_token = None,
            cloud_provider = 'dropbox'
            delete_after_upload = False
        )

    def get_settings_restricted_paths(self):
        return dict(
            admin=[['api_token'], ]
        )

    def get_template_configs(self):
        return [
            dict(type ='settings', custom_bindings = False, template ='cloud_timelapse_settings.jinja2')
        ]

    ##~~ Software update hook
    
    def get_update_information(self):
        return dict(
            dropbox_timelapse=dict(
                displayName="Cloud Timelapse Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="digitalfrost",
                repo="OctoPrint-Cloud-Timelapse",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/digitalfrost/OctoPrint-Cloud-Timelapse/archive/{target_version}.zip"
            )
        )

 __plugin_name__ = "Cloud Timelapse Plugin"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = CloudTimelapsePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }   
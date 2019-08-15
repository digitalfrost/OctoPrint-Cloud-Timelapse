# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.events import Events
import os

class CloudTimelapsePlugin(
        octoprint.plugin.SettingsPlugin,octoprint.plugin.EventHandlerPlugin,octoprint.plugin.TemplatePlugin, octoprint.plugin.RestartNeedingPlugin):


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
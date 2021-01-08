#!/usr/bin/env python

"""
This is a test for remotely populating the Jenkins CreatePackageVFX20 form and starting a build
"""

import argparse
from getpass import getpass
import logging
import os
import pprint

import jenkins  # pip install python-jenkins


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server", required=False, default="https://jenkins-staging.thefoundry.co.uk"
    )
    parser.add_argument("--job", required=False, default="CreatePackageVFX2020Staging")
    parser.add_argument("--user", required=True)
    parser.add_argument("--recipe-dir", required=True)
    args = parser.parse_args()

    server = jenkins.Jenkins(
        args.server,
        username=args.user,
        password=getpass(prompt=f"Jenkins password for {args.user}: "),
    )
    user = server.get_whoami()
    version = server.get_version()
    logging.debug("Hello %s from Jenkins %s", user["fullName"], version)

    """
           'vcs_type=git\n'
           'vcs_path=\n'
           'vcs_reference=\n'
           'conan_recipe_path=\n'
           'build_versions=\n'
           'vfx_platform=vfx20\n'
           'linux_release=true\n'
           'mac_release=true\n'
           'win_release=true\n'
           'linux_debug=true\n'
           'mac_debug=true\n'
           'win_debug=true\n'
           'linux_label=\n'
           'mac_label=\n'
           'win_label=\n'
           'skip_conan_upload=false\n'
           'conan_user=common\n'
           'conan_channel=development\n'
           'conan_options=\n'
           'lifetime=\n'
           'conan_short_paths=false\n'
           'conan_config_branch=master\n'
           'test_folder=\n'
           'linux_short_paths=false\n'
           'disable_ccache=true\n'
           'disable_clcache_direct_mode=false\n'
           'use_spawned_vms=true\n'
           'p4_shelf=\n'
           'build_timeout=360\n'
           'verify_channels=true\n'
           'use_revisions=true',
    """
    params = {
        "skip_conan_upload": "true",
        "vcs_type": "git",
        "vcs_path": "git@gitlab.thefoundry.co.uk:libraries/conan/recipes.git",
        "conan_recipe_path": args.recipe_dir,
    }
    queue_item_number = server.build_job(args.job, parameters=params)
    queued_item = server.get_queue_item(queue_item_number)
    logging.debug("Queued job: %s", pprint.pformat(queued_item, compact=True))


if __name__ == "__main__":
    logging.getLogger().setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
    _main()

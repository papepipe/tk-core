# Copyright (c) 2016 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from ..errors import ShotgunDeployError
from .. import constants
from .. import util
log = util.get_shotgun_deploy_logger()

def create_io_descriptor(sg, descriptor_type, dict_or_uri, bundle_cache_root, fallback_roots):
    """
    Factory method. Use this method to construct all DescriptorIO instances.

    :param sg: Shotgun connection to associated site
    :param descriptor_type: Either AppDescriptor.APP, CORE, ENGINE or FRAMEWORK
    :param dict_or_uri: A std descriptor dictionary dictionary or string
    :param bundle_cache_root: Root path to where downloaded apps are cached
    :param fallback_roots: List of immutable fallback cache locations where
                           apps will be searched for. Note that when descriptors
                           download new content, it always ends up in the
                           bundle_cache_root.
    :returns: Descriptor object
    """
    from .base import IODescriptorBase
    from .appstore import IODescriptorAppStore
    from .dev import IODescriptorDev
    from .path import IODescriptorPath
    from .shotgun_entity import IODescriptorShotgunEntity
    from .git_tag import IODescriptorGitTag
    from .git_branch import IODescriptorGitBranch
    from .manual import IODescriptorManual

    if isinstance(dict_or_uri, basestring):
        # translate uri to dict
        descriptor_dict = IODescriptorBase.dict_from_uri(dict_or_uri)
    else:
        descriptor_dict = dict_or_uri

    if descriptor_dict.get("type") == "app_store":
        descriptor = IODescriptorAppStore(descriptor_dict, sg, descriptor_type)

    elif descriptor_dict.get("type") == "shotgun":
        descriptor = IODescriptorShotgunEntity(descriptor_dict, sg)

    elif descriptor_dict.get("type") == "manual":
        descriptor = IODescriptorManual(descriptor_dict)

    elif descriptor_dict.get("type") == "git":
        descriptor = IODescriptorGitTag(descriptor_dict)

    elif descriptor_dict.get("type") == "git_branch":
        descriptor = IODescriptorGitBranch(descriptor_dict)

    elif descriptor_dict.get("type") == "dev":
        descriptor = IODescriptorDev(descriptor_dict)

    elif descriptor_dict.get("type") == "path":
        descriptor = IODescriptorPath(descriptor_dict)

    else:
        raise ShotgunDeployError("Unknown descriptor type for '%s'" % descriptor_dict)

    # specify where to go look for caches
    descriptor.set_cache_roots(bundle_cache_root, fallback_roots)

    if descriptor_dict.get("version") == constants.LATEST_DESCRIPTOR_KEYWORD:
        log.debug("Latest keyword detected. Searching for latest version...")
        descriptor = descriptor.get_latest_version()
        log.debug("Resolved latest to be %r" % descriptor)

    return descriptor

def descriptor_uri_to_dict(uri):
    """
    Translates a descriptor uri into a dictionary, suitable for
    use with the create_io_descriptor factory method below.

    :param uri: descriptor string uri
    :returns: descriptor dictionary
    """
    from .base import IODescriptorBase
    return IODescriptorBase.dict_from_uri(uri)

def descriptor_dict_to_uri(ddict):
    """
    Translates a descriptor dictionary into a uri.

    :param ddict: descriptor dictionary
    :returns: descriptor uri
    """
    from .base import IODescriptorBase
    return IODescriptorBase.uri_from_dict(ddict)
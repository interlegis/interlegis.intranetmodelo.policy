# -*- coding: utf-8 -*-
"""Backport of collective.cover API."""
from collective.cover.tiles.configuration import ANNOTATIONS_KEY_PREFIX
from persistent.dict import PersistentDict
from plone.app.imaging.utils import getAllowedSizes
from zope.annotation.interfaces import IAnnotations


def get_tile_configuration(cover, id, _raw=False):
    """Get tile configuration and hide some of its ugglyness."""
    annotations = IAnnotations(cover)
    key = '{0}.{1}'.format(ANNOTATIONS_KEY_PREFIX, id)
    configuration = annotations.get(key, False)
    if not configuration:
        # FIXME: tiles don't have configuration first time we instantiate them
        tile = cover.get_tile(id)
        configuration = tile.get_tile_configuration()  # return defaults
        annotations[key] = PersistentDict(configuration)

    return configuration if _raw else prettify(configuration)


def set_tile_configuration(cover, id, **configuration):
    """Set tile configuration."""
    assert id in cover.list_tiles()
    annotations = IAnnotations(cover)
    key = '{0}.{1}'.format(ANNOTATIONS_KEY_PREFIX, id)
    # FIXME: tiles don't have configuration first time we instantiate them
    current = annotations.get(key, get_tile_configuration(cover, id, True))

    configuration = unprettify(configuration)
    for field, settings in configuration.iteritems():
        # update only keys present on the configuration parameter
        if 'order' in settings:
            # we have to reorder subsequent fields also
            index = int(settings['order'])
            _reorder(current, field, index)
        current[field].update(settings)

    annotations[key] = PersistentDict(current)


def prettify(configuration):
    original = configuration
    for key, value in original.iteritems():
        if isinstance(value, dict):
            # TODO: find a better name for 'htmltag'
            if 'imgsize' in value:
                value['scale'] = value['imgsize'].split(' ')[0]
                del value['imgsize']
            if 'order' in value:
                value['order'] = int(value['order'])
            if 'position' in value:
                value['align'] = value['position']
                del value['position']
            if 'visibility' in value:
                value['visible'] = value['visibility'] == u'on'
                del value['visibility']
        configuration[key] = value
    return configuration


def unprettify(configuration):
    original = configuration
    for key, value in original.iteritems():
        if isinstance(value, dict):
            # TODO: find a better name for 'htmltag'
            if 'scale' in value:
                allowed_sizes = getAllowedSizes()
                scale = value['scale']
                assert scale in allowed_sizes
                width, height = allowed_sizes[scale]
                value['imgsize'] = '{0} {1}:{2}'.format(scale, width, height)
                del value['scale']
            if 'order' in value:
                value['order'] = unicode(value['order'])
            if 'align' in value:
                value['position'] = value['align']
                del value['align']
            if 'visible' in value:
                value['visibility'] = u'on' if value['visible'] else u'off'
                del value['visible']
        configuration[key] = value
    return configuration


def _get_fields_in_order(configuration):
    fields = [(configuration[k]['order'], k)
              for k, v in configuration.iteritems() if k != 'css_class']
    fields.sort(key=lambda f: f[0])
    return [f[1] for f in fields]


def _set_fields_in_order(configuration, order):
    for i, field in enumerate(order):
        configuration[field]['order'] = unicode(i)


def _reorder(configuration, field, new_index):
    order = _get_fields_in_order(configuration)
    old_index = order.index(field)
    order.insert(new_index, order.pop(old_index))
    _set_fields_in_order(configuration, order)

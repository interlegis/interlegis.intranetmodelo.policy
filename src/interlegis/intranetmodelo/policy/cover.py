# -*- coding: utf-8 -*-
"""Backport of collective.cover API."""
from collective.cover.tiles.configuration import ANNOTATIONS_KEY_PREFIX
from persistent.dict import PersistentDict
from plone.app.imaging.utils import getAllowedSizes
from plone.tiles.interfaces import ITileDataManager
from zope.annotation.interfaces import IAnnotations

import json


def get_tiles(cover, types=None, layout=None):
    """Traverse the layout tree and return a list of tiles on it.

    :param types: tile types to be filtered; if none, return all tiles
    :type types: str or list
    :param layout: a JSON object describing sub-layout (internal use)
    :type layout: list
    :returns: a list of tiles; each tile is described as {id, type}
    """
    filter = types is not None
    if filter and isinstance(types, str):
        types = [types]

    if layout is None:
        # normal processing, we use the object's layout
        try:
            layout = json.loads(cover.cover_layout)
        except TypeError:
            layout = []
    else:
        # we are recursively processing the layout
        assert isinstance(layout, list)

    tiles = []
    for e in layout:
        if e['type'] == 'tile':
            if filter and e['tile-type'] not in types:
                continue
            tiles.append(dict(id=e['id'], type=e['tile-type']))
        if 'children' in e:
            tiles.extend(get_tiles(cover, types, e['children']))
    return tiles


def list_tiles(cover, types=None):
    """Return a list of tile id the layout.

    :param types: tile types to be filtered; if none, return all tiles
    :type types: str or list
    :returns: a list of tile ids
    """
    return [t['id'] for t in get_tiles(cover, types)]


def get_tile_type(cover, tile):
    """Get tile type."""
    tile = [t for t in get_tiles(cover) if t['id'] == tile]
    assert len(tile) in (0, 1)
    if len(tile) == 0:
        raise ValueError
    return tile[0]['type']


def get_tile(cover, tile):
    """Get tile type."""
    type = str(get_tile_type(cover, tile))
    tile = str(tile)
    return cover.restrictedTraverse('{0}/{1}'.format(type, tile))


def set_tile_data(cover, tile, **data):
    """Set tile attributes."""
    tile = get_tile(cover, tile)
    data_mgr = ITileDataManager(tile)
    data_mgr.set(data)


def get_tile_configuration(cover, id, _raw=False):
    """Get tile configuration and hide some of its ugglyness."""
    annotations = IAnnotations(cover)
    key = '{0}.{1}'.format(ANNOTATIONS_KEY_PREFIX, id)
    configuration = annotations.get(key, False)
    if not configuration:
        # FIXME: tiles don't have configuration first time we instantiate them
        tile = get_tile(cover, id)
        configuration = tile.get_tile_configuration()  # return defaults
        annotations[key] = PersistentDict(configuration)

    return configuration if _raw else prettify(configuration)


def set_tile_configuration(cover, id, **configuration):
    """Set tile configuration."""
    assert id in list_tiles(cover)
    annotations = IAnnotations(cover)
    key = '{0}.{1}'.format(ANNOTATIONS_KEY_PREFIX, id)
    # FIXME: tiles don't have configuration first time we instantiate them
    current = annotations.get(key, get_tile_configuration(cover, id, True))

    configuration = unprettify(configuration)
    for key, value in configuration.iteritems():
        current[key] = value

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

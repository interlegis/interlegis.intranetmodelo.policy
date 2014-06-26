# -*- coding: utf-8 -*-
from datetime import datetime
from interlegis.intranetmodelo.policy.utils import _add_id

import os

PROJECTNAME = 'interlegis.intranetmodelo.policy'

DEPENDENCIES = [
    'CMFPlacefulWorkflow',
]

LOREM_TITLE = u'Lorem ipsum'
LOREM_DESCRIPTION = u'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.'

IMAGE = open(
    os.path.join(
        os.path.dirname(__file__), 'tests', 'bandeira-brasil.jpg')).read()

startDate = datetime.now()
endDate = datetime.now()
timezone = 'Brazil/East',

# new intranet structure; this dictionary defines the objects that are going
# to be created on the root of the intranet; it also includes information
# about folder constrains and objects to be created inside them
INTRANET_STRUCTURE = [
    dict(
        type='collective.cover.content',
        title=u'Página inicial da Intranet',
        template_layout='Intranet Modelo',
    ),
    dict(
        type='Folder',
        title=u'Institucional',
        _children=[
            dict(
                type='Folder',
                title=u'Comunicados',
                _addable_types=['Collection', 'Folder', 'News Item'],
                _children=[
                    dict(
                        type='Collection',
                        title=u'Comunicados',
                        query=[
                            dict(
                                i='portal_type',
                                o='plone.app.querystring.operation.selection.is',
                                v='News Item',
                            ),
                            dict(
                                i='path',
                                o='plone.app.querystring.operation.string.relativePath',
                                v='../',
                            ),
                        ],
                        sort_reversed=True,
                        sort_on=u'created',
                        limit=100,
                    ),
                    dict(
                        type='News Item',
                        title=LOREM_TITLE,
                        description=LOREM_DESCRIPTION,
                    ),
                    dict(
                        type='News Item',
                        id='lorem-ipsum-1',
                        title=LOREM_TITLE,
                        description=LOREM_DESCRIPTION,
                    ),
                    dict(
                        type='News Item',
                        id='lorem-ipsum-2',
                        title=LOREM_TITLE,
                        description=LOREM_DESCRIPTION,
                    ),
                    dict(
                        type='News Item',
                        id='lorem-ipsum-3',
                        title=LOREM_TITLE,
                        description=LOREM_DESCRIPTION,
                    ),
                ],
            ),
            dict(
                type='Folder',
                title=u'Enquetes',
                _addable_types=['collective.polls.poll', 'Collection', 'Folder'],
                _children=[
                    dict(
                        type='collective.polls.poll',
                        title=u'Gostou da nova intranet?',
                        options=[
                            dict(option_id=0, description=u'Sim'),
                            dict(option_id=1, description=u'Não'),
                            dict(option_id=2, description=u'Pode melhorar'),
                        ],
                    ),
                ],
            ),
            # dict(
            #     type='Folder',
            #     title=u'Eventos',
            #     _addable_types=['Collection', 'Event', 'Folder'],
            #     _children=[
            #         dict(
            #             type='Collection',
            #             title=u'Eventos',
            #             query=[
            #                 dict(
            #                     i='portal_type',
            #                     o='plone.app.querystring.operation.selection.is',
            #                     v='Event',
            #                 ),
            #                 dict(
            #                     i='path',
            #                     o='plone.app.querystring.operation.string.relativePath',
            #                     v='../',
            #                 ),
            #             ],
            #             sort_reversed=True,
            #             sort_on=u'created',
            #             limit=100,
            #         ),
            #         dict(
            #             type='Event',
            #             title=u'Lorem ipsum',
            #             description=u'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.',
            #             startDate=startDate,
            #             endDate=endDate,
            #             timezone=timezone,
            #         ),
            #         dict(
            #             type='Event',
            #             id='lorem-ipsum-1',
            #             title=u'Lorem ipsum',
            #             description=u'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.',
            #             startDate=startDate,
            #             endDate=endDate,
            #             timezone=timezone,
            #         ),
            #         dict(
            #             type='Event',
            #             id='lorem-ipsum-2',
            #             title=u'Lorem ipsum',
            #             description=u'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.',
            #             startDate=startDate,
            #             endDate=endDate,
            #             timezone=timezone,
            #         ),
            #         dict(
            #             type='Event',
            #             id='lorem-ipsum-3',
            #             title=u'Lorem ipsum',
            #             description=u'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.',
            #             startDate=startDate,
            #             endDate=endDate,
            #             timezone=timezone,
            #         ),
            #     ],
            # ),
        ],
    ),
    dict(
        type='Folder',
        title=u'Setores',
        _children=[
            dict(
                type='Department',
                title=u'Setor 1',
            ),
            dict(
                type='Department',
                title=u'Setor 2',
            ),
            dict(
                type='Department',
                title=u'Setor N',
            ),
        ],
    ),
    dict(
        type='Folder',
        title=u'Serviços',
        _children=[
        ],
    ),
    dict(
        type='Folder',
        title=u'Projetos',
        _children=[
        ],
    ),
    dict(
        type='Folder',
        title=u'Solicitações',
        _children=[
        ],
    ),
    dict(
        type='Folder',
        title=u'Ponto de encontro',
        _children=[
            dict(
                type='Classifieds',
                title=u'Classificados',
            ),
            dict(
                type='Folder',
                title=u'Galeria de fotos',
                _addable_types=['Collection', 'Folder', 'Image'],
            ),
            dict(
                type='Folder',
                title=u'Mural',
                _addable_types=['Collection', 'Folder', 'News Item'],
                _children=[
                    dict(
                        type='Collection',
                        title=u'Mural',
                        query=[
                            dict(
                                i='portal_type',
                                o='plone.app.querystring.operation.selection.is',
                                v='News Item',
                            ),
                            dict(
                                i='path',
                                o='plone.app.querystring.operation.string.relativePath',
                                v='../',
                            ),
                        ],
                        sort_reversed=True,
                        sort_on=u'created',
                        limit=100,
                    ),
                    dict(
                        type='News Item',
                        title=LOREM_TITLE,
                        description=LOREM_DESCRIPTION,
                    ),
                ],
            ),
        ],
    ),
]

INTRANET_STRUCTURE = _add_id(INTRANET_STRUCTURE)

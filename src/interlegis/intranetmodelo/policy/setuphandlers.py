# -*- coding: utf-8 -*-
from interlegis.intranetmodelo.policy.config import DEPENDENCIES
from interlegis.intranetmodelo.policy.config import IMAGE
from interlegis.intranetmodelo.policy.config import INTRANET_STRUCTURE
from interlegis.intranetmodelo.policy.config import PROJECTNAME
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.uuid.interfaces import IUUID
from plonesocial.microblog.interfaces import IMicroblogContext
from Products.CMFCore.interfaces import IFolderish
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import alsoProvides
from zope.interface import implements

import logging

logger = logging.getLogger(PROJECTNAME)


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'interlegis.intranetmodelo.policy:uninstall',
            u'plonesocial.activitystream:default'
            u'plonesocial.activitystream:uninstall'
            u'plonesocial.microblog:default'
            u'plonesocial.microblog:uninstall'
            u'plonesocial.network:default'
            u'plonesocial.network:uninstall'
        ]


def install_old_style_dependencies():
    """Install/reinstall old-style dependencies.
    """
    logger.info(u'Instalando dependências do pacote')
    qi = api.portal.get_tool('portal_quickinstaller')
    for product in DEPENDENCIES:
        if not qi.isProductInstalled(product):
            qi.installProduct(product)
            logger.debug(u'    {0} instalado'.format(product))
        else:
            qi.reinstallProducts([product])
            logger.debug(u'    {0} reinstalado'.format(product))


def set_intranet_workflow_policy(obj):
    """Set workflow policy for object (and below if folderish).
    """
    obj.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
    pc = getattr(obj, WorkflowPolicyConfig_id)
    pc.setPolicyIn(policy='intranet')
    if IFolderish.providedBy(obj):
        pc.setPolicyBelow(policy='intranet')
    logger.debug(u'    {0} política de workflow alterada'.format(obj.getId()))


def create_intranet_root(portal):
    title = 'Intranet'
    id = title.lower()
    if id not in portal:
        logger.info(u'Criando estrutura da Intranet Modelo')
        intranet = api.content.create(
            # portal, type='Folder', title=title, excludeFromNav=True)
            portal, type='Folder', title=title)
        set_intranet_workflow_policy(intranet)
        # enable local navigation
        alsoProvides(intranet, INavigationRoot)
        # enable local microblog
        alsoProvides(intranet, IMicroblogContext)
        # XXX: workaround for https://github.com/plone/plone.api/issues/99
        intranet.setTitle(title)
        intranet.reindexObject()
    else:
        # XXX: why are we passing over here? running setuphandlers twice?
        logger.warn(u'Pulando {0}; conteúdo existente'.format(title))
        intranet = portal[id]
    return intranet


def constrain_types(folder, addable_types):
    """Constrain addable types in folder."""
    folder.setConstrainTypesMode(True)
    folder.setImmediatelyAddableTypes(addable_types)
    folder.setLocallyAllowedTypes(addable_types)


def create_intranet_structure(root, structure):
    """Create intranet structure."""
    for item in structure:
        id = item['id']
        title = item['title']
        if id not in root:
            obj = api.content.create(root, **item)
            # constrain types in folder?
            if '_addable_types' in item:
                constrain_types(obj, item['_addable_types'])
            # the content has more content inside? create it
            if '_children' in item:
                create_intranet_structure(obj, item['_children'])
            # add an image to all news items
            if obj.portal_type == 'News Item':
                obj.setImage(IMAGE)
            # XXX: workaround for https://github.com/plone/plone.api/issues/99
            obj.setTitle(title)
            obj.reindexObject()
            logger.debug(u'    {0} criado e publicado'.format(title))
        else:
            logger.debug(u'    pulando {0}; conteúdo existente'.format(title))


def setup_department_permissions(root):
    """Department content type is allowed **only** within its own folder
    """
    permission = 'interlegis.intranetmodelo.departments: Add Department'
    roles = ('Manager', 'Site Administrator', 'Owner', 'Contributor')
    folder = root['setores']
    folder.manage_permission(
        permission,
        roles=roles
    )
    logger.debug(u'Permissoes ajustadas em {0}'.format(folder.Title()))

    # Remove permission on the root of the site
    portal = api.portal.get()
    portal.manage_permission(
        permission,
        roles=(),
    )


def import_registry_settings():
    """Import registry settings; we need to do this before other stuff here,
    like using a cover layout defined there.

    XXX: I don't know if there is other way to do this on ZCML or XML.
    """
    PROFILE_ID = 'profile-{0}:default'.format(PROJECTNAME)
    setup = api.portal.get_tool('portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')


def populate_intranet_cover(portal):
    """Populate intranet front page. The layout is composed by 3 rows:

    1. 1 basic tile
    2. 2 collection tiles
    3. 3 banner tiles

    Populate and configure those tiles.
    """
    from cover import set_tile_configuration

    base_url = portal['intranet']['ponto-de-encontro'].absolute_url()
    cover = portal['intranet']['pagina-inicial-da-intranet']
    # second row
    tiles = cover.list_tiles('collective.cover.collection')
    obj = portal['intranet']['institucional']['comunicados']['comunicados']
    assert obj.portal_type == 'Collection'
    uuid = IUUID(obj)
    data = dict(header=u'Comunicados', footer=u'Mais…', uuid=uuid)
    cover.set_tile_data(tiles[0], **data)
    set_tile_configuration(cover, tiles[1], image={'scale': 'icon'})
    obj = portal['intranet']['ponto-de-encontro']['mural']['mural']
    assert obj.portal_type == 'Collection'
    uuid = IUUID(obj)
    data = dict(header=u'Mural', footer=u'Mais…', uuid=uuid)
    cover.set_tile_data(tiles[1], **data)
    set_tile_configuration(cover, tiles[1], image={'scale': 'preview'})
    # third row
    tiles = cover.list_tiles('collective.cover.banner')
    remote_url = base_url + '/classificados'
    data = dict(title=u'Classificados', remote_url=remote_url)
    cover.set_tile_data(tiles[0], **data)
    remote_url = base_url + '/galeria-de-fotos'
    data = dict(title=u'Galeria de fotos', remote_url=remote_url)
    cover.set_tile_data(tiles[1], **data)
    remote_url = base_url + '/mural'
    data = dict(title=u'Mural', remote_url=remote_url)
    cover.set_tile_data(tiles[2], **data)


def set_intranet_default_page(portal):
    """Set the default page for the intranet."""
    portal['intranet'].setDefaultPage('pagina-inicial-da-intranet')
    logger.info(u'Visão padrão da intranet estabelecida')


def open_feedback_poll(portal):
    intranet = portal['intranet']
    poll = intranet['institucional']['enquetes']['gostou-da-nova-intranet']
    api.content.transition(poll, 'open')


def setup_various(context):
    marker_file = '{0}.txt'.format(PROJECTNAME)
    if context.readDataFile(marker_file) is None:
        return

    install_old_style_dependencies()
    portal = api.portal.get()
    import_registry_settings()
    intranet = create_intranet_root(portal)
    create_intranet_structure(intranet, INTRANET_STRUCTURE)
    setup_department_permissions(intranet)
    populate_intranet_cover(portal)
    set_intranet_default_page(portal)
    # open_feedback_poll(portal)


def fix_links_in_static_portlet(context):
    """Fix links in "atalhos" portlet. To make this independent of portal site
    name we need to fix the links adding the portal URL. This is called after
    import of portlets.xml.
    """

    marker_file = '{0}.txt'.format(PROJECTNAME)
    if context.readDataFile(marker_file) is None:
        return

    from plone.portlets.interfaces import IPortletAssignmentMapping
    from plone.portlets.interfaces import IPortletManager
    from zope.component import getMultiAdapter
    from zope.component import getUtility

    portal = api.portal.get()
    obj = portal['intranet']['pagina-inicial-da-intranet']
    manager = getUtility(IPortletManager, name='plone.leftcolumn', context=obj)
    mapping = getMultiAdapter((obj, manager), IPortletAssignmentMapping)
    assert 'atalhos' in mapping

    portlet = mapping['atalhos']
    intranet_url = portal.absolute_url() + '/intranet/'
    portlet.text = portlet.text.replace('intranet/', intranet_url)
    logger.debug(u'Links substituidos no portlet de atalhos')

    manager = getUtility(IPortletManager, name='plone.rightcolumn', context=obj)
    mapping = getMultiAdapter((obj, manager), IPortletAssignmentMapping)
    assert 'voting-portlet' in mapping

    portlet = mapping['voting-portlet']
    intranet = portal['intranet']
    poll = intranet['institucional']['enquetes']['gostou-da-nova-intranet']
    portlet.poll = IUUID(poll)
    logger.debug(u'Portlet de enquetes atualizado')

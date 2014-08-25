# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.0b3'
description = 'Intranet Modelo do Programa Interlegis.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='interlegis.intranetmodelo.policy',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='interlegis intranet',
    author='Programa Interlegis',
    author_email='ti@interlegis.leg.br',
    url='https://github.com/interlegis/interlegis.intranetmodelo.policy',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['interlegis'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'cioppino.twothumbs',
        'collective.classifieds',
        'collective.cover',
        'collective.polls',
        'collective.weather',
        'collective.xmpp.chat',
        'collective.xmpp.core',
        'five.grok',
        'ftw.globalstatusmessage',
        'interlegis.intranetmodelo.departments',
        'plone.api',
        'plone.app.event [archetypes] <1.2',
        'plone.app.ldap',
        'plone.app.openid',
        'plone.app.portlets',
        'plone.app.users',
        'plone.formwidget.captcha',
        'plonesocial.activitystream',
        'plonesocial.microblog',
        'plonesocial.network',
        'Products.CMFCore',
        'Products.CMFPlacefulWorkflow',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'Products.SQLAlchemyDA',
        's17.portlets',
        's17.taskmanager',
        'setuptools',
        'Solgema.fullcalendar',
        'webcouturier.dropdownmenu',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot] >=4.2.2',
            'plone.browserlayer',
            'plone.testing',
            'robotsuite',
        ],
    },
)

********************************
interlegis.intranetmodelo.policy
********************************

.. contents:: Conteúdo
   :depth: 2

Introdução
==========

Este pacote inclui as políticas da Intranet Modelo do Programa Interlegis.

O pacote cria um folder chamado 'Intranet' e aplica nele um workflow de
intranet. Todo conteúdo criado dentro desse folder usará também esse workflow.

O pacote instala também o Plone Social Suite para prover uma solução de
microblogging completa, incluindo fluxo de atividades, perfis de usuário e
funcionalidade de seguir/deixar de seguir.

Dos portlets são adicionados no contexto do folder da Intranet: atualização do
estado e fluxo de atividades.

O viewlet ``plonesocial.suite.navigation``, instalado pelo pacote
``plonesocial.activitystream``, e ocultado.

Informação dos membros do portal
--------------------------------

O pacote adiciona 3 campos no formulário de informação dos membros do portal:

* data de nascimento
* número do ramal
* número do celular

Visões
------

Uma nova visão chamada de `@@members-list` foi disponibilizada. Esta visão
lista os membros do portal mostrando seu retrato, nome completo, locação,
ramal, celular e email.

Dependências
============

Este pacote instala as seguintes dependências:

* `collective.weather`_
* `collective.xmpp.chat`_
* `interlegis.intranetmodelo.departments`_
* `Products.CMFPlacefulWorkflow`_
* `plonesocial.activitystream`_
* `plonesocial.microblog`_
* `plonesocial.network`_
* `s17.taskmanager`_

.. _`collective.weather`: https://pypi.python.org/pypi/collective.weather
.. _`collective.xmpp.chat`: https://pypi.python.org/pypi/collective.xmpp.chat
.. _`interlegis.intranetmodelo.departments`: https://pypi.python.org/pypi/interlegis.intranetmodelo.departments
.. _`Plone Social Suite`: https://pypi.python.org/pypi/plonesocial.suite
.. _`plonesocial.activitystream`: https://pypi.python.org/pypi/plonesocial.activitystream
.. _`plonesocial.microblog`: https://pypi.python.org/pypi/plonesocial.microblog
.. _`plonesocial.network`: https://pypi.python.org/pypi/plonesocial.network
.. _`Products.CMFPlacefulWorkflow`: https://pypi.python.org/pypi/Products.CMFPlacefulWorkflow
.. _`s17.taskmanager`: https://pypi.python.org/pypi/s17.taskmanager

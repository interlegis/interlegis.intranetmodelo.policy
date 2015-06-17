Changelog
=========

1.0b5 (2015-06-17)
------------------

- Fix test test_setup.py
  [marciomazza]


1.0b4 (2014-10-24)
------------------

- Fix import step registration to avoid running it twice
  [hvelarde]

- Fix test for collective.cover layouts
  [jeanferri]

- Change discussion default settings
  [jeanferri]

- Remove institucional folder from intranet because it already exists in portal
  [jeanferri]

- Fix import step registration to avoid running it twice.
  Feedback poll is now open by default.
  [hvelarde]

- Install s17.taskmanager by default.
  [hvelarde]


1.0b3 (2014-08-25)
------------------

- Correções nos metadados do pacote
  [ericof]


1.0b2 (2014-07-02)
------------------

- Habilita servidor XMPP padrão (https://colab.interlegis.leg.br/ticket/2944).
  [hvelarde]


1.0b1 (2014-06-05)
------------------

- Configuração de grupos organizacionais e permissões (refs. `#2909`_).

- Adiciona o ``collective.polls`` como dependência do projeto; adiciona
  portlets de votação.

- Relação dinâmica de aniversariantes (refs. `#2911`_).

- Recados, mensagens e alertas para membros (refs. `#2913`_).

- Comentários, ranqueamento e classificação de conteúdos (refs. `#2915`_).

- Adiciona portlet estático com atalhos para criação de conteúdo.

- Adiciona o ``collective.weather`` como dependência do projeto; instala,
  configura e adiciona o portlet do estado do tempo.

- Cria estruturas de informação como setores, serviços, utilidades, projetos
  (refs. `#2908`_ e `#2914`_).

- Mural e classificados (refs. `#2912`_).

- Atualiza a versão do ``plone.app.event`` para 2.5.1.


1.0a4 (2014-05-18)
------------------

- Remove limitação no versionamento do plone.app.portlets.

- Lista de funcionários e seus contatos (refs. `#2910`_).


1.0a3 (2014-05-01)
------------------

- Cliente para mensageiro XMPP web integrado.

- Conector para bancos de dados relacionais.

- Conector para OpenLDAP e OpenID.

- Agenda de eventos compartilhada com o portal.

- Gerenciamento de ocorrências e atividades.

- Hide install/uninstall profiles of package dependencies.


1.0a2 (2014-03-11)
------------------

- Avoid ``ConfigurationConflictError: Conflicting configuration actions``
  when installing with Portal Modelo by renaming the upgrade step that
  sets up the intranet.


1.0a1 (2014-03-11)
------------------

- Initial release.

.. _`#2908`: https://colab.interlegis.leg.br/ticket/2908
.. _`#2909`: https://colab.interlegis.leg.br/ticket/2909
.. _`#2910`: https://colab.interlegis.leg.br/ticket/2910
.. _`#2911`: https://colab.interlegis.leg.br/ticket/2911
.. _`#2912`: https://colab.interlegis.leg.br/ticket/2912
.. _`#2913`: https://colab.interlegis.leg.br/ticket/2913
.. _`#2914`: https://colab.interlegis.leg.br/ticket/2914
.. _`#2915`: https://colab.interlegis.leg.br/ticket/2915

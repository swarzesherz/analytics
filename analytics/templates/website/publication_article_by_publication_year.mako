## coding: utf-8
<%inherit file="base.mako"/>

<%block name="central_container">
  <div class="chart">
    <%include file="publication_article_licenses_publication_year.mako"/>
  </div>
  <div class="chart">
    <%include file="publication_article_subject_areas_publication_year.mako"/>
  </div>
  <div class="chart">
    <%include file="publication_article_languages_publication_year.mako"/>
  </div>
  <div class="chart">
    <%include file="publication_article_affiliations_publication_year.mako"/>
  </div>
  <div class="chart">
    <%include file="publication_article_citable_documents.mako"/>
  </div>
</%block>

<%block name="extra_js">
</%block>
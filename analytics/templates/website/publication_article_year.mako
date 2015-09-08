## coding: utf-8
<div id="article_year" style="width:60%; height:400px;"></div>
<script language="javascript">
    $(document).ready(function() {
        var options = {
            'chart': {
                'type': 'column'
            },
            'title': {
                'text': '${_(u'Distribuição de ano de publicação dos documentos')}',
            },
            'yAxis': {
                'title': {
                    'text': '${_(u'Número de documentos')}'
                }
            },
            'legend': {
                'enabled': false
            }
        };
        
        var url =  "${request.route_url('publication_article_year')}?code=${selected_code}&collection=${selected_collection_code}&callback=?";

        $.getJSON(url,  function(data) {
            options['series'] = data['series'];
            options['xAxis'] = {
                'categories': data['categories'],
                'title': {
                    'text': '${_(u'Ano de publicação')}',
                    'align': 'high'
                }
            };
            $('#article_year').highcharts(options);
        });
    });
</script>
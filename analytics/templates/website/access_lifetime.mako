<ul id="lifetime" style="width: 60%; list-style-type: none; padding: 0px; margin: 0px;"></ul>
<script language="javascript">
    $(document).ready(function() {
        var options = {
            'chart': {
                'type': 'column'
            },
            'xAxis': {
                'title': {
                    'text': 'Publication Year',
                    'align': 'high'
                }
            },
            'yAxis': {
                'title': {
                    'text': ''
                }
            },
            'title': {
                'text': 'Vida útil de artigos por número de acessos',
            },
            'legend': {
                'enabled': false
            }
        };
        
        var url =  "/ajx/accesses/lifetime?code=${selected_code}&collection=${selected_collection_code}&range_start=${range_start}&range_end=${range_end}&callback=?";

        $.getJSON(url,  function(data) {
            for (item in data) {
                options['series'] = data[item]['series'];
                options['xAxis']['categories'] = data[item]['categories'];
                options['yAxis']['title']['text'] = 'acessos ' + data[item]['series'][0]['name'];
                options['title']['text'] = 'Vida útil de artigos por número de acessos em ' + data[item]['series'][0]['name']
                $('#lifetime').append('<li id="lifetime_'+item+'" style="height: 250px; margin-bottom: 100px; padding: 0px; margin: 0px;"></li>');
                $('#lifetime_'+item).highcharts(options);
            };
        });
    });
</script>
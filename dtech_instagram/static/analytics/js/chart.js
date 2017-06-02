    function chart_maker(target_element_id, chart_data) {
        var chartDataBase = {
            "type": "serial",
            "theme": "light",
            "valueAxes": [{
                "gridColor": "none",
                //"gridAlpha": 0.2,
                //"dashLength": 0,
                "minimum": 0,
                "color":"#797979"
            }],
            "gridAboveGraphs": true,
            "startDuration": 1,
            "balloon": {
                "borderThickness": 0,
                "shadowAlpha": 0,
                "maxHeight":"45px",
                "offsetY": 4,
                "fixedPosition": true
            },
            "graphs": [{
                "balloonText": "<img width='45px' src='[[img_url]]' />",
                "fillAlphas": 0.8,
                "lineAlpha": 0.2,
                "type": "column",
                "valueField": "value",
                "fillColors": "#6BBAEC",
                "columnWidth":.875,
                "yAxis":0
            }],
            "chartCursor": {
                "categoryBalloonEnabled": false,
                "cursorAlpha": 0,
                "zoomable": false
            },
            "categoryField": "label",
            "categoryAxis": {
                "gridPosition": "start",
                "gridAlpha": 0,
                "tickPosition": "start",
                "tickLength": 1
            },
            "export": {
                "enabled": false
            }
        };

        chart_data = $.extend(true, {"dataProvider": chart_data}, chartDataBase);
        var Chart = AmCharts.makeChart(target_element_id, chart_data);
    }

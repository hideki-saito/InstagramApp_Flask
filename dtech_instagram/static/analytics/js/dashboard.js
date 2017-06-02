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


        var engagementChartData = $("#engagement-chart").data("chart-data");
        engagementChartData = $.extend(true, {"dataProvider": engagementChartData}, chartDataBase);
        var engagementChart = AmCharts.makeChart("engagement-chart", engagementChartData);


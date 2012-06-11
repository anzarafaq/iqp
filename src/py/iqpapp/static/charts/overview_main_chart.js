/**
 * Define global variables
 */
var overviewMainChart; // global
var overviewMainChartOptions;

function changeChartType(type,options,chart)
{
    var chartNewOptions;
    chartNewOptions= options;
    chartNewOptions.chart.defaultSeriesType = String(type);
    chartNewOptions.series.type = String(type);
    chartNewOptions.series[0].type = String(type);
    overviewMainChart.destroy();
    overviewMainChart = new Highcharts.Chart(chartNewOptions);
}

function attachSortHandlers()
{
        jQuery(".hDivBox").find("table").find("thead").find("tr").find("th").each(function(index,val)
        {
            jQuery(this).click(function()
            {
                
                reDrawTable(index,this);
            });
        });
}
function formatData(seriesData)
{
    data = new Array();
    cat = new Array();
    for(var i = 0; i<seriesData.length; i++)
    {
        data.push(
            {
                name : seriesData[i][0],
                scenarioCount : seriesData[i][1], //we need scenario count to post this object to server for gereating pdf from table data
                y : seriesData[i][2]
            }
        )
        cat.push(
            seriesData[i][0]
        )
    }
    return [data,cat];
}

/**
 * Request data from the server and create a chart
 * 
 */
function createOverviewMainChart(args, container) {
    url = '/overview_main_chart_data_source/' + '?'
    $.getJSON(url, args, function(data) {
    var yaxisname = getParameterByName("filter");
    var chartType = getParameterByName('chartType');
    switch(chartType)
    {
        case "column":
        $(".chart-icons[alt = 'column']").addClass('chart-icon-inactive');
        $(".chart-icons[alt = 'pie']").addClass('chart-icon-active');
            break;
        case "pie":
        $(".chart-icons[alt = 'pie']").addClass('chart-icon-inactive');
        $(".chart-icons[alt = 'column']").addClass('chart-icon-active');
            break;
        case null:
            $(".chart-icons[alt = 'column']").addClass('chart-icon-inactive');
            $(".chart-icons[alt = 'pie']").addClass('chart-icon-active');
            chartType = "column";
            break;
        default:
            chartType = "column";
            $(".chart-icons[alt = 'column']").addClass('chart-icon-inactive');
            $(".chart-icons[alt = 'pie']").addClass('chart-icon-active');
            break;
    }
    overviewMainChartOptions = {
      chart: {
        renderTo: container,
        defaultSeriesType: chartType
            },
        credits: {
            enabled: false
        },
        title: {
            text: 'Application Family '+ (yaxisname || "")
            //text: 'Application Family Issues'
            },
        xAxis: {
            categories: [],
            enabled: true,
            labels: {
                formatter: function() {
                    // currently this does not create the href links. problem with highcharts version?
                    var retval = "<a href='/" + this.value + "/?chartType=column'>" + this.value + "</a>";
                    return  retval;
                }
            }
        },
        tooltip: {
        formatter: function() {
            tempobj = this;
            return '<b>'+ this.point.name +'</b>: '+  Highcharts.numberFormat(this.y, 0, ',') + ' Issues';
        }
        },
        legend: {
            enabled: false
        },
        series: [{
        type: chartType,
        cursor: 'pointer',
        point: {
            events: {
            click: function() {
                var newUrl = './' + this.name + '/' + '?'
                for (var key in args) {
                var val = args[key];
                newUrl = newUrl + key + '=' + val + '&'
                }
                //newUrl = newUrl + 'chartType=' + overviewMainChartOptions.chart.defaultSeriesType;
                newUrl =jQuery.param.querystring(newUrl,"chartType="+overviewMainChartOptions.chart.defaultSeriesType);
                $(location).attr('href',newUrl);
            }
            }
        },
        data: []
        }],
        yAxis : {
            title:
            {
                text : yaxisname?yaxisname+" Issues":"Issues"
            }
        },
        exporting:
        {
            enabled : false,
            filename : "chart",
            type : "image/png",
            url : "http://localhost/exporting/index.php"
        }
    };
    var DataAndCat = formatData(data);
    overviewMainChartOptions.series[0].data = DataAndCat[0]; // data[0] = name, data[1] = no of scenarios, data[2] = problems total
    overviewMainChartOptions.xAxis.categories = DataAndCat[1];
    overviewMainChart = new Highcharts.Chart(overviewMainChartOptions);
    window.tableData = data; // make a global object for data that can be used again when we sort it
    window.tableTitle = ""; //no table title for overiew page table
    drawTable(2); // 2 -> sortby , by default no of scenario
    attachSortHandlers();
    });
};

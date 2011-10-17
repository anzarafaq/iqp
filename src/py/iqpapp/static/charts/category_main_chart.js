/**
 * Define global variables
 */
var categoryMainChart; // global
var categoryMainChartOptions;

/**
 * Request data from the server and create a chart
 */

function changeChartType(type,options,chart)
{
	var chartNewOptions;
	chartNewOptions= options;
	chartNewOptions.chart.defaultSeriesType = String(type);
	chartNewOptions.series.type = String(type);
	chartNewOptions.series[0].type = String(type);
	categoryMainChart.destroy();
	categoryMainChart = new Highcharts.Chart(chartNewOptions);
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
				y : seriesData[i][2]
			}
		)
		cat.push(
			seriesData[i][0]
		)
	}
	return [data,cat];
}

function createCategoryMainChart(name, args, container) {
    url = '/category_main_chart_data_source/' + name + '/' + '?'
    $.getJSON(url, args, function(data) {
    var yaxisname = getParameterByName("filter");
    var chartType = getParameterByName('chartType');
     switch(chartType)
    {
    	case "column":
    	$(".chart-icons[alt = 'column']").addClass('chart-icon-inactive');
    	$(".chart-icons[alt = 'pie']").addClass('chart-icon-active');
    	chartType = "column";
    		break;
    	case "pie":
    	$(".chart-icons[alt = 'pie']").addClass('chart-icon-inactive');
    	$(".chart-icons[alt = 'column']").addClass('chart-icon-active');
    	chartType = "pie";
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
	categoryMainChartOptions = {
        chart: {
			renderTo: container,
			defaultSeriesType: 'column'
         },
        credits: {
        	enabled: false
    	},
        title: {
			text: name + ' Issues'
            },
        xAxis: {
        	categories: []
    		},
    	yAxis : {
			title:
			{
				text : yaxisname?yaxisname+" Issues":"Issues"
			}
		},
	    tooltip: {
		formatter: function() {
		    tempobj = this;
		    return '<b>'+ this.point.name +'</b>: '+   Highcharts.numberFormat(this.y, 0, ',') + ' Issues';
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
			    var newUrl = './' + this.name + '/?';
			    for (var key in args) {
				var val = args[key];
				newUrl = newUrl +key + '=' + val + '&'
			    }
			    newUrl =jQuery.param.querystring(newUrl,"chartType="+categoryMainChartOptions.chart.defaultSeriesType);
			    $(location).attr('href',newUrl);
			}
		    }
		},
		data: []
	    }]
	};
	var DataAndCat = formatData(data);
	categoryMainChartOptions.series[0].data =DataAndCat[0];
	categoryMainChartOptions.xAxis.categories = DataAndCat[1];
	categoryMainChart = new Highcharts.Chart(categoryMainChartOptions);
	window.tableData = data; // make a global object for data that can be used again when we sort it
	window.tableTitle = ""; //no table title for overiew page table
	drawTable(2); // 2 -> sortby , by default no of scenario
	attachSortHandlers();
    });
}
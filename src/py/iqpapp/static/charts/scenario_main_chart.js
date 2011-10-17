/**
 * Define global variables
 */
var scenarioMainChart; // global
var scenarioMainChartOptions;
var selectedPoint = null; //we use this in the point.events.click to reset it
var groupBy = null;//we need this when we create tables
//
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
			//scenarioMainChart.redraw();
			scenarioMainChart = new Highcharts.Chart(chartNewOptions);
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
				y : seriesData[i][1],
				sliced : false,
				selected : false
			}
		);
		cat.push(
			seriesData[i][0]
		);
	}
	return [data,cat];
}

function createScenarioMainChart(name, args, container,scn_des) {
	shortDes = wordFormatting(scn_des);
    mainUrl = '/scenario_main_chart_data_source/' + name + '/' + '?'
    $.getJSON(mainUrl, args, function(data) {
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
	scenarioMainChartOptions = {
            chart: {
		renderTo: container,
		defaultSeriesType : chartType
            },
            events:
            {
            	load : createScenarioTrendChart(name, args, "scenario-trend-chart-container")
            },
            credits: {
        enabled: false
    	},
            title: {
		text: shortDes,
		align:"center",
		style:
		{
			fontWeight : 'normal'
		}
            },
	    yAxis: {
		title: {
		    text: 'Issues'
		},
		min: 0
	    },
	    xAxis: {
        categories: []/*,
        labels:
  				{
  					rotation : null,
  					y : 10
  				}*/
    	},
	    tooltip: {
		formatter: function() {
		    return '<b>'+ this.point.name +'</b>: '+ this.y + ' Issues';
		}
	    },
	    legend: {
        	enabled: false
    	},
    	plotOptions: {
         pie: {
            allowPointSelect: true
           }
      },
	    series: [{
	    id : 'series1',
	    allowPointSelect : true,
	    cursor: 'pointer',
		type: chartType,
		data: [],
		point:{
		events: {
			click: function() {
				var options;
				$('.qsbox').val("");
				if(this.selected)
				{
					options = {
						query : "",
						newp : 1
						//url : window.tableUrl.replace('&match="like"','&match="="'),
						//url : flextable.url+'&match=""'
					}
					scenarioMainChartOptions.series[0].data[this.x].selected = false;
					scenarioMainChartOptions.series[0].data[this.x].sliced = false;
					if(selectedPoint !== null) 
					{
						scenarioMainChartOptions.series[0].data[selectedPoint].selected = false;
						scenarioMainChartOptions.series[0].data[selectedPoint].sliced = false;
					}
						
					/*this.config.selected = false;
					this.config.sliced = false;*/
				}
				else
				{
					options = {
						qtype : groupBy?groupBy:getParameterByName('groupby'),
						query : encodeURIComponent(this.name),
						url : jQuery.param.querystring(window.tableUrl,"match=equals"),//window.tableUrl.replace('&match=like','&match="="'),
						newp : 1
						//url : flextable.url+'&match=""'
					};
					scenarioMainChartOptions.series[0].data[this.x].selected = true;
					scenarioMainChartOptions.series[0].data[this.x].sliced = true;
					if(selectedPoint !== null)
					{
						scenarioMainChartOptions.series[0].data[selectedPoint].selected = false;
						scenarioMainChartOptions.series[0].data[selectedPoint].sliced = false;
					}
					/*this.config.selected = true;
					this.config.sliced = true;*/
				}
				selectedPoint = this.x;
				window.tableUrl = jQuery.param.querystring(window.tableUrl,"match=like");//window.tableUrl.replace('&match="="','&match=like');
				flextable = $('#scenario_tables').flexOptions(options);
				$('#scenario_tables').flexReload(flextable);
				//var t = setTimeout("$('#scenario_tables').flexReload(flextable);",350);
				flextable = $('#scenario_tables').flexOptions({url:window.tableUrl});
				return true;
			  }
		   }
		  }
	    }]
	};
	$('#sb_input').attr('placeholder',wordFormatting(data['groupby']," "));
	groupBy = data['groupby'];
	var DataAndCat = formatData(data['data']);
	scenarioMainChartOptions.series[0].data = DataAndCat[0];
	/*if(scenarioMainChartOptions.series[0].data.length > 10)
	{
		scenarioMainChartOptions.xAxis.labels.rotation = 25;
		scenarioMainChartOptions.xAxis.labels.y = 35;
	}*/
	scenarioMainChartOptions.xAxis.categories = DataAndCat[1];
	scenarioMainChart = new Highcharts.Chart(scenarioMainChartOptions);
    });
}
/**
 * Request data from the server and create the groupby dropdown selector
 * 
 */
// filters on the rights
// this function is not used
/*function createScenarioMainChartOptions(name, args, container) {
    optionsUrl = '/scenario_main_chart_options_data_source/' + name + '/' + '?'
    $.getJSON(optionsUrl, args, function(data) {
	var items = [];
	var mostlyused_length;
	//if data["most-five"]
	
		$.each(data["most-five"],function(key,val)
		{
		var getUrl = String(val);
		var val = wordFormatting(String(val)," ");
	    items.push('<li class = "default-filter"><label for='+getUrl+'>'+val+'</label></li>');
	 	});
	   $.each(data["others"],function(key,val)
		{
		var getUrl = String(val);
		var val = wordFormatting(String(val)," ");
	    items.push('<li class = "default-filter"><label for='+getUrl+'>'+val+'</label></li>');
	 	});
	$("#sb_dropdown").append(items.join('')).find("li:last").addClass('bottom-menu-item')
		//append the helpers
	.parent()
	.find('li')
	.eq(0)
	.before('<li class = "list-tags"> <i>Most Commonly Used</i></li>')
	.parent().find('li')
	.eq(data["most-five"].length)
	.after('<li class = "list-tags"> <i>Others</i></li>');
	//we use thsese numbers when the user blurs the input to know which one is currently selected useing mouse etc
	window.totalFilters = items.length;
	window.currentFilter = 0; //not the 0 because it will be a tag
    });
} */

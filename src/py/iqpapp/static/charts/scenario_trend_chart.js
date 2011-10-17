/**
 * Define global variables
 */
var scenarioTrendChart; // global
var scenarioTrendChartOptions;
var scenarioPopUpTrendChart;
var popUpTrendData;

/**
 * Request data from the server and create a chart
 */
function createScenarioTrendChart(name, args, container) {
    proportionChartUrl = '/scenario_trend_chart_data_source/' + name + '/' + '?'
    $.getJSON(proportionChartUrl, args, function(data) {
	scenarioTrendChartOptions = {
	    chart: {
		renderTo: container,
		defaultSeriesType: 'line',
		marginBottom : 40
	    },
        events:
        {
	    	load : createScenarioTableHeaders(name, args, "scenario_table")
	    },
	    credits: {
        enabled: false
    	},
	    title: {
		text: 'Trend (Last 5 runs)',
		x:20
	    },
	     subtitle: {
         text: ' '
      	},
	    legend: {
        	enabled: false
    	},
    	 tooltip: {
         		formatter : function()
         		{
         			var date = new Date(this.x);
         			return date.toDateString();
         		}             
      	},
    	plotOptions: {
         area: {
            fillColor: {
               linearGradient: [0, 0, 0, 300],
               stops: [
                  [0, Highcharts.getOptions().colors[0]],
                  [1, 'rgba(2,0,0,0)']
               ]
            },
            lineWidth: 1,
            marker: {
               enabled: false,
               states: {
                  hover: {
                     enabled: true,
                     radius: 5
                  }
               }
            },
            shadow: false,
            states: {
               hover: {
                  lineWidth: 1                  
               }
            }
         }
       },
	    xAxis: {
	    	labels :
	    		{
	    			enabled : false
	    		}
	    },
	    yAxis: {
		title: {
		    text: 'Issues'
		},
			min : 0.6,
         startOnTick: false,
         showFirstLabel: false
	    },
	    series: [{
	    type : 'line',
		name: wordFormatting(name," "),
		data: []
	    }],
      	exporting:
	    {
	    	enabled : false
	    }
	};
	popUpTrendData = data;
	var trendData;
	if(data.length > 5)
	{
		trendData = data.slice(0,5)
	}
	else
		trendData = data;
	scenarioTrendChartOptions.series[0].data = trendData;
	scenarioTrendChart = new Highcharts.Chart(scenarioTrendChartOptions);
    });
}

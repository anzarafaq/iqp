/**
 * Define global variables
 */
var overviewProportionChart; // global
var overviewProportionChartOptions;

/**
 * Request data from the server and create a chart
 */
function formatProportionData(data)
{
	var formattedData = [];
	var issueName;
	if (data.length > 0){
	issueName = data[0][1] > 1 ? "Issues" : "Issue";
	formattedData.push(
		{
		name : issueName,
		y	 : data[0][1],
		sliced: true,
        selected: true,
        color : '#FF0000'
       }
	);
	}
	var noIssueName;
	if (data.length > 1)
	{
	 noIssueName = data[1][1] > 1 ? "No Issues" : "No Issue";
	formattedData.push(
		{
		name : noIssueName,
		y	 : data[1][1],
		sliced: false,
        selected: false,
		color: '#50B432'
		}
	);
	}
	return formattedData;
}
function createOverviewProportionChart(args, container) {
    url = '/overview_proportion_chart_data_source/' + '?'
    $.getJSON(url, args, function(data) {
	overviewProportionChartOptions = {
        chart: {
			renderTo: container,
			defaultSeriesType: 'pie',
			plotBackgroundColor: null,
         	plotBorderWidth: 0,
         	plotShadow: false
         },
       	credits: {
        	enabled: false
    	},
        title: {
			text: 'Issues vs. No Issues'
            },
	    tooltip: {
		formatter: function() {
		    return '<b>'+ this.point.name +'</b>: '+ this.y + ' scenarios';
		}
	    },
	    series: [{
		type: 'pie',
		data: []
	    }],
	    plotOptions: {
         pie: {
            allowPointSelect: true,
            slicedOffset : 3,
            size: 140,
            dataLabels: {
                distance: 5,
                color: '333'
            }
           }
      },
      exporting:
	    {
	    	enabled : false
	    }
	};
	data = formatProportionData(data);
	overviewProportionChartOptions.series[0].data = data;
	overviewProportionChart = new Highcharts.Chart(overviewProportionChartOptions);
    });
}

var scenarioPopUpTrendChartOptions = {
	chart:{
         renderTo: 'popup-trend-container',
         zoomType: 'x'
      },
       title: {
         text: 'Trend'
      },
      credits: {
        enabled: false
    	},
       subtitle: {
         text: document.ontouchstart === undefined ?
            'Click and drag in the plot area to zoom in' :
            'Drag your finger over the plot to zoom in'
      },
      tooltip: {
         shared: true               
      },
      legend: {
         enabled: false
      },
      xAxis: {
	    labels :
	    		{
	    			enabled : true
	    		},
		 type: 'datetime',
		 labels: {
            formatter: function() {
                return Highcharts.dateFormat('%d %b %y', this.value);
            }
       		},
       		style: {
				color: '#6D869F',
				fontWeight: 'bold'
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
      series: [{
         type: 'area',
         data : null
        }]
      };
       
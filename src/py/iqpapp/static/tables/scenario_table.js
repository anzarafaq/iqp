/**
 * Request data from the server and create a table
 */
/* Declare global variable columnNames, it can be used later for column sorting and searching*/
var columnNames = null;
var flextable = 
{
	url: null,
	method : 'GET',
	dataType: 'json',
	colModel :[]
	/* [
		{display: 'ISO', name : 'iso', width : 40, sortable : true, align: 'center'},
		{display: 'Name', name : 'name', width : 180, sortable : true, align: 'left'},
		{display: 'Printable Name', name : 'printable_name', width : 120, sortable : true, align: 'left'},
		{display: 'ISO3', name : 'iso3', width : 130, sortable : true, align: 'left', hide: true},
		{display: 'Number Code', name : 'numcode', width : 80, sortable : true, align: 'right'}
		] */,
	/*buttons : [
		{name: 'Add', bclass: 'add', onpress : null},
		{name: 'Delete', bclass: 'delete', onpress : null},
		{separator: true}
		], */
	searchitems : [
		/*{display: 'ISO', name : 'iso'},
		{display: 'Name', name : 'name', isdefault: true}*/
		],
	sortname:null,
	sortorder: "asc",
	usepager: true,
	resizable: false,
	page : 1,
	title: "Scenario Table",
	useRp: true,
	rpOptions: [15, 50, 100],
	rp: 15,
	showTableToggleBtn: false,
	width: 955,
	height: 240,
	onSuccess : attachToolTip

};
	function drawToolTip(td,e)
{
	var offset = jQuery(td).offset();
  	//e.stopPropagation();
  	var data = jQuery(td).find("div").html();
  	var wide = 6  * data.length;
  	var leftoffset = offset.left -( (wide - jQuery(td).width()) / 2 );
  	jQuery("#tooltip").show().offset({left : leftoffset ,top : offset.top }).html(data).width(wide);
}

function attachToolTip()
{
	var cellData = null;
	$("#scenario_tables").find("tbody").find("tr").each(function()
	{
		jQuery(this).find("td").each(function(){
			
			
				jQuery(this).mouseover(function(e)
				{
					if( (jQuery.trim(jQuery(this).find("div").html()).length * 6) > (jQuery(this).width()))
					{
					drawToolTip(this,e);	
					jQuery("#tooltip").mouseleave(function(){
						jQuery(this).hide();		
					});
					} //END IF
		});
	});
});
}
function createScenarioTableHeaders(name, args, container) {
		//$("#datepicker").datepicker();
				 /* First get the table headers */
				 
				$.getJSON('/scenario_header_table_data_source/'+name+"/",function (json) {
					$.each(json, function(key, val) {
						flextable.colModel.push(
						 	{
							display : wordFormatting(val," "),
							name : val,
							width : parseInt(val.length)*6 < 100 ? 100 :parseInt(val.length)*6,
							sortable : true,
							align : 'center'
							});
							
						flextable.searchitems.push(
							{
								display : wordFormatting(val,"&nbsp;"),
								name : val
							}
							);
						//window.tableheaders = json;
				});
				flextable.sortname = json[0];
				flextable.title = "<h3 style = 'color :#0070A3; margin: 0px'> " + wordFormatting(name," ") + " Summary" + "</h3>"
				columnNames = json;
				createScenarioTable(name, args, container,columnNames);
		});
	}


function createScenarioTable(name, args, container,headers)
{
				window.scenarioName = name; //we need this global object for exporting
				//window.tableUrl is bar clicks
				window.tableUrl = flextable.url = groupBy?'/scenario_table_data_source/'+name+"/?&headers="+columnNames+'&groupBy='+groupBy+'&match=like':'/scenario_table_data_source/'+name+"/?&headers="+columnNames+'&match=like';
				$("#scenario_tables").flexigrid(
					flextable
				);
}

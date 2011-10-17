
/**
 * Request data from the server and create a table
 */
/* Declare global variable columnNames, it can be used later for column sorting and searching*/
var columnNames = null;
var trendExists = true;
var dateConversionColumn = 6;
var flextable = 
{
	url: null,
	method : 'GET',
	dataType: 'json',
	colModel :
	 [] ,
	/*buttons : [
		{name: 'Add', bclass: 'add', onpress : null},
		{name: 'Delete', bclass: 'delete', onpress : null},
		{separator: true}
		], */
	
	sortname:'stats_percentage',
	sortorder: "desc",
	usepager: true,
	resizable: false,
	rpOptions: [15, 25, 50],
	title: "",
	useRp: true,
	rp: 15,
	showTableToggleBtn: false,
	width: 665,
	height: 415,
	onSuccess : addLinksAndDate //call addliknks after building the table
};

function createSubcategoryTable(name, args, container) 
{
		window.subCategoryName = name //we need this global object for exporting
		var filter =getParameterByName('filter');
		if (filter == ('Stats' || 'Features'))
		{
			flextable.colModel.push(
				{display: '', name : '',hide: true},
				{display: 'Scenario', name : 'name', width : 330, sortable : true, align: 'left'},
				{display: 'Current Count', name : 'current', width : 100, sortable : true, align: 'center'},
				{display: 'Last Refreshed', name : 'refreshtime', width : 200, sortable : true, align: 'center'}
			);
			flextable.sortname = 'name';
			flextable.sortorder = "asc";
			trendExists = false;
			dateConversionColumn = 3;
			flextable.rp = 25;
		}
		else
		{
			flextable.colModel.push(
				{display: '', name : '',hide: true},
				{display: 'Scenario', name : 'name', width : 180, sortable : true, align: 'left'},
				{display: 'Current Count', name : 'current', width : 70, sortable : true, align: 'center'},
				{display: 'Total Count', name : 'stats_total', width : 70, sortable : true, align: 'center'},
				{display: 'Percentage Of Total', name : 'stats_percentage', width : 100, sortable : true,align: 'center'},
				{display: 'Trend', name : 'trend', width : 70, sortable : true, align: 'center'},
				{display: 'Last Refreshed', name : 'refreshtime', width : 100, sortable : true, align: 'center'}
			);
		}
		if(filter)
		{
		flextable.url = "/sub_category_table_data_source/"+name+"/"+"?filter="+filter;
		}
		else
		{
		flextable.url = "/sub_category_table_data_source/"+name+"/";
		}
		flextable.title = "<h4 style = 'text-align:center;color :#0070A3; margin: 0px'> " + name + " Summary" + "</h4>"
		$("#subcategory_table").flexigrid(
				flextable
		);		
}
	function drawToolTip(td,e)
{
	var offset = jQuery(td).offset();
  	//e.stopPropagation();
  	var data = jQuery(td).find("div").html();
  	var wide = 7  * data.length;
  	var leftoffset = offset.left -( (wide - jQuery(td).width()) / 2 );
  	jQuery("#tooltip").show().offset({left : leftoffset ,top : offset.top }).html(data).width(wide);
}
function attachToolTip()
{
	var cellData = null;
	$("#subcategory_table").find("tbody").find("tr").each(function()
	{
		jQuery(this).find("td").eq(1).mouseover(function(e)
				{
					var href = jQuery(this).siblings().eq(0).find("div").html();
					if( (jQuery.trim(jQuery(this).find("div").html()).length * 6) > (jQuery(this).width()))
					{
					drawToolTip(this,e);
					jQuery("#tooltip").click(function(e)
					{
						document.location.href = "./"+href+"/?";
					});
					/*mouseleave(function(){
						jQuery(this).hide();		
					});*/
					} //END IF
		});

});
}

function addLinksAndDate(flextable)
{
		$("#subcategory_table").find("tbody").find("tr").each(function()
			{
				jQuery(this).css("cursor","pointer");
				$(this).click(function()
				{	 
					 document.location.href = "./"+$(this).find("div").html()+"/?";
				});
				if(trendExists) //only apply if trend column exists
				{
					var trend = $(this).find("td").eq(5).find("div");
					if ( parseInt( trend.html() ) > 0)
					{
						upImage = new Image(); 
						upImage.src = "/static/images/green-up.png";
						trend.html(upImage);
					}
					else if(parseInt( trend.html() ) < 0)
					{
						downImage = new Image(); 
						downImage.src = "/static/images/red-down.png";
						trend.html(downImage);
					}
					else
					{
						equalImage = new Image(); 
						equalImage.src = "/static/images/equal-icon.png";
						trend.html(equalImage);
					}
				}
				var dateCell = $(this).find("td").eq(dateConversionColumn).find("div");
				var unixTime = parseInt($(dateCell).html());
				var date = new Date(unixTime * 1000);
				$(dateCell).html(date.toDateString());			
			}
		);
		attachToolTip();
}

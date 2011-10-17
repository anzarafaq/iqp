$(document).ready(function(){
/*
 * jQuery BBQ: Back Button & Query Library - v1.3pre - 8/26/2010
 * http://benalman.com/projects/jquery-bbq-plugin/
 * 
 * Copyright (c) 2010 "Cowboy" Ben Alman
 * Dual licensed under the MIT and GPL licenses.
 * http://benalman.com/about/license/
 */
(function($,r){var h,n=Array.prototype.slice,t=decodeURIComponent,a=$.param,j,c,m,y,b=$.bbq=$.bbq||{},s,x,k,e=$.event.special,d="hashchange",B="querystring",F="fragment",z="elemUrlAttr",l="href",w="src",p=/^.*\?|#.*$/g,u,H,g,i,C,E={};function G(I){return typeof I==="string"}function D(J){var I=n.call(arguments,1);return function(){return J.apply(this,I.concat(n.call(arguments)))}}function o(I){return I.replace(H,"$2")}function q(I){return I.replace(/(?:^[^?#]*\?([^#]*).*$)?.*/,"$1")}function f(K,P,I,L,J){var R,O,N,Q,M;if(L!==h){N=I.match(K?H:/^([^#?]*)\??([^#]*)(#?.*)/);M=N[3]||"";if(J===2&&G(L)){O=L.replace(K?u:p,"")}else{Q=m(N[2]);L=G(L)?m[K?F:B](L):L;O=J===2?L:J===1?$.extend({},L,Q):$.extend({},Q,L);O=j(O);if(K){O=O.replace(g,t)}}R=N[1]+(K?C:O||!N[1]?"?":"")+O+M}else{R=P(I!==h?I:location.href)}return R}a[B]=D(f,0,q);a[F]=c=D(f,1,o);a.sorted=j=function(J,K){var I=[],L={};$.each(a(J,K).split("&"),function(P,M){var O=M.replace(/(?:%5B|=).*$/,""),N=L[O];if(!N){N=L[O]=[];I.push(O)}N.push(M)});return $.map(I.sort(),function(M){return L[M]}).join("&")};c.noEscape=function(J){J=J||"";var I=$.map(J.split(""),encodeURIComponent);g=new RegExp(I.join("|"),"g")};c.noEscape(",/");c.ajaxCrawlable=function(I){if(I!==h){if(I){u=/^.*(?:#!|#)/;H=/^([^#]*)(?:#!|#)?(.*)$/;C="#!"}else{u=/^.*#/;H=/^([^#]*)#?(.*)$/;C="#"}i=!!I}return i};c.ajaxCrawlable(0);$.deparam=m=function(L,I){var K={},J={"true":!0,"false":!1,"null":null};$.each(L.replace(/\+/g," ").split("&"),function(O,T){var N=T.split("="),S=t(N[0]),M,R=K,P=0,U=S.split("]["),Q=U.length-1;if(/\[/.test(U[0])&&/\]$/.test(U[Q])){U[Q]=U[Q].replace(/\]$/,"");U=U.shift().split("[").concat(U);Q=U.length-1}else{Q=0}if(N.length===2){M=t(N[1]);if(I){M=M&&!isNaN(M)?+M:M==="undefined"?h:J[M]!==h?J[M]:M}if(Q){for(;P<=Q;P++){S=U[P]===""?R.length:U[P];R=R[S]=P<Q?R[S]||(U[P+1]&&isNaN(U[P+1])?{}:[]):M}}else{if($.isArray(K[S])){K[S].push(M)}else{if(K[S]!==h){K[S]=[K[S],M]}else{K[S]=M}}}}else{if(S){K[S]=I?h:""}}});return K};function A(K,I,J){if(I===h||typeof I==="boolean"){J=I;I=a[K?F:B]()}else{I=G(I)?I.replace(K?u:p,""):I}return m(I,J)}m[B]=D(A,0);m[F]=y=D(A,1);$[z]||($[z]=function(I){return $.extend(E,I)})({a:l,base:l,iframe:w,img:w,input:w,form:"action",link:l,script:w});k=$[z];function v(L,J,K,I){if(!G(K)&&typeof K!=="object"){I=K;K=J;J=h}return this.each(function(){var O=$(this),M=J||k()[(this.nodeName||"").toLowerCase()]||"",N=M&&O.attr(M)||"";O.attr(M,a[L](N,K,I))})}$.fn[B]=D(v,B);$.fn[F]=D(v,F);b.pushState=s=function(L,I){if(G(L)&&/^#/.test(L)&&I===h){I=2}var K=L!==h,J=c(location.href,K?L:{},K?I:2);location.href=J};b.getState=x=function(I,J){return I===h||typeof I==="boolean"?y(I):y(J)[I]};b.removeState=function(I){var J={};if(I!==h){J=x();$.each($.isArray(I)?I:arguments,function(L,K){delete J[K]})}s(J,2)};e[d]=$.extend(e[d],{add:function(I){var K;function J(M){var L=M[F]=c();M.getState=function(N,O){return N===h||typeof N==="boolean"?m(L,N):m(L,O)[N]};K.apply(this,arguments)}if($.isFunction(I)){K=I;return J}else{K=I.handler;I.handler=J}}})})(jQuery,this);
//end jQuery BBQ
	// place the slider buttons
	if($('li.headlink').length > 7)
	{
		$('.menu-sliders').show();
		$('.menu-sliders').eq(0).addClass('menu-slider-inactive');
		window.extraBars = $('li.headlink').length - 7;
	}
	else
	{
		$('#cssdropdown').find('.headlink:first').addClass('corner-left-menu').parent().find('.headlink:last').addClass('corner-right-menu');
	}
	//slide down
    $('li.headlink').hover(
	function() { 
				var ul = $(this).find('ul');
				$(ul).css({'display':'block'});
				//ul.css({'display':'block'}).slideDown(500); 
				var ul_height = $(ul).height();
				$('#topbar').height(514+35);//css({'height':(514+35) + 'px'});
				if(ul_height >= 514)
				{
					//var topbarheight = (514+35) + 'px';
					
					$(ul).css({'display':'block','width':'136px','overflow-y': 'scroll','height':'514px'}).height(514);
					//$(ul).addClass('ul_hover');
					//$('#topbar').css({'height':topbarheight});
				}
				else
				{
					//var topbarheight = 35 + 'px';
					$(ul).css({'display':'block','height':ul_height,'overflow-y': 'hidden','width':'131px'}).height(ul_height);
					//$('#topbar').css({'height':topbarheight});
				}
				},
	function() { $('ul', this).css({'display':'none','width':'136px','height':'auto'}); 
	$('#topbar').height(35);} 
	);
	//border styling
	//$('#cssdropdown').find('.headlink:first').addClass('corner-left-menu').parent().find('.headlink:last').addClass('corner-right-menu');
	$('li.headlink').each(function(){
		$(this).find('ul').find('li:last').addClass('bottom-menu-item');
	});
	// mouse over styling
	$('li.headlink a,li.headlink > ul > li > a').mouseover(
		function()
		{
			$(this).removeClass('non-mouseover').addClass('menu-item-hover');
		}).mouseleave(
		function()
		{
			$(this).removeClass('menu-item-hover').addClass('non-mouseover');
		}
	);
	
	//Menu slider for left
	var leftSliderClick = function()
	{
		if(!jQuery('#cssdropdown').is(':animated'))
		{
		var ulPos = parseInt(jQuery('#cssdropdown').css('left'));
		if(ulPos >= -396 && ulPos < 0 )
		{
			jQuery('#cssdropdown').
			animate({
				left:String(ulPos + (window.extraBars)*(132))+'px'
				},300)
			
			$(this).addClass('menu-slider-inactive');
			jQuery('#menu-right-slider').removeClass('menu-slider-inactive').addClass('menu-slider-active');
		}
		/*if(ulPos >= -132)
		{
			
		}
		else
		{
			$('.menu-sliders').eq(1).removeClass('menu-slider-inactive');	
		}*/
		}
	}
	jQuery('#menu-left-slider').bind('mouseover',leftSliderClick);
	//Menu slider for right
	jQuery('#menu-right-slider').mouseover(function()
	{
		//jQuery(this).unbind('click');
		if(!jQuery('#cssdropdown').is(':animated'))
		{
		var ulPos = parseInt(jQuery('#cssdropdown').css('left'));
		if(ulPos <= 0 && ulPos > -396)
		{
			jQuery('#cssdropdown').
			animate({
				left:String(ulPos + (window.extraBars)*(-132))+'px'
				},{duration : 300,queue : false},function()
				{
					
				});
				$(this).addClass('menu-slider-inactive');
				jQuery('#menu-left-slider').addClass('menu-slider-active').removeClass('menu-slider-inactive');
		}
		/*if(ulPos <= (window.extraBars-1)*(-132))
		{
			$(this).addClass('menu-slider-inactive');
		}
		else
		{
			//$('.menu-sliders').eq(0).removeClass('menu-slider-inactive');
		} */
	  }
	});
});

// highlight tabs
function highlightTabs(category_name)
	{
		$('li.headlink').each(function(){
			if($(this).find("a").html() == category_name)
			{
				$(this).removeClass('non-mouseover').addClass('selected-tab').find("a:first").css("color","#fff");
			}
		});
	}
	
// capitalize first letter and remove underscores
String.prototype.capitalize = function(){
   return this.replace( /(^|\s)([a-z])/g , function(m,p1,p2){ return p1+p2.toUpperCase(); } );
  };

function wordFormatting(text,joinBy)
{
	var words = String(text).split("_");
	for(var i = 0; i< words.length;i++)
	{
		words[i] = words[i].toLowerCase(); // first convert all to lowercase
		words[i] = words[i].capitalize(); // convert only the first letter to capitals
		//words[i].charAt(0).toUpperCase();
	}
	var newWord = words.join(joinBy);
	return newWord;	
}

function getParameterByName(name)
{
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regexS = "[\\?&]" + name + "=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.href);
  if(results == null)
    return null;
  else
    return decodeURIComponent(results[1].replace(/\+/g, " "));
}

function customSortAsc(a,b) {
    if(a[window.customTableSortBy] < b[window.customTableSortBy])
    	return 1;
    else if (a[window.customTableSortBy] > b[window.customTableSortBy])
    	return -1;
    else
    	return 0
}

function customSortDesc(a,b) {
    if(a[window.customTableSortBy] > b[window.customTableSortBy])
    	return 1;
    else if (a[window.customTableSortBy] < b[window.customTableSortBy])
    	return -1;
    else
    	return 0
}

function drawTable(sortby) //initially data comes from category main chart ajax source, use the same one to create table
{
	var data = window.tableData;
	window.customTableSortBy = sortby;
	data.sort(customSortAsc)
	var rows = [];
	window.tableHeaders = [
							{	name : 'Application',
								sortDir : null,
								abbr : 'Application'
							},
							{	name :'No of Scenarios',
								sortDir : null,
								abbr : 'No Of Scenarios'
							},
							{	name :'No of Issues',
								sortDir : "asc",
								abbr : 'No Of Issues'
							}
						];
	flextable = 
	{
		colModel : [
                        {display: 'Application', name : 'Application',abbr : 'Application',width : 210, align: 'center'},
                        {display: 'No Of Scenarios', name : 'No Of Scenarios',abbr : 'No Of Scenarios',width : 210, /* sortable : true,*/ align: 'center'},
                        {display: 'No Of Issues', name : 'No Of Issues',abbr : 'No Of Issues',width : 210, /* sortable : true ,*/ align: 'center'}
                ],
        resizable: false,
		width: 668,
		height: 'auto',
		title : "<h4 style = 'text-align:center;color :#111; margin: 0px'> " + window.tableTitle + " Summary" + "</h4>"
	};
	jQuery(data).each(function(key,val)
	{
		rows.push('<tr><td>'+ val[0]+'</td>'+
					'<td>' + val[1]+'</td>'+
					'<td>' + val[2]+'</td>'+
					'</tr>');
	});
	jQuery("#application-table").find("tbody").append(rows.join('')).parent().flexigrid( flextable );
	jQuery(".hDivBox").find("table").find("thead").find("tr").find("th").eq(2).addClass("sorted").find('div').addClass('sdescs');
	//Asked to remove this
	/*var rows = jQuery("#application-table").find("tbody").find("tr");
	jQuery.each(rows,function(index,value)
	{
		jQuery(rows[index]).find('td').eq(2).addClass('sorted');
	});*/
}

function setSortDirNull(index)
{
	for(var i = 0; i < window.tableHeaders.length ; i++)
	{
		window.tableHeaders[i].sortDir = null;
	}
}

function reDrawTable(hIndex,tableHead)
{
	var prevIndex = window.customTableSortBy;
	window.customTableSortBy = hIndex;
	var data = window.tableData;
	switch(window.tableHeaders[hIndex].sortDir)
	{
		case null:
			data.sort(customSortAsc);
			setSortDirNull(hIndex);
			window.tableHeaders[hIndex].sortDir = "asc"
			break;
		case "asc":
			data.sort(customSortDesc);
			setSortDirNull(hIndex);
			window.tableHeaders[hIndex].sortDir = "desc"
			break;
		case "desc":
			data.sort(customSortAsc);
			setSortDirNull(hIndex);
			window.tableHeaders[hIndex].sortDir = "asc"
			break;
	}
	var rows = jQuery("#application-table").find("tbody").find("tr");
	jQuery(data).each(function(index,value)
	{
		jQuery(rows[index]).find("td").each(function(ind,val){
			
			jQuery(this).find("div").text(value[ind]); // change the data
			
			// add the sorted class for the rows
		/*	if(ind == hIndex)
				jQuery(this).addClass("sorted");
			else
				jQuery(this).removeClass("sorted"); */
				
			// add the sorted class for the header
		});
		//jQuery(rows[index]).find("td").eq(hIndex).addClass("sorted").siblings().removeClass("sorted");
	});
	var add = window.tableHeaders[hIndex].sortDir;
	var remove;
	if(window.tableHeaders[hIndex].sortDir == 'asc')
		remove = 'desc';
	else
		remove = 'asc'
	jQuery(".hDivBox").find("table").find("thead").find("tr").find("th").eq(hIndex).
			addClass("sorted").
			find('div').
			addClass('s'+ add + 's').
			removeClass('s'+ remove + 's').
			parent().
			siblings().
			each(function()
			{
				$(this).removeClass("sorted").find('div').removeClass('sascs sdescs');
			});
}

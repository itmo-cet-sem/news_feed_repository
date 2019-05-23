var last_element_shown = 13; 

var bricks_wrapper = document.getElementsByClassName('bricks-wrapper')[0];

var pagination = document.getElementsByClassName('pagination')[0];
var json = JSON.parse(unescape(pagination.dataset.json));
pagination.addEventListener('click',function_show_several_more);

function function_show_several_more() {
	var i;
	for(i=0;i<8;i++) function_showmore();
	var script = document.createElement('script');
	script.innerHTML = 'function_delete_all_unavailable_images();'; 
	document.getElementsByTagName('body')[0].appendChild(script);
}


function function_showmore() {
	if(last_element_shown<(json.length-1)) {
		last_element_shown++;
		var new_element = build_brick(json[last_element_shown]);
		bricks_wrapper.appendChild(new_element);

		new_element.classList.remove('animate-this');

		var containerBricks = $('.bricks-wrapper');

		containerBricks.masonry( 'addItems', new_element );
		containerBricks.imagesLoaded().progress( function() {
			containerBricks.masonry('layout');
		})

		$WIN = $(window);
		$WIN.on('resize', function() {	
			// remove animation classes	
			new_element.classList.remove('animate-this');
			new_element.classList.remove('animated');
			new_element.classList.remove('fadeInUp');
		});
	} else {
		pagination.classList.add('hidden');
	}
}

function build_brick(json) {
	var article = document.createElement('article');
	article.className = 'brick entry format-standard animate-this';
	article.innerHTML = '\
	       <div class=\'entry-thumb\'>\
		  <a href=\'' + json['href'] + '\' class=\'thumb-link\'>\
			  <img src=\'' + json['image'] + '\' data-imagetotest=\'1\'>\
		  </a>\
	       </div>\
	       <div class=\'entry-text\'>\
		<div class=\'entry-header\'>\
			<div class=\'entry-meta\'>\
				<span class=\'cat-links\'>\
					<a href=\'#\'>' + json['source'] + '</a> \
					<!--<a href=\'#\'>Photography</a> -->\
				</span>\
			</div>\
			<h1 class=\'entry-title\'><a href=\'' + json['href'] + '\' target=\'_blank\'>' + json['title'] + '</a></h1>\
		</div>\
						<div class=\'entry-excerpt\'>\
							' + json['description'] + '\
						</div>\
	       </div>\
	';
	return article;
}

function build_brick_quote(json) {
	return '\
		<article class=\'brick entry format-quote animate-this\' >\
	       <div class=\'entry-thumb\'>                  \
			   <blockquote>\
				<a class=\'blockquote-with-link\' href=\'' + json['href'] + '\' target=\'_blank\'><p>' + json['title'] + '</p></a>\
				<cite>' + json['source'] + '</cite> \
			   </blockquote>	          \
	       </div>\
		</article> <!-- end article -->\
';
}



const http = require('http');
const fs = require('fs');
const path = require('path');

exports.build_section = function (request,response,url_parsed,dir_data) {
        response.writeHead(200);
		var content = '';

		var header = new Promise((resolve, reject) => {
			 fs.readFile('header.html',callback_file)
			function callback_file(error, content) {
				if(error) reject(error);
				else resolve(content);
			}
		});
		var footer = new Promise((resolve, reject) => {
			 fs.readFile('footer.html',callback_file)
			function callback_file(error, content) {
				if(error) reject(error);
				else resolve(content);
			}
		});
		var json_pnp = new Promise((resolve, reject) => {
			 fs.readFile(dir_data + 'pnp_page_data.json',callback_file)
			function callback_file(error, content) {
				if(error) reject(error);
				else resolve(content);
			}
		});
		var json_tass = new Promise((resolve, reject) => {
			 fs.readFile(dir_data + 'tass_page_data.json',callback_file)
			function callback_file(error, content) {
				if(error) reject(error);
				else resolve(content);
			}
		});
		var json_rg = new Promise((resolve, reject) => {
			 fs.readFile(dir_data + 'rg_page_data.json',callback_file)
			function callback_file(error, content) {
				if(error) reject(error);
				else resolve(content);
			}
		});
		var json_duma = new Promise((resolve, reject) => {
			 fs.readFile(dir_data + 'duma_page_data.json',callback_file)
			function callback_file(error, content) {
				if(error) reject(error);
				else resolve(content);
			}
		});
	//	var json_section1 = new Promise((resolve, reject) => {
	//		 fs.readFile(dir_data + 'duma_page_data.json',callback_file)
	//		function callback_file(error, content) {
	//			if(error) reject(error);
	//			else resolve(content);
	//		}
	//	});

		Promise.all([header,footer,json_pnp,json_tass,json_rg,json_duma]).then(array_results => {
			console.log('all promises');
			var i;

			content = array_results[0] + page_header + brick_entry;
			var json_pnp = JSON.parse(array_results[2]);
			var json_tass = JSON.parse(array_results[3]);
			var json_rg = JSON.parse(array_results[4]);
			var json_duma = JSON.parse(array_results[5]);

			var json = [];
			for(i=0;i<json_pnp.length;i++){
				json_pnp[i]['source'] = 'Парламентская газета';
				json_pnp[i]['text'] = null;
				json.push(json_pnp[i]);
			}
			for(i=0;i<json_tass.length;i++){
				json_tass[i]['source'] = 'ТАСС';
				json_tass[i]['text'] = null;
				json.push(json_tass[i]);
			}
			for(i=0;i<json_rg.length;i++){
				json_rg[i]['source'] = 'Российская газета';
				json_rg[i]['text'] = null;
				json.push(json_rg[i]);
			}
			for(i=0;i<json_duma.length;i++){
				json_duma[i]['source'] = 'Государственная Дума';
				json_duma[i]['text'] = null;
				json.push(json_duma[i]);
			}
			json_pnp = json_tass = json_rg = json_duma = null;
			shuffle(json);
			
			var array_jsons = [];
			array_jsons.push(json[0]);
			array_jsons.push(json[1]);
			array_jsons.push(json[2]);
			content+=build_entry_content(array_jsons);
			for(i=3;i<14;i++)
				if(i==5||i==7) content+=build_brick_quote(json[i]);
				else content += build_brick(json[i]);
			content+=set_brick_exit(json);
			content+=array_results[1];
			response.end(content, 'utf-8');
		});
}

function build_entry_content(array_jsons) {
	var content = '';
	var i;
	for(i=0;i<array_jsons.length;i++) content+='\
							<li>\
								<div class=\'featured-post-slide\'>\
									<div class=\'post-background\' style=\'background-image:url("' + array_jsons[i]['image'] + '");\'></div>\
									<div class=\'overlay\'></div>\
									<div class=\'post-content\'>\
										<ul class=\'entry-meta\'>\
												<!--<li>September 06, 2016</li>--> \
												<li><a href=\'#\' >' + array_jsons[i]['source'] + '</a></li>\
											</ul>\
										<h1 class=\'slide-title\'><a href=\'' + array_jsons[i]['href'] + '\' target=\'_blank\' title=\'\'>' + array_jsons[i]['title'] + '</a></h1> \
									</div>\
								</div>\
							</li> <!-- /slide -->\
';

	return '\
		<div class=\'brick entry featured-grid animate-this\'>\
			<div class=\'entry-content\'>\
				<div id=\'featured-post-slider\' class=\'flexslider\'>\
						<ul class=\'slides\'>\
						' + content + '\
						</ul> <!-- end slides -->\
					</div> <!-- end featured-post-slider -->\
			</div> <!-- end entry content -->\
		</div>\
	';
}

function build_brick(json) {
	return '\
		<article class=\'brick entry format-standard animate-this\'>\
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
			</article> <!-- end article -->\
';
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

const brick_entry = '\
   <section id=\'bricks\' class=\'with-top-sep\'>\
	<div class=\'row masonry\'>\
		<!-- brick-wrapper -->\
	 <div class=\'bricks-wrapper\'>\
		<div class=\'grid-sizer\'></div>\
';

// TODO: cleanup here. Pagination went to another button.
function set_brick_exit(json) {
	return '\
	 </div> <!-- end brick-wrapper --> \
	</div> <!-- end row -->\
	<div class=\'row\'>\
		<nav class=\'pagination\' data-json=\'' + escape(JSON.stringify(json)) + '\'>\
			<div class=\'button-secondary\'>See More</div>\
		     <!--<span class=\'page-numbers prev inactive\'>Prev</span>\
			<span class=\'page-numbers current\'>1</span>\
			<a href=\'?page=2&\' class=\'page-numbers\'>2</a>\
		      <a href=\'#\' class=\'page-numbers\'>3</a>\
		      <a href=\'#\' class=\'page-numbers\'>4</a>\
		      <a href=\'#\' class=\'page-numbers\'>5</a>\
		      <a href=\'#\' class=\'page-numbers\'>6</a>\
		      <a href=\'#\' class=\'page-numbers\'>7</a>\
		      <a href=\'#\' class=\'page-numbers\'>8</a>\
		      <a href=\'#\' class=\'page-numbers\'>9</a>\
			<a href=\'#\' class=\'page-numbers next\'>Next</a>-->\
	      </nav>\
	</div>\
   </section> <!-- end bricks -->\
';
}
const brick_exit = '\
	 </div> <!-- end brick-wrapper --> \
	</div> <!-- end row -->\
	<div class=\'row\'>\
		<nav class=\'pagination\'>\
			<div class=\'button-secondary\'>See More</div>\
		     <!--<span class=\'page-numbers prev inactive\'>Prev</span>\
			<span class=\'page-numbers current\'>1</span>\
			<a href=\'?page=2&\' class=\'page-numbers\'>2</a>\
		      <a href=\'#\' class=\'page-numbers\'>3</a>\
		      <a href=\'#\' class=\'page-numbers\'>4</a>\
		      <a href=\'#\' class=\'page-numbers\'>5</a>\
		      <a href=\'#\' class=\'page-numbers\'>6</a>\
		      <a href=\'#\' class=\'page-numbers\'>7</a>\
		      <a href=\'#\' class=\'page-numbers\'>8</a>\
		      <a href=\'#\' class=\'page-numbers\'>9</a>\
			<a href=\'#\' class=\'page-numbers next\'>Next</a>-->\
	      </nav>\
	</div>\
   </section> <!-- end bricks -->\
';

const page_header = '\
	<!-- page header\
   ================================================== -->\
	<section id=\'page-header\'>\
		<div class=\'row current-cat\'>\
			<div class=\'col-full\'>\
				<h1>Category: General</h1>\
			</div>\
		</div>\
	</section>\
   <!-- masonry\
   ================================================== -->\
';

function shuffle(sourceArray) {
    for (var i = 0; i < sourceArray.length - 1; i++) {
        var j = i + Math.floor(Math.random() * (sourceArray.length - i));

        var temp = sourceArray[j];
        sourceArray[j] = sourceArray[i];
        sourceArray[i] = temp;
    }
    return sourceArray;
}

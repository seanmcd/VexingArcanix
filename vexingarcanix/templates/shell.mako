<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Vexing Arcanix: Learn Your Deck</title>
	## This description is just for the main page - it should probably be a def() later.
	<meta name="description" content="You can use Vexing Arcanix to get better at Magic, Pokemon, and other card games by answering questions about your deck. ">
	
    </head>
    <body>
        ## Prompt IE 6/7/8 users to install Chrome Frame. This is not an IE-friendly site.
        ## * chromium.org/developers/how-tos/chrome-frame-getting-started
	<!--[if lt IE 9]><p class=chromeframe>Internet Explorer is not advanced enough to reliably process this web site. You may encounter problems. <a href="http://browsehappy.com/">Upgrade to a different browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">install Google Chrome Frame</a> to experience this site as intended.</p><![endif]-->
	<header>
            <div style="width: 80%; margin: auto;">
                <div id="masthead" style="margin: auto; text-align: center;">
                    <h1>Welcome to Vexing Arcanix</h1>
		</div>
            </div>
	</header>

        <div role="main">
	    <%block name="main_content" />
	</div>

	<footer>

	</footer>

	## Put JavaScript at the bottom for fast page loading. Grab jQuery from
	## the Google CDN with a protocol relative URL, but fall back to a local
	## if that fails.
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
	<script>window.jQuery || document.write('<script src="js/libs/jquery-1.7.2.min.js"><\/script>')</script>

    </body>
</html>

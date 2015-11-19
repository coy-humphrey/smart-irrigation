<!doctype html>
<html>
    <head>
        <title></title>
    </head>


    <asset:stylesheet src="home.css" />
    <body>

        <!--content is a wrapper for the whole page  -->
        <div class="content">
            <!--UCSC logo and smart irrigation title -->
            <div class="site-header" role="banner">
                <div class="name-row">
                    <div class="campus-name">
                        <a class="campus-logo-image">
                            <!--Scalable image used -->
                            <img src="${resource(dir:'images',file:'ucsc-logo.svg')}"/>
                        </a>
                    </div>
                    <div class="site-name">
                        <p class= "title-text">Smart Irrigation</p>
                    </div>
                </div>
            </div>
            <div class="home-content">
                <div class="summary-wrapper">
                    <div class="summary-box">
                        <div class="summary-title">
                            Summary
                        </div>
                        <div class="summary-content">
                            Information <br>
                            from <br>
                            backend <br>
                            database <br>
                            will <br>
                            go <br>
                            here <br>
                        </div>
                    </div>
                </div>
                <div class="weather-wrapper">
                    <div class="weather-forecast">
                        <!--Thanks to http://blog.forecast.io/forecast-embeds/ -->
                        <iframe id="forecast_embed" type="text/html" frameborder="0" height="245" width="495px"
                                src="http://forecast.io/embed/#lat=36.954871&lon=-122.048429&name=Natural Bridges High"> </iframe>
                    </div>
                </div>
            </div>
        </div>
        <script>
</script>
    </body>
</html>
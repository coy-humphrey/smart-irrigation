<!doctype html>
<html>
    <head>
        <title></title>
        <g:set var="x" value="${Data}"/>
        <!-- Load Google Charts API and fill with data from IndexController -->
        <script type="text/javascript"
                src="https://www.google.com/jsapi?autoload={
            'modules':[{
              'name':'visualization',
              'version':'1',
              'packages':['corechart']
            }]
          }"></script>
        ​

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
                            Some summary content here
                        </div>
                    </div>
                </div>

                <div>
                    <article class="tabs">

                        <section id="tab1">
                            <h2><a href="#tab1">Water Usage</a></h2>
                            <p><div id="waterTime_chart" style="width: 900px; height: 500px"></div></p>
                        </section>

                        <section id="tab2">
                            <h2><a href="#tab2">Crop Temperature</a></h2>
                            <p><div id="tempTime_chart" style="width: 900px; height: 500px"></div></p>
                        </section>
                    </article>
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
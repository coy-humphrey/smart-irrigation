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
        <script type="text/javascript">
            google.load('visualization', '1.1', {packages: ['line']});
            google.setOnLoadCallback(drawChart);
            function drawChart() {
                // Use Groovy to transform UserData and hand it to the chart creation JS.
                <%
                def day = [];
                def month = [];
                def year = [];

                def temp = [];
                def s1 = [];
                def s2 = [];
                def s3 = [];
                for(int i = 0; i < x.length(); i++){
                StringTokenizer s = new StringTokenizer(x[i].getAt("time").toString(), '-')
                    year[i] = s.nextToken()
                    month[i] = s.nextToken()
                    day[i] = s.nextToken().substring(0,2)

                    temp[i] = x[i].getAt("temp")
                    s1[i] = x[i].getAt("s1")
                    s2[i] = x[i].getAt("s2")
                    s3[i] = x[i].getAt("s3")
                } %>

                // Google Charts API (chart constructor)

                var waterTimeTable = [];
                var tempTimeTable = [];
                var day = ${day};
                var month = ${month};
                var year = ${year};

                var temp = ${temp};
                var s1 = ${s1};
                var s2 = ${s2};
                var s3 = ${s3};

                // Construct Water Time Table
                waterTimeTable[0] = ['Year', 'S1', 'S2', 'S3'];
                for(var i = 1; i < ${x.length()}; i++){
                    waterTimeTable[i] = ["" + year[i] + "-" + month[i] + "-" + day[i], s1[i], s2[i], s3[i]];
                }

                // Construct Temperature Time Table
                tempTimeTable[0] = ['Year', 'Temperature'];
                for(var i = 1; i < ${x.length()}; i++){
                    tempTimeTable[i] = ["" + year[i] + "-" + month[i] + "-" + day[i], temp[i]];
                }

                // Draw Water Usage vs. Time table
                var data = google.visualization.arrayToDataTable(waterTimeTable);
                var options = {
                    title: 'Moisture information',
                    legend: { position: 'bottom' }
                };
                var chart = new google.visualization.LineChart(document.getElementById('waterTime_chart'));
                chart.draw(data, options);

                // Draw Temperature Usage vs. Time table
                var data = google.visualization.arrayToDataTable(tempTimeTable);
                var options = {
                    title: 'Temperature information',
                    legend: { position: 'bottom' }
                };
                var chart = new google.visualization.LineChart(document.getElementById('tempTime_chart'));
                chart.draw(data, options);
            }
        </script>
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
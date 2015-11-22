<!doctype html>
<html>
    <head>
        <title></title>
        <g:set var="x" value="${Data}"/>
        <!-- Load Google Charts API and fill with data from HomeController -->
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
            google.setOnLoadCallback(drawChart);
            function drawChart() {
                <%
                def day = [];
                def month = [];
                def year = [];

                def s1 = [];
                def s2 = [];
                def s3 = [];
                for(int i = 0; i < x.length(); i++){
                StringTokenizer s = new StringTokenizer(x[i].getAt("time").toString(), '-')
                    year[i] = s.nextToken()
                    month[i] = s.nextToken()
                    day[i] = s.nextToken().substring(0,2)

                    s1[i] = x[i].getAt("s1")
                    s2[i] = x[i].getAt("s2")
                    s3[i] = x[i].getAt("s3")
                } %>

                var arr = [];
                var day = ${day};
                var month = ${month};
                var year = ${year};

                var s1 = ${s1};
                var s2 = ${s2};
                var s3 = ${s3};

                arr[0] = ['Year', 'S1', 'S2', 'S3'];
                for(var i = 1; i < ${x.length()}; i++){
                    arr[i] = ["" + year[i] + "-" + month[i] + "-" + day[i], s1[i], s2[i], s3[i]];
                    console.log(arr[i]);
                }
                console.log(arr);


                var data = google.visualization.arrayToDataTable(arr);
        var options = {
            title: 'Sensor information',
            curveType: 'function',
            legend: { position: 'bottom' }
        };
        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
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
                            ${x[0].getAt("time")}
                        </div>
                        <div class="summary-content">
                            <script type="text/javascript">
                            </script>
                        </div>
                    </div>
                </div>
                <div id="curve_chart" style="width: 900px; height: 500px"></div>
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
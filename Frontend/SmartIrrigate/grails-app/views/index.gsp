<!doctype html>
<html>
    <head>
        <title></title>
        <asset:javascript src="processing.min.js"/>

        <g:set var="x" value="${Data}"/>
    </head>


    <asset:stylesheet src="home.css" />
    <body>
            <!--content is a wrapper for the whole page  -->
            <div class="content">
                <div class = "animation-banner">
                    <script type="text/processing" data-processing-target="processing-canvas">
                            // colors:          lt blue  red      yellow   orange   violet   turkoise    purpe dk green
                            color[] palette = { #0099CC, #E00000, #CCFF00, #FF3300, #AD1BF7, #1BE3F7, #FEFCFF, #003300 };

                            int[][] flowers; // 2D array of flowers positions, size and color
                            int step = 0; // frame number, used for rotation

                            // constants
                            int X = 0, Y = 1, SIZE = 2, COLOR = 3, GROW = 4; // used for flower data
                            int MAX_FLOWERS = 10; // change to a higher number if running in Java
                            int MAX_FLOWER_SIZE = 50;
                            int NUM_PETALS = 10;
                            float PETAL_ANGLE = 2.0 * PI / float(NUM_PETALS);
                            int[] WINDOW_SIZE = { 1280, 720 };

                            // initial setup
                            void setup() {
                                // size(WINDOW_SIZE[0], WINDOW_SIZE[1], P2D);  // uncomment this line and comment out the next line if running on Java
                                size(1600, 100); // Processing export to JS barfs on the line above so changed to this
                                flowers = new int[MAX_FLOWERS][5];  // array of flowers
                            }

                            void draw() {
                                background(palette[0]);
                                step++;
                                for (int i = 0; i < MAX_FLOWERS; i++) {
                                    // draw flower if created
                                    if (flowers[i][X] > 0) {
                                        // grow or shrink flowers
                                        if (flowers[i][GROW] < 1) { // shrinking state
                                            flowers[i][SIZE] -=0.50; // increase the number to increase speed (for shrinking)
                                            if (flowers[i][SIZE] <= 0) {
                                                flowers[i][X] = 0; // mark flower as destroyed
                                                continue;  // skip drawing it
                                            }
                                        }else{ // growing state
                                            flowers[i][SIZE] = flowers[i][SIZE] + 0.50; // increase in the number to increase the speed (for growing)
                                            if (flowers[i][SIZE] >= MAX_FLOWER_SIZE) {
                                                flowers[i][SIZE] = MAX_FLOWER_SIZE;
                                                flowers[i][GROW] = -1; // change direction of growth next frame
                                            }
                                        }

                                        // draw stem
                                        fill(#00CC00);
                                        rect(flowers[i][X] - 3, flowers[i][Y], 5, height);

                                        // draw center of flower
                                        ellipseMode(CENTER);
                                        fill(#EEEEEE);
                                        ellipse(flowers[i][X], flowers[i][Y], 30, 30);

                                        //draw petals rotating around center of flower
                                        ellipseMode(CORNER);
                                        pushMatrix(); // save default rotation and coordinate state
                                        translate(flowers[i][X], flowers[i][Y]); // set rotation center to middle of flower
                                        fill(palette[flowers[i][COLOR]]);
                                        // each flower has a different starting angle, and rotation changes slightly each frame
                                        rotate((i/float(MAX_FLOWERS - 1)) * PI / 2.0 + step * PI / 50.0);
                                        for (int j = 0; j < 80; j++) {
                                            rotate(PETAL_ANGLE); // default is 2.0 * PI / 10.0, evenly spaced for 10 petals around flower
                                            ellipse(-15, 15, 30, 30 + flowers[i][SIZE]);
                                        }
                                        popMatrix(); // restore rotation and coordinate state
                                    }else{
                                        // 2% chance per frame of empty flower array position creating a new flower
                                        if (random(1) < 0.02){
                                            flowers[i][X] = int(random(width - MAX_FLOWER_SIZE / 2.0) + MAX_FLOWER_SIZE / 2.0);
                                            flowers[i][Y] = int(random(height - MAX_FLOWER_SIZE / 2.0) + MAX_FLOWER_SIZE / 2.0);
                                            flowers[i][SIZE] = 0;
                                            flowers[i][COLOR] = int(random(6)) + 1;
                                            flowers[i][GROW] = 1;
                                        }
                                    }
                                }
                            }
                        </script>
                    <canvas id="processing-canvas"> </canvas>
                </div>
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
                <div class="logout-btn">
                    <form name="logout" method="POST" action="/logout">
                    <input type="submit" value="logout"></form>
                </div>
                <div class="summary-wrapper">
                    <div class="summary-box">
                        <div class="summary-title">
                            Summary
                        </div>
                        <div class="summary-content">
                            Some summary content here
                            Some summary content here
                            Some summary content here
                            <br>
                            <br>
                            <a class="button" href="#popup1">Moisture Readings</a>
                            <br>
                            <br>
                            <br>
                            <a class="button" href="#popup2">Soil Temp Readings</a>
                        </div>
                    </div>
                </div>
                <!-- Load Google Charts API and fill with data from IndexController -->
                <script type="text/javascript"
                        src="https://www.google.com/jsapi?autoload={
                        'modules':[{
                        'name':'visualization',
                        'version':'1',
                        'packages':['corechart']
                        }]}">
                </script>​
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
                <div class="weather-wrapper">
                    <div class="weather-forecast">
                        <!--Thanks to http://blog.forecast.io/forecast-embeds/ -->
                        <iframe id="forecast_embed" type="text/html" frameborder="0" height="245" width="495px"
                                src="http://forecast.io/embed/#lat=36.954871&lon=-122.048429&name=Natural Bridges High"> </iframe>
                    </div>
                </div>
                <div id="popup1" class="overlay">
                    <div class="popup">
                        <h2>Soil Moisture Content Readings</h2>
                        <a class="close" href="#">×</a>
                        <div class="content">
                            <div class="graphs">
                                <article class="tabs">
                                        <h2><a href="#tab1"></a></h2>
                                        <p><div id="waterTime_chart" style="width: 900px; height: 500px"></div></p>
                                </article>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="popup2" class="overlay">
                    <div class="popup">
                        <h2>Soil Temperature Readings</h2>
                        <a class="close" href="#">×</a>
                        <div class="content">
                            <div class="graphs">
                                <article class="tabs">
                                    <h2><a href="#tab2"></a></h2>
                                    <p><div id="tempTime_chart" style="width: 900px; height: 500px"></div></p>
                                </article>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
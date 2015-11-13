<!doctype html>
<html>
    <head>   </head>
        <asset:stylesheet src="main.css" />
        <body onload="document.f.username.focus();">

            <!--content is a wrapper for the whole page -->
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

                <div class="content">
                    <br>
                    <a href="/">Index</a>
                    <br>
                    <g:link controller="home">Home (Login Required)</g:link>
                </div>
            </div>

        </body>
</html>

<!doctype html>
<html>
    <head>   </head>
        <asset:stylesheet src="main.css" />
        <body>
            <div class="content">
                <div class="site-header" role="banner">
                    <div class="name-row">
                        <div class="campus-name">
                            <a class="campus-logo-image">
                                <img src="${resource(dir:'images',file:'ucsc-logo.svg')}" />
                            </a>
                        </div>
                        <div class="site-name">
                            <p class= "title-text">Smart Irrigation</p>
                        </div>
                    </div>
                </div>
                <div class="login-content">
                    <div class="login-wrap">
                        <div class="login-box">
                            <form id="login" name="login">
                                <label>Username:</label>
                                <br>
                                <input name="user-name" id="user-name" title="Enter your username here" type="text" value>
                                <br>
                                <label>Password:</label>
                                <br>
                                <input name="password" id="password" title="Enter your password here" type="password">
                                <br>
                                <input class="login-btn" name="Submit" type="submit" value="Login to Smart Irrigation">
                            </form>
                        </div>
                    </div>
                </div>
            </div>

        </body>
</html>

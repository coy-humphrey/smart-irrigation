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

                <!--login-content is a wrapper for the login section/second half of page -->
                <div class="login-content">

                    <!--login-wrap allows enclosure to have the darker color surrounded by white -->
                    <div class="login-wrap">
                        <div class="login-box">

                            <h3>Login with Username and Password</h3><form name="f" action="/login" method="POST">
                             <table>
                                <tbody>
                                <tr><td>User:</td><td>
                                <input name="username" value="" type="text"></td></tr>
                                <tr><td>Password:</td><td>
                                <input name="password" type="password"></td></tr>
                                <tr><td colspan="2"><input name="submit" value="Login" type="submit"></td></tr>
                              </tbody></table>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

        </body>
</html>

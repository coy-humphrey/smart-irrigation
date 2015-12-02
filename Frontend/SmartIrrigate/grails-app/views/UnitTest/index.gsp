<%@ page import="example.UnitTestController" %>
<html>
<body>
Welcome to the unit testing controller<br>
        The following tests will be run:<br>
        Test Login Controler:<br>

        Test DatabaseClient:<br>

        Test IndexController:<br>

        Test MyUserDetails:<br><br><br>


        <div>
            <p>Login Controller Test and MyUserDetails Test:

            <p>User from Login Controller: &nbsp;&nbsp;&nbsp;${example.UnitTestController.LoginControllerUnitTest()}
            <p>Currently Logged in user: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${IndexUser}

            <%def String LoginResult  = (example.UnitTestController.LoginControllerUnitTest().equals(IndexUser))? "Success": "Failure" %>
            <p> Test ${LoginResult}
        </div>

<br><br>
        <div>
            <p>Database Client Test and Index Controller Test:

            <p>Json from Range Function: &nbsp;&nbsp;&nbsp;${example.UnitTestController.DatabaseClientTest()}
            <p>Json from Get Data Function: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${DBStringData}

            <%def String DBResult  =  (example.UnitTestController.DatabaseClientTest().equals(DBStringData))? "Success": "Failure"%>
            <p> Test ${DBResult}
        </div>

<br><br>
</body>
</html>
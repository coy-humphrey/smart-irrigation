package example

import org.grails.web.json.JSONArray

/**
 * Created by Yli-Ihminen on 11/30/2015.
 */
class UnitTestController {



    def index(){
        String IndexCurrentUser = IndexController.CurrentUser.toString()
        String DBTestGetData = DatabaseClient.GetData("/get_field?field=s1&field=s2&start=%222014-10-06_06:27:29%22&end=%222015-12-22_14:04:29%22&table=" + IndexController.CurrentUser.dbTable)
        return [IndexUser: IndexCurrentUser, DBStringData: DBTestGetData]
    }

    // Unit Test for the Login Controller
    public static String LoginControllerUnitTest(){
        // Test getCurrentUser()
        MyUserDetails current = LoginController.getCurrentUser()
        return current.toString()
    }

    public static String DatabaseClientTest(){
        String jsonString = "ERROR"
        String[] fields = ["s1", "s2"]
        try{
            JSONArray test =  DatabaseClient.DataWithDateRange("2014-10-06_06:27:29", "2015-12-22_14:04:29", fields, IndexController.CurrentUser.dbTable)
            jsonString = test.toString()
        } catch(MalformedURLException e) {
            jsonString = e.toString()
        } catch (IOException e ) {
            jsonString = e.toString()
        }
        return jsonString
    }
}

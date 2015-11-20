package example

import grails.converters.JSON
import org.grails.web.json.JSONArray
import org.grails.web.json.JSONObject

class HomeController {

    static MyUserDetails CurrentUser;
    static JSONArray UserData;

    def index() {
        GetUserData()
        //CurrentUser = User.findByUsername("ian")
        //render CurrentUser.username
    }

    private void GetUserData(){
       // Get current logged in user
        CurrentUser = LoginController.getCurrentUser()

       // Query Database for number of sensors
       // <STUB> API CALL HERE
       // Placeholder code
        int numSensors = 3
        //</STUB>

       // Generate fields array
        def fields = new String[numSensors]
        for(int i = 0; i < numSensors; i++) {
            fields[i] = "s" + (i+1)
        }

        // Calculate dates needed for DB lookup
        // <STUB>
        def date1 = "2014-10-06_06:27:29"
        def date2 = "2015-12-22_14:04:29"


       //Call DataWithRange to query for sensor data in the given range
        UserData = DatabaseClient.DataWithDateRange(date1, date2, fields)

    }
}

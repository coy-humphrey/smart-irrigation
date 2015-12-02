package example

import grails.converters.JSON
import org.grails.web.json.JSONArray
import org.grails.web.json.JSONObject

import java.text.DateFormat
import java.text.SimpleDateFormat

class IndexController {

    static MyUserDetails CurrentUser;
    static JSONArray UserData;

    def index() {
        // Get and return userdata for currently logged in user.
        GetUserData()
        [Data: UserData]
    }

    private void GetUserData(){
       // Get current logged in user
        CurrentUser = LoginController.getCurrentUser()

       // Query Database for number of sensors
       // <STUB> API CALL HERE
       // Placeholder code
        int numSensors = 3
        //</STUB>

       // Generate wanted fields array
        def fields = new String[numSensors + 1]
        int i;
        for(i = 0; i < numSensors; i++) {
            fields[i] = "s" + (i+1)
        }
        fields[i] = "temp"

        // Calculate dates needed for DB lookup (1 year maximum)
        // Use format for start and end %Y-%m-%d_%H:%M:%S
        DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd_HH:mm:ss")

        // Calendar is created to format the dates for the chart. Currently they are hardcoded, but can be
        // changed by changing the following variables



        Calendar cal = Calendar.getInstance()
        int granularity = Calendar.MONTH;
        int range = 2;

        cal.add(granularity, range)
        def end = dateFormat.format(cal.getTime())
        cal.add(granularity, -range)
        def start = dateFormat.format(cal.getTime())


       //Call DataWithRange to query for sensor data in the given range
        UserData = DatabaseClient.DataWithDateRange(start, end, fields, CurrentUser.dbTable)
    }
}

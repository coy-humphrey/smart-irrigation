package example

import grails.converters.JSON
import org.grails.web.json.JSONArray
import org.grails.web.json.JSONObject

import java.text.DateFormat
import java.text.SimpleDateFormat

class HomeController {

    static MyUserDetails CurrentUser;
    static JSONArray UserData;

    def index() {
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

       // Generate fields array
        def fields = new String[numSensors + 1]
        int i;
        for(i = 0; i < numSensors; i++) {
            fields[i] = "s" + (i+1)
        }

        fields[i] = "temp"
        // Calculate dates needed for DB lookup (1 year maximum)
        // Use format for start and end %Y-%m-%d_%H:%M:%S
        DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd_HH:mm:ss")
        Calendar cal = Calendar.getInstance()
        cal.add(Calendar.MONTH, 6)
        def end = dateFormat.format(cal.getTime())
        cal.add(Calendar.MONTH, -6)
        def start = dateFormat.format(cal.getTime())


       //Call DataWithRange to query for sensor data in the given range
        UserData = DatabaseClient.DataWithDateRange(start, end, fields)
    }
}

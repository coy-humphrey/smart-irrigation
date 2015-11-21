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
<<<<<<< HEAD
        render "hello world!"
=======
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
        def fields = new String[numSensors]
        for(int i = 0; i < numSensors; i++) {
            fields[i] = "s" + (i+1)
        }

        // Calculate dates needed for DB lookup (1 year maximum)
        // Use format for start and end %Y-%m-%d_%H:%M:%S
        DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd_HH:mm:ss")
        Calendar cal = Calendar.getInstance()
        def end = dateFormat.format(cal.getTime())
        println end
        cal.add(Calendar.YEAR, -2)
        def start = dateFormat.format(cal.getTime())
        println start

        //def start = "2014-10-06_06:27:29"
       //def end = "2015-12-22_14:04:29"


       //Call DataWithRange to query for sensor data in the given range
        UserData = DatabaseClient.DataWithDateRange(start, end, fields)
        println UserData
>>>>>>> f9607ce71ee7ccb692591692c818ca6e7794b665
    }
}

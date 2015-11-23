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
<<<<<<< HEAD:Frontend/SmartIrrigate/grails-app/controllers/example/HomeController.groovy
<<<<<<< HEAD
        render "hello world!"
=======
=======
        // Get and return userdata for currently logged in user.
>>>>>>> 853ce3ebe011d9e1f790c322c7e709869f544e32:Frontend/SmartIrrigate/grails-app/controllers/example/IndexController.groovy
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
        Calendar cal = Calendar.getInstance()
        cal.add(Calendar.MONTH, 2)
        def end = dateFormat.format(cal.getTime())
        cal.add(Calendar.MONTH, -2)
        def start = dateFormat.format(cal.getTime())


       //Call DataWithRange to query for sensor data in the given range
        UserData = DatabaseClient.DataWithDateRange(start, end, fields)
<<<<<<< HEAD:Frontend/SmartIrrigate/grails-app/controllers/example/HomeController.groovy
        println UserData
>>>>>>> f9607ce71ee7ccb692591692c818ca6e7794b665
=======
>>>>>>> 853ce3ebe011d9e1f790c322c7e709869f544e32:Frontend/SmartIrrigate/grails-app/controllers/example/IndexController.groovy
    }
}

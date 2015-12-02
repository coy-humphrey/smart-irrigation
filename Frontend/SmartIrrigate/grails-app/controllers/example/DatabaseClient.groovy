package example

import grails.io.IOUtils
import grails.converters.JSON
import org.grails.web.json.JSONArray
import org.grails.web.json.JSONObject

/**
 * Created by Yli-Ihminen on 11/20/2015.
 */
class DatabaseClient {

    // HTTP address for the database hosted by
    final static String DATABASE_ROOT = "http://smart-irrigation.elasticbeanstalk.com"

    // Example request:
    // get_field?field=s1&field=s2&start=%222014-10-06_06:27:29%22&end=%222015-12-22_14:04:29%22&table=entry


    // Constructs request for getting sensor data from database through PythonAPI query
    static JSONArray DataWithDateRange(String date1, String date2, String[] fields, String dbTable){
        String field = "";
        Iterator<String> it = fields.iterator()
        while(it.hasNext()){
            field += "field=" + it.next()
            if(it.hasNext()){
                field += "&"
            }
        }
        def request = "/get_field?" + field + "&start=%22" + date1 + "%22&end=%22" + date2 + "%22&table="+ dbTable

        GetData(request);
    }

    // Accepts request as argument.
    // Queries the PythonAPI for database access given the request string.
    static JSONArray GetData(String request) {
        try {
            String webPage = DATABASE_ROOT + request;
            String name = "bob";
            String password = "secret";

            String authString = name + ":" + password;
            byte[] authEncBytes = Base64.getEncoder().encode(authString.getBytes());
            String authStringEnc = new String(authEncBytes);

            URL url = new URL(webPage);
            URLConnection urlConnection = url.openConnection();
            urlConnection.setRequestProperty("Authorization", "Basic " + authStringEnc);
            InputStream is = urlConnection.getInputStream();

            return JSON.parse(is, "UTF-8")
        }
        catch(MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e ) {
            e.printStackTrace();
        }
    }
}

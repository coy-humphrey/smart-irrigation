package example

/**
 * Created by Yli-Ihminen on 11/19/2015.
 */
class DatabaseClient {

    static String test() {

        try{
        String webPage = "http://smart-irrigation.elasticbeanstalk.com/get_field?field=s1&field=s2&start=%222014-10-06_06:27:29%22&end=%222015-12-22_14:04:29%22&table=entry";
        String name = "bob";
        String password = "secret";

        String authString = name + ":" + password;
        byte[] authEncBytes = Base64.encoder.encode(authString.getBytes());
        String authStringEnc = new String(authEncBytes);

        URL url = new URL(webPage);
        URLConnection urlConnection = url.openConnection();
        urlConnection.setRequestProperty("Authorization", "Basic " + authStringEnc);
        InputStream is = urlConnection.getInputStream();
        InputStreamReader isr = new InputStreamReader(is);

        int numCharsRead;
        char[] charArray = new char[1024];
        StringBuffer sb = new StringBuffer();
        while ((numCharsRead = isr.read(charArray)) > 0) {
            sb.append(charArray, 0, numCharsRead);
        }
        String result = sb.toString();
            return result;
        }
        catch(MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e ) {
            e.printStackTrace();
        }
        return "ERROR";

    }
}

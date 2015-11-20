package example

import grails.io.IOUtils

class HomeController {

    static MyUserDetails CurrentUser;
    static String info;

    def index() {
        GetUserData()
        render info
        //CurrentUser = User.findByUsername("ian")
        //render CurrentUser.username
    }

    private void GetUserData(){
       CurrentUser = LoginController.getCurrentUser()
        info = DatabaseClient.test();

    }
}

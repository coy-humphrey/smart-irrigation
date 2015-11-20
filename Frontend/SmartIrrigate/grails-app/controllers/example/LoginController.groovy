package example

import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.User;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.security.core.userdetails.UserDetailsService;

/**
 * Created by Yli-Ihminen on 11/12/2015.
 */
class LoginController {
    def index(){

    }

    // Get current user from LoginController
    @RequestMapping(value="/login", method = RequestMethod.GET)
    static public User getCurrentUser(){
        User user = (User)SecurityContextHolder.getContext().getAuthentication().getPrincipal()
        return user
    }
}

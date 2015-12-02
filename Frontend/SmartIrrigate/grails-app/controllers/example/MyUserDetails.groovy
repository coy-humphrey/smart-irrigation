package example

import org.springframework.security.core.GrantedAuthority
import org.springframework.security.core.userdetails.User

/**
 * Created by Yli-Ihminen on 11/19/2015.
 */
public class MyUserDetails extends GrailsUser {

    final String dbTable

    MyUserDetails(String username, String password, boolean enabled,
                  boolean accountNonExpired, boolean credentialsNonExpired,
                  boolean accountNonLocked,
                  Collection<GrantedAuthority> authorities,
                  long id, String dbTable) {
        super(username, password, enabled, accountNonExpired,
                credentialsNonExpired, accountNonLocked, authorities, id)

        this.dbTable = dbTable
    }

    public String toString(){
        return super.toString() + " dbTable:" + this.dbTable
    }
}

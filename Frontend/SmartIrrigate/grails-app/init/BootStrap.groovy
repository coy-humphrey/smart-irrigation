import example.*
import grails.util.Environment

class BootStrap {

    def init = { servletContext ->

        switch (Environment.current) {
            case Environment.DEVELOPMENT:

                def user = new User(username: 'ian', password: 'password', enabled: true, testing: 'penis', accountExpired: false, accountLocked: false, credentialsExpired: false ).save(failOnError: true)
                def admin = new User(username: 'admin', password: 'admin', enabled: true, testing: 'notpenis', accountExpired: false, accountLocked: false, credentialsExpired: false ).save(failOnError: true)

                def roleUser = new Authority(authority: 'ROLE_USER').save(failOnError: true)
                def roleAdmin = new Authority(authority: 'ROLE_ADMIN').save(failOnError: true)

                UserAuthority.create(user, roleUser, true)
                UserAuthority.create(admin, roleUser, true)
                UserAuthority.create(admin, roleAdmin, true)


                break
            case Environment.PRODUCTION:

                break
        }
    }
    def destroy = {
    }
}

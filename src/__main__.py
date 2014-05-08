import getpass
import aerochat.database

if __name__ == '__main__':
    print "Welcome to AeroChat!"

    db = aerochat.database.MessageDatabase(getpass.getuser(), "./messages")

    # TODO this is just a test
    db.publish_message("Test message")
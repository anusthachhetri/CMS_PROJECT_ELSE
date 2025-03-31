class MongoDBRouter:
    """
    A router to control all database operations on models for MongoDB.
    """
 
    def db_for_read(self, model, **hints):
        """
        Directs read operations for json_app models to the MongoDB database.
        """
        if model._meta.app_label == 'json_app':
            return 'mongo'
        return None
 
    def db_for_write(self, model, **hints):
        """
        Directs write operations for json_app models to the MongoDB database.
        """
        if model._meta.app_label == 'json_app':
            return 'mongo'
        return None
 
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allows relations only between models in the same database.
        """
        if obj1._meta.app_label == 'contenttypes' or obj2._meta.app_label == 'contenttypes':
            return True
        db_list = ('mongo', 'default')
        if obj1._meta.app_label in db_list and obj2._meta.app_label in db_list:
            return True
        return None
 
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensures that migrations for json_app go to the mongo database and other apps to the default db.
        """
        system_apps = ['auth', 'contenttypes', 'admin', 'sessions']
        if app_label in system_apps:
            return db == 'default'
        if app_label == 'json_app':
            return db == 'mongo'
        return db == 'default'
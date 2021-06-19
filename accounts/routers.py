# class DjangoRouter(object):
#     """
#     A router to control all database operations on models in the
#     auth application.
#     """
#
#     def db_for_read(self, model, **hints):
#         """
#         Attempts to read auth models go to auth.
#         """
#         app_list = ('admin', 'auth', 'contenttypes')
#         if model._meta.app_label in app_list:
#             return 'users'
#         return None
#
#     def db_for_write(self, model, **hints):
#         """
#         Attempts to write auth models go to auth.
#         """
#         app_list = ('auth', 'admin', 'contenttypes')
#         if model._meta.app_label in app_list:
#             return 'users'
#         return None
#
#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Allow relations if a model in the auth app is involved.
#         """
#         app_list = ('auth', 'admin', 'contenttypes')
#         if obj1._meta.app_label in app_list and obj2._meta.app_label in app_list:
#             return True
#         return True
#
#     def allow_migrate(self, db, app_label, model=None, **hints):
#         """
#         Make sure the auth app only appears in the 'auth'
#         database.
#         """
#         app_list = ('auth', 'admin', 'contenttypes')
#
#         if app_label in app_list:
#             return db == 'users'
#         return None
#
#
# class MyApp2Router(object):
#
#     def db_for_read(self, model, **hints):
#
#         if model._meta.app_label == 'accounts':
#             return 'users'
#         return None
#
#     def db_for_write(self, model, **hints):
#         if model._meta.app_label == 'accounts':
#             return 'users'
#         return None
#
#     def allow_syncdb(self, db, model):
#         if db == 'users':
#             return model._meta.app_label == 'accounts'
#         elif model._meta.app_label == 'accounts':
#             return False
#         return None
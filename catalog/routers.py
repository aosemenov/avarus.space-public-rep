# class CatalogRouter(object):
#
#     def db_for_read(self, model, **hints):
#
#         if model._meta.app_label == 'catalog':
#             return 'users'
#         return None
#
#     def db_for_write(self, model, **hints):
#         if model._meta.app_label == 'catalog':
#             return 'users'
#         return None
#
#     def allow_syncdb(self, db, model):
#         if db == 'users':
#             return model._meta.app_label == 'catalog'
#         elif model._meta.app_label == 'catalog':
#             return False
#         return None
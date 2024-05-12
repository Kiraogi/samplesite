class BboardDbRouter:
    """
    Роутер баз данных для Django проекта.
    Определяет, к какой базе данных направлять запросы для моделей определенного приложения.
    """

    def db_for_read(self, model, **hints):
        """
        Направляет операции чтения для приложения bboard в базу данных 'other'.
        """
        if model._meta.app_label == 'bboard':
            return 'other'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Направляет операции записи для приложения bboard в базу данных 'other'.
        """
        if model._meta.app_label == 'bboard':
            return 'other'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Разрешает отношения, если оба объекта принадлежат одному приложению.
        """
        if obj1._meta.app_label == 'bboard' or obj2._meta.app_label == 'bboard':
            return True
        elif 'default' in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Определяет, на какую базу данных следует применять миграции.
        """
        if app_label == 'bboard':
            return db == 'other'
        return db == 'default'
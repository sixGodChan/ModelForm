from django.apps import AppConfig


class SixgodConfig(AppConfig):
    name = 'sixgod'

    def ready(self):
        super(SixgodConfig, self).ready()

        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('sg')  # 找寻所有app中的sg.py

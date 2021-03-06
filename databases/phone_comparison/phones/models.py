from django.db import models

# чтобы упростить задачу сбора данных, я поставила в модели
# дефолтными те значения, которые совпадают у всех трёх
# выбранных моделей телефона

# сами модели создаются командой import_phones.py


class Phone(models.Model):
    name = models.CharField(max_length=50)

    price = models.IntegerField()

    screen_technology = models.CharField(max_length=15)
    touchscreen = models.BooleanField(default=True)
    touchscreen_type = models.CharField(max_length=15, default='емкостный')
    multitouch = models.BooleanField(default=True)
    screen_diagonal = models.FloatField()
    display_resolution = models.CharField(max_length=15)
    pixel_density = models.IntegerField(null=True)
    contrast = models.IntegerField(null=True)
    brightness = models.IntegerField(null=True)

    platform = models.CharField(max_length=10)
    OS = models.CharField(max_length=15)

    CPU = models.CharField(max_length=20, null=True)
    n_cores = models.IntegerField(null=True)
    CPU_max_frequency = models.FloatField(null=True)

    cam = models.BooleanField(default=True)
    cam_modules = models.IntegerField(default=1)
    cam_1st_module_resolution = models.IntegerField()
    cam_2nd_module_resolution = models.IntegerField(null=True)
    cam_3rd_module_resolution = models.IntegerField(null=True)
    cam_4th_module_resolution = models.IntegerField(null=True)
    cam_1st_module_aperture = models.FloatField()
    cam_2nd_module_aperture = models.FloatField(null=True)
    cam_3rd_module_aperture = models.FloatField(null=True)
    cam_4th_module_aperture = models.FloatField(null=True)
    front = models.BooleanField(default=True)
    front_resolution = models.IntegerField()
    front_aperture = models.FloatField()
    video_recording = models.BooleanField(default=True)
    video_resolution = models.CharField(max_length=30, null=True)
    front_video_resolution = models.CharField(max_length=30, null=True)
    video_frame_rate = models.CharField(max_length=100, null=True)
    digital_zoom_photo = models.IntegerField(null=True)
    digital_zoom_video = models.IntegerField(null=True)
    optical_zoom_photo = models.IntegerField(null=True)
    optical_zoom_video = models.IntegerField(null=True)
    flash = models.BooleanField(default=True)
    flash_type = models.CharField(max_length=15, default='Светодиодная')
    cam_functions = models.CharField(max_length=300)

    memory = models.FloatField()
    availiable_memory = models.FloatField(null=True)
    RAM = models.FloatField(null=True)
    cartridge = models.BooleanField(default=False)
    cartridge_type = models.CharField(max_length=20, null=True)
    cartridge_max_capacity = models.FloatField(null=True)

    stereo_sound = models.BooleanField(default=False)

    multimedia = models.CharField(
        max_length=30, default='Аудиоплеер, Видеоплеер')
    audio_formats = models.CharField(max_length=150, null=True)
    video_formats = models.CharField(max_length=50, null=True)

    sensors = models.CharField(max_length=100)
    sensors_additional = models.CharField(max_length=100)

    cellular_standards = models.CharField(max_length=20)
    GSM_ranges = models.CharField(
        max_length=20, default='1800, 1900, 850, 900')
    UMTS_3G_ranges = models.CharField(max_length=50)
    LTE_ranges = models.CharField(max_length=150)
    internet = models.CharField(max_length=50)
    n_sim = models.IntegerField()
    sim_type = models.CharField(max_length=10)
    sim_work_mode = models.CharField(max_length=15, null=True)

    wireless = models.CharField(max_length=30)
    wifi = models.CharField(max_length=50)
    wifi_direct = models.BooleanField(default=False)
    bluetooth = models.FloatField()
    bluetooth_profiles = models.CharField(max_length=10, null=True)
    wired_connection = models.CharField(max_length=10)
    headphone_jack = models.CharField(max_length=10)

    navigation = models.CharField(max_length=100)
    digital_compass = models.BooleanField(default=False)

    battery_type = models.CharField(max_length=10, null=True)
    battery_capacity = models.IntegerField(null=True)
    max_time_wifi = models.IntegerField(null=True)
    max_time_4G_talk = models.IntegerField(null=True)
    max_time_4G = models.IntegerField(null=True)
    max_time_music = models.IntegerField(null=True)
    max_time_video = models.IntegerField(null=True)

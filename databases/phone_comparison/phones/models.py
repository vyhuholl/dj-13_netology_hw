from django.db import models

# чтобы упростить задачу сбора данных, я поставила в модели
# дефолтными те значения, которые совпадают у всех трёх
# выбранных моделей телефона

# сами модели создаются скриптом phones/get_phone_info.py

class Phone(models.Model):
    name = models.CharField(max_length=50)

    price = models.IntegerField()

    screen_technology = models.CharField(max_length=15)
    touchscreen = models.BooleanField(default=True)
    touchscreen_type = models.CharField(max_length=15, default='емкостный')
    multitouch = models.BooleanField(default=True)
    screen_diagonal = models.FloatField()
    display_resolution = models.CharField(max_length=15)
    pixel_density = models.IntegerField()
    contrast = models.IntegerField()
    brightness = models.IntegerField()

    platform = models.CharField(max_length=10)
    OS = models.CharField(max_length=15)

    CPU = models.CharField(max_length=20)
    n_cores = models.IntegerField()
    CPU_max_frequency = models.FloatField()

    cam = models.BooleanField(default=True)
    cam_modules = models.IntegerField(default=1)
    cam_1st_module_resolution = models.IntegerField()
    cam_2nd_module_resolution = models.IntegerField()
    cam_3rd_module_resolution = models.IntegerField()
    cam_4th_module_resolution = models.IntegerField()
    cam_1st_module_aperture = models.FloatField()
    cam_2nd_module_aperture = models.FloatField()
    cam_3rd_module_aperture = models.FloatField()
    cam_4th_module_aperture = models.FloatField()
    front = models.BooleanField(default=True)
    front_resolution = models.IntegerField()
    front_aperture = models.FloatField()
    video_recording = models.BooleanField(default=True)
    video_resolution = models.CharField(max_length=30)
    front_video_resolution = models.CharField(max_length=30)
    video_frame_rate = models.CharField(max_length=100)
    digital_zoom_photo = models.IntegerField()
    digital_zoom_video = models.IntegerField()
    optical_zoom_photo = models.IntegerField()
    optical_zoom_video = models.IntegerField()
    flash = models.BooleanField(default=True)
    flash_type = models.CharField(max_length=15, default='Светодиодная')
    cam_functions = models.CharField(max_length=300)

    memory = models.IntegerField()
    availiable_memory = models.IntegerField()
    RAM = models.IntegerField()
    cartridge = models.BooleanField(default=False)
    cartridge_type = models.CharField(max_length=20)
    cartridge_max_capacity = models.IntegerField()

    stereo_sound = models.BooleanField(default=False)

    multimedia = models.CharField(
        max_length=30, default='Аудиоплеер, Видеоплеер')
    audio_formats = models.CharField(max_length=150)
    video_formats = models.CharField(max_length=50)

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
    sim_work_mode = models.CharField(max_length=15)

    wireless = models.CharField(max_length=30)
    wifi = models.CharField(max_length=30)
    wifi_direct = models.BooleanField(default=False)
    bluetooth = models.FloatField()
    bluetooth_profiles = models.CharField(max_length=10)
    wired_connection = models.CharField(max_length=10)
    headphone_jack = models.CharField(max_length=10)

    navigation = models.CharField(max_length=100)
    digital_compass = models.BooleanField(default=False)

    battery_type = models.CharField(max_length=10)
    battery_capacity = models.IntegerField()
    max_time_wifi = models.IntegerField()
    max_time_4G_talk = models.IntegerField()
    max_time_4G = models.IntegerField()
    max_time_music = models.IntegerField()
    max_time_video = models.IntegerField()

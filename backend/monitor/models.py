# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Abnormaldata(models.Model):
    recordtime = models.DateTimeField(db_column='recordTime', primary_key=True)  # Field name made lowercase.
    data = models.FloatField()
    direction = models.CharField(max_length=10)
    deviceid = models.ForeignKey('Deviceinfo', models.DO_NOTHING, db_column='deviceId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'abnormalData'
        unique_together = (('recordtime', 'direction', 'deviceid'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Deviceinfo(models.Model):
    deviceid = models.CharField(db_column='deviceId', primary_key=True, max_length=20)  # Field name made lowercase.
    devicename = models.CharField(db_column='deviceName', max_length=20)  # Field name made lowercase.
    offset = models.FloatField()
    loweroutlier = models.FloatField(db_column='lowerOutlier')  # Field name made lowercase.
    upperoutlier = models.FloatField(db_column='upperOutlier')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'deviceInfo'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Earthquakeinfo(models.Model):
    earthquakeid = models.CharField(db_column='earthquakeId', primary_key=True, max_length=20)  # Field name made lowercase.
    level = models.FloatField()
    starttime = models.DateField(db_column='startTime')  # Field name made lowercase.
    longitude = models.FloatField()
    latitude = models.FloatField()
    depth = models.FloatField()
    location = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'earthquakeInfo'


class Historicaldata(models.Model):
    time = models.DateTimeField(primary_key=True)
    xdata = models.FloatField(db_column='xData')  # Field name made lowercase.
    ydata = models.FloatField(db_column='yData')  # Field name made lowercase.
    zdata = models.FloatField(db_column='zData')  # Field name made lowercase.
    deviceid = models.ForeignKey(Deviceinfo, models.DO_NOTHING, db_column='deviceId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'historicalData'
        unique_together = (('time', 'deviceid'),)


class Seismicdata(models.Model):
    recordtime = models.DateField(db_column='recordTime', primary_key=True)  # Field name made lowercase.
    xdata = models.FloatField(db_column='xData')  # Field name made lowercase.
    ydata = models.FloatField(db_column='yData')  # Field name made lowercase.
    zdata = models.FloatField(db_column='zData')  # Field name made lowercase.
    deviceid = models.ForeignKey(Deviceinfo, models.DO_NOTHING, db_column='deviceId')  # Field name made lowercase.
    earthquakeid = models.ForeignKey(Earthquakeinfo, models.DO_NOTHING, db_column='earthquakeId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seismicData'


class Supervisorinfo(models.Model):
    supervisorid = models.CharField(db_column='supervisorId', primary_key=True, max_length=20)  # Field name made lowercase.
    supervisorname = models.CharField(db_column='supervisorName', max_length=20)  # Field name made lowercase.
    supervisormail = models.CharField(db_column='supervisorMail', max_length=100)  # Field name made lowercase.
    supervisorphone = models.CharField(db_column='supervisorPhone', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'supervisorInfo'

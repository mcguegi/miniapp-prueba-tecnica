# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Commerce(models.Model):
    k_idcommerce = models.IntegerField(primary_key=True)
    n_commerce = models.CharField(max_length=50)
    o_address = models.CharField(max_length=200, blank=True, null=True)
    o_telephone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commerce'


class Order(models.Model):
    k_idorder = models.IntegerField(primary_key=True)
    f_dateorder = models.DateField()
    n_tokenorder = models.CharField(max_length=100)
    n_tokenpayment = models.CharField(max_length=100, blank=True, null=True)
    n_status = models.CharField(max_length=3)
    v_total = models.IntegerField()
    k_iddetail = models.IntegerField(blank=True, null=True)
    k_idcommerce = models.ForeignKey(Commerce, models.DO_NOTHING, db_column='k_idcommerce', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'


class Orderdetail(models.Model):
    k_iddetail = models.IntegerField(primary_key=True)
    q_quantity = models.IntegerField()
    v_subtotal = models.IntegerField()
    k_idorder = models.ForeignKey(Order, models.DO_NOTHING, db_column='k_idorder', blank=True, null=True)
    k_idproduct = models.ForeignKey('Product', models.DO_NOTHING, db_column='k_idproduct', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orderdetail'


class Product(models.Model):
    k_idproduct = models.IntegerField(primary_key=True)
    n_product = models.CharField(max_length=50)
    n_description = models.CharField(max_length=200, blank=True, null=True)
    k_idcommerce = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'

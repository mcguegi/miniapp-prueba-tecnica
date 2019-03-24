from django.db import models

class Product(models.Model):
    k_idproduct = models.IntegerField(primary_key=True)
    n_product = models.CharField(max_length=50)
    n_description = models.CharField(max_length=200, blank=True, null=True)
    v_price = models.IntegerField()

    def __str__(self):
        return str(self.k_idproduct)

class Customer(models.Model):
    k_id = models.CharField(primary_key=True, max_length=50)
    k_idtype = models.CharField(max_length=3)
    n_name = models.CharField(max_length=50)
    n_lastname = models.CharField(max_length=50)
    o_email = models.CharField(max_length=50, blank=True, null=True)


class Orderbill(models.Model):
    k_idorderbill = models.IntegerField(primary_key=True)
    f_dateorderbill = models.DateField()
    n_tokenorderbill = models.CharField(max_length=100)
    n_tokenpayment = models.CharField(max_length=200, blank=True, null=True)
    n_status = models.CharField(max_length=3)
    v_total = models.IntegerField()
    k = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)


class Orderbilldetail(models.Model):
    k_iddetail = models.IntegerField(primary_key=True)
    q_quantity = models.IntegerField()
    v_subtotal = models.IntegerField()
    k_idorderbill = models.ForeignKey(
        Orderbill, on_delete=models.CASCADE, db_column='k_idorderbill', blank=True, null=True)
    k_idproduct = models.ForeignKey(
        Product, on_delete=models.CASCADE, db_column='k_idproduct', blank=True, null=True)


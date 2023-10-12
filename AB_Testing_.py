import pandas as pd
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Görev 1:  Veriyi Hazırlama ve Analiz Etme

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

dataframe_control = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Control Group")
dataframe_test = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Test Group")

df_control = dataframe_control.copy()
df_test = dataframe_test.copy()

# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.
def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)

pd.plotting.scatter_matrix(df_control)
plt.show()

pd.plotting.scatter_matrix(df_test)
plt.show()

# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

df_test["group"] = "test"
df_control["group"] = "control"
df = pd.concat([df_control,df_test], axis=0,ignore_index=True)
df.head()

# Görev 2:  A/B Testinin Hipotezinin Tanımlanması

#ADIM1 - HİPOTEZ KUR

#H0: M1 =  M2 (kontrol grubu ile test grubu arsaında ortalama satın alma ortalamaları arasında fark yoktur.)
#H1: M1 != M2 (kontrol grubu ile test grubu arsaında ortalama satın alma ortalamaları arasında fark vardır.)

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz

df.groupby("group").agg({"Purchase": "mean"})

# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.
# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz
# Normallik Varsayımı :
#H0: Normallik varsayımı sağlanmaktadır.
#H1: Normallik varsayımı sağlanmamaktadır.

test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print("Tes stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

test_stat, pvalue = shapiro(df.loc[df["group"] == "test", "Purchase"])
print("Tes stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

#p value değeri ikisinde de 0.05 den büyük ise H0 reddedilemez yani normallik varsayımı sağlanır.

# Varyans Homojenliği :
#H0: Varyans homojenliği sağlanır.
#H1: Varyans homojenliği sağlanmaz.

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print("Tes stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

#p value = 0.108>0.05 ise H0 reddedilemez.Yani varyanslar homojendir.

# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz

#Varsayımların ikisi de sağlandığı için parametrik yöntem kullanılır.
# H0: M1 = M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında ist. ol.anl.fark yoktur.)
# H1: M1 != M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında ist. ol.anl.fark vardır)

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Adım 3: Test sonucunda elde edilen p_valuedeğerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

#p value 0.3493>0.05 ise H0 reddedilemez.Yani kontrol grubu ile test grubu arsaında ortalama satın alma ortalamaları arasında fark yoktur.

# GÖREV 4 : Sonuçların Analizi

#veriler normal dağıldığı ve varyansları homojen olduğu için parametrik yöntem kullandım. ttest_ind fonk kullanarak
#p value değeri hesapladım.Sonuç olarak müşteriye average bidding yöntemi ile maximum bidding yöntemi arasında önemli
#bir farkın olmadığını söylerdim.






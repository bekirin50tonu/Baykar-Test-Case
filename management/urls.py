from django.urls import path

from management.views import ProductionItemApi, ProductionPlaneView, ProductionItemViewDataset, PlaneViewApi, ProductionPlaneViewDataset

urlpatterns = [

    path("planes", PlaneViewApi.as_view(),name="planes"), # uçak tiplerinin alınması sağlanır.
    path("items", ProductionItemApi.as_view(), name="production-item-view"),# parça tipleri ile alakalı bilgiler alınması, silinmesi sağlanır.

    path("dataset/produced",ProductionItemViewDataset.as_view({'get':"list"}), name="production-item-view-dataset"), # dataset olarak listelenecek şekilde üretilen parçalar listelenir.
    path("dataset/montage",ProductionPlaneViewDataset.as_view({'get':"list"}), name="montage-plane-view-dataset"), # uçak üretiminide kullanılan parçaları listeler.
    path("montage", ProductionPlaneView.as_view(), name="production-plane-view"), # montaj yapılacak endpointi içerir.

]

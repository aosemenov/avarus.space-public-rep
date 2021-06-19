from django.urls import path
from . import views

from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('success/', views.FeedBackView.as_view(), name='feedback_view'),
    path('books/', views.DatasetsView, name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
]

urlpatterns += [
    path('mybooks/',  views.DatasetsView, name='my-borrowed'),
    path(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),
    path('myrequests/', views.RequestsByUserListView.as_view(), name='my-requests'),
]

urlpatterns += [
    path('analysis/', views.analysis_view, name='analysis_view'),
    path('cor/', views.CorDatasetsView, name='cor-analysis'),
    path('cor-column/', views.get_column, name='cor-column'),
    path('result/', views.get_name, name='cor-result'),
]

urlpatterns += [
    path('component/', views.CompDatasetsView, name='comp-analysis'),
    path('component-column/', views.get_column_comp, name='comp-column'),
    path('component-result/', views.get_name_comp, name='comp-result'),
]
urlpatterns += [
    path('factor/', views.FactorDatasetsView, name='factor-analysis'),
    path('factor-column/', views.get_column_factor, name='factor-column'),
    path('factor-result/', views.get_name_factor, name='factor-result'),
]
urlpatterns += [
    path('statistics/', views.StatisticsDatasetsView, name='statistics_view'),
    path('statistics-column/', views.get_column_statistics, name='statistics-column'),
    path('statistics-result/', views.get_name_statistics, name='statistics-result'),
]

urlpatterns += [
    path('jacquard/', views.JacquardDatasetsView, name='jacquard-analysis'),
    path('jacquard-result/', views.get_name_jacquard, name='jacquard-result'),
]
urlpatterns += [
    path('species-result/', views.get_name_species, name='species-result'),
    path('plants-amount/', views.get_name_plants, name='plants-amount'),
]
urlpatterns += [
    path('about/', views.AboutView, name='about'),
]



from django.conf.urls import url
from restapi import views

urlpatterns = [
    url(r'problems/$', views.ProblemAPIView.as_view(), name='problems-listcreate'),
    url(r'problems/(?P<pk>\d+)/$', views.ProblemRUDView.as_view(), name='problems-rud'),
    url(r'problems/(?P<problem_id>\d+)/testcases/$', views.TestCaseAPIView.as_view(), name='testcases-listcreate'),
    url(r'problems/(?P<problem_id>\d+)/testcases/(?P<pk>\d+)/$', views.TestCaseRUDView.as_view(), name='testcases-rud'),
    url(r'problems/(?P<problem_id>\d+)/ratings/$', views.RatingAPIView.as_view(), name='ratings-listcreate'),
    url(r'problems/(?P<problem_id>\d+)/ratings/(?P<pk>\d+)$', views.RatingRUDView.as_view(), name='ratings-rud'),
    url(r'problems/(?P<problem_id>\d+)/solutions/', views.SolutionAPIView.as_view(), name='solutions-listcreate'),
    url(r'problems/(?P<problem_id>\d+)/solutions/(?P<pk>\d+)$', views.SolutionRetrieveView.as_view(), name='solutions-retrieve'),
]

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin

from usuarios import views as usuariosViews
from proyectos import views as proyectosViews

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reca.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', usuariosViews.home, name='home'),
    url(r'^registro/$', usuariosViews.Registro.as_view(), name='registro'),
    url(r'^login/$', usuariosViews.Login.as_view(), name='login'),
    url(r'^logout/$', usuariosViews.logout, name='logout'),

    #URL's de proyectos
    url(r'^proyecto/$', proyectosViews.proyectos, name='proyectos'),
    url(r'^proyecto/agregar/$', proyectosViews.AgregarProyecto.as_view(), name='agregar-proyecto'),
    url(r'^proyecto/editar/(?P<id_proyecto>\d{1,})/$', proyectosViews.EditarProyecto.as_view(), name="editar-proyecto"),
    url(r'^proyecto/borrar/(?P<id_proyecto>\d{1,})/$', proyectosViews.borrarProyecto, name="borrar-proyecto"),


)

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	



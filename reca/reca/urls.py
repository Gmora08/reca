from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin

from usuarios import views as usuariosViews
from proyectos import views as proyectosViews
from iteraciones import views as iteracionesViews

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

    #URL's de proyectosusr
    url(r'^proyecto/$', proyectosViews.proyectos, name='proyectos'),
    url(r'^proyecto/agregar/$', proyectosViews.AgregarProyecto.as_view(), name='agregar-proyecto'),
    url(r'^proyecto/editar/(?P<id_proyecto>\d{1,})/$', proyectosViews.EditarProyecto.as_view(), name="editar-proyecto"),
    url(r'^proyecto/borrar/(?P<id_proyecto>\d{1,})/$', proyectosViews.borrarProyecto, name="borrar-proyecto"),

    #URL's de analistas
    url(r'^analistas/$', usuariosViews.analistas, name='analistas'),
    url(r'^analistas/agregar/$', usuariosViews.AgregarAnalista.as_view(), name='agregar-analista'),
    url(r'^analistas/editar/(?P<id_analista>\d{1,})/$', usuariosViews.EditarAnalista.as_view(), name='editar-analista'),
    url(r'^analistas/borrar/(?P<id_analista>\d{1,})/$', usuariosViews.borrarAnalista, name="borrar-analista"),

    #URL's de iteraciones
    url(r'^iteracion/$', iteracionesViews.iteraciones, name='iteraciones'),
    url(r'^iteracion/agregar/$', iteracionesViews.AgregarIteracion.as_view(), name='agregar-iteracion'),
    url(r'^iteracion/editar/(?P<id_iteracion>\d{1,})/$', iteracionesViews.EditarIteracion.as_view(), name='editar-iteracion'),
    url(r'^iteracion/borrar/(?P<id_iteracion>\d{1,})/$', iteracionesViews.borrarIteracion, name="borrar-iteracion"),

)

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	



from django.contrib import admin
from django.urls import path
from core import views  # <-- Importando explicitamente do app 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('novo/', views.novo_pedido, name='novo_pedido'),
    path('cliente/novo/', views.novo_cliente, name='novo_cliente'),
    path('produto/novo/', views.novo_produto, name='novo_produto'),
    path('pedido/<int:pk>/', views.detalhe_pedido, name='detalhe_pedido'),
    path('pedido/<int:pk>/editar/', views.editar_pedido, name='editar_pedido'),
    path('pedido/<int:pk>/mudar-status/<str:novo_status>/', views.mudar_status_pedido, name='mudar_status'),
    path('pedido/<int:pk>/gerar-recibo/', views.gerar_recibo, name='gerar_recibo'),
]
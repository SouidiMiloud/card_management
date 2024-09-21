from django.urls import path
from .views import home, buy, support_tickets, register, user_login, user_logout, authenticate_user, add_hq_card, add_vhq_card, add_dump_card, add_wholesale_card, profile, update_password, shoppings, remove_shopping, new_ticket, ticket_details, reply, close_ticket, add_self_account, proof, add_self_account_shop, add_hq_shop, hq_orders, vhq_orders, dump_orders, wholesale_orders, self_account_orders,hq_detail_cards, vhq_detail_cards, dump_detail_cards, wholesale_detail_cards, self_account_detail_cards, add_dump_shop, add_vhq_shop, add_wholesale_shop, bulk_hq_card, bulk_dump_card, bulk_self_account, bulk_vhq_card, bulk_wholesale_card, add_funds, payment_callback


urlpatterns = [
    path('', home, name='home'),
    path('buy/', buy, name='buy'),
    path('tickets/', support_tickets, name='support_tickets'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('authenticate/', authenticate_user, name='authenticate'),

    path('add_hq_card/', add_hq_card, name='add_hq_card'),
    path('add_vhq_card/', add_vhq_card, name='add_vhq_card'),
    path('add_dump_card/', add_dump_card, name='add_dump_card'),
    path('add_wholesale_card/', add_wholesale_card, name='add_wholesale_card'),
    path('add_hq_shop/<int:card_id>', add_hq_shop, name='add_hq_shop'),
    path('add_vhq_shop/<int:card_id>', add_vhq_shop, name='add_vhq_shop'),
    path('add_dump_shop/<int:card_id>', add_dump_shop, name='add_dump_shop'),
    path('add_wholesale_shop/<int:card_id>', add_wholesale_shop, name='add_wholesale_shop'),
    path('remove_shopping/<int:shopping_id>', remove_shopping, name='remove_shopping'),
    path('shoppings/', shoppings, name='shoppings'),

    path('profile/', profile, name='profile'),
    path('update_password/', update_password, name='update_password'),

    path('new_ticket/', new_ticket, name='new_ticket'),
    path('ticket_details/<int:ticket_id>', ticket_details, name='ticket_details'),
    path('reply/<int:ticket_id>', reply, name='reply'),
    path('close_ticket/<int:ticket_id>', close_ticket, name='close_ticket'),

    path('add_self_account/', add_self_account, name='add_self_account'),
    path('proof/<int:account_id>', proof, name='proof'),
    path('add_self_account_shop/<int:account_id>', add_self_account_shop, name='add_self_account_shop'),

    path('hq_orders/', hq_orders, name='hq_orders'),
    path('vhq_orders/', vhq_orders, name='vhq_orders'),
    path('dump_orders/', dump_orders, name='dump_orders'),
    path('wholesale_orders/', wholesale_orders, name='wholesale_orders'),
    path('self_account_orders/', self_account_orders, name='self_account_orders'),

    path('hq_detail_cards/', hq_detail_cards, name='hq_detail_cards'),
    path('vhq_detail_cards/', vhq_detail_cards, name='vhq_detail_cards'),
    path('dump_detail_cards/', dump_detail_cards, name='dump_detail_cards'),
    path('wholesale_detail_cards/', wholesale_detail_cards, name='wholesale_detail_cards'),
    path('self_account_detail_cards/', self_account_detail_cards, name='self_account_detail_cards'),

    path('bulk_hq_card', bulk_hq_card, name='bulk_hq_card'),
    path('bulk_vhq_card', bulk_vhq_card, name='bulk_vhq_card'),
    path('bulk_dump_card', bulk_dump_card, name='bulk_dump_card'),
    path('bulk_wholesale_card', bulk_wholesale_card, name='bulk_wholesale_card'),
    path('bulk_self_account', bulk_self_account, name='bulk_self_account'),

    path('add_funds/', add_funds, name='add_funds'),
    path('callback', payment_callback, name='callback'),
]
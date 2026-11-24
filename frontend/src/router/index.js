import {createRouter,createWebHistory} from 'vue-router'
export default createRouter({history:createWebHistory(),scrollBehavior:()=>({top:0}),routes:[
 {path:'/',component:()=>import('../views/HomeView.vue')},
 {path:'/search',component:()=>import('../views/KoreanSearchView.vue')},
 {path:'/new',component:()=>import('../views/NewFiguresView.vue')},
 {path:'/makers',component:()=>import('../views/MakersView.vue')},
 {path:'/franchises',component:()=>import('../views/FranchisesView.vue')},
 {path:'/events',component:()=>import('../views/EventsView.vue')},
 {path:'/login',component:()=>import('../views/AccountView.vue')},
 {path:'/figures',component:()=>import('../views/FigureListView.vue')},
 {path:'/figures/:id',component:()=>import('../views/FigureDetailView.vue')},
 {path:'/prices/:id',component:()=>import('../views/PriceCompareView.vue')},
 {path:'/chat/:id?',component:()=>import('../views/AIChatView.vue')},
 {path:'/favorites',component:()=>import('../views/FavoritesView.vue')},
 {path:'/purchases',component:()=>import('../views/PurchasesView.vue')},
 {path:'/status',component:()=>import('../views/DataStatusView.vue')},
 {path:'/:pathMatch(.*)*',redirect:'/'}]})

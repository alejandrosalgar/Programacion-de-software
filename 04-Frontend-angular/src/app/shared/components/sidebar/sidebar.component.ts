import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

declare interface RouteInfo {
    path: string;
    title: string;
    icon: string;
    class: string;
    roles?: string[];
}

export const ROUTES: RouteInfo[] = [
    { path: '/dashboard', title: 'Dashboard',  icon: 'design_app', class: '' },
    { path: '/categorias', title: 'Categorías',  icon:'shopping_basket', class: '', roles: ['admin'] },
    { path: '/usuarios', title: 'Usuarios',  icon:'users_single-02', class: '', roles: ['admin'] },
    { path: '/productos', title: 'Productos',  icon:'shopping_box', class: '' },
    { path: '/pruebas', title: 'Pruebas',  icon:'shopping_box', class: '' },
    { path: '/notifications', title: 'Notificaciones',  icon:'ui-1_bell-53', class: '', roles: ['admin'] },
    { path: '/upgrade', title: 'Configuración',  icon:'objects_spaceship', class: 'active active-pro', roles: ['admin'] }
];

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  menuItems: any[] = [];

  constructor(
    public authService: AuthService,
    private router: Router
  ) { }

  ngOnInit() {
    this.menuItems = ROUTES.filter(menuItem => this.canAccessMenuItem(menuItem));
  }

  canAccessMenuItem(menuItem: RouteInfo): boolean {
    // Si no tiene roles definidos, todos pueden acceder
    if (!menuItem.roles || menuItem.roles.length === 0) {
      return true;
    }

    // Verificar si el usuario actual tiene alguno de los roles requeridos
    const userRole = this.authService.getUserRole();
    return userRole ? menuItem.roles.includes(userRole) : false;
  }
  
  isMobileMenu() {
      if ( window.innerWidth > 991) {
          return false;
      }
      return true;
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }
}

import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService, LoginRequest } from '../../../core/services/auth.service';
import { NotificationService } from '../../../core/services/notification.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="login-container">
      <div class="login-card slide-in-up">
        <div class="card glass">
          <div class="card-header text-center">
            <div class="login-icon">
              <i class="now-ui-icons ui-1_lock-circle-open"></i>
            </div>
            <h2 class="card-title text-title-contrast">Iniciar Sesión</h2>
            <p class="login-subtitle text-high-contrast">Accede a tu cuenta para continuar</p>
          </div>
          
          <div class="card-body">
            <form (ngSubmit)="onSubmit()" #loginForm="ngForm" class="login-form">
              <div class="form-group">
                <label for="email" class="form-label">
                  <span class="label-icon">
                    <i class="now-ui-icons users_single-02"></i>
                  </span>
                  Usuario
                </label>
                <input 
                  type="text" 
                  id="email"
                  class="form-control" 
                  [(ngModel)]="loginData.nombre_usuario"
                  name="nombre_usuario"
                  required
                  placeholder="admin"
                  #email="ngModel"
                  [class.is-invalid]="email.invalid && email.touched"
                >
                <div class="invalid-feedback" *ngIf="email.invalid && email.touched">
                  <div *ngIf="email.errors?.['required']">El usuario es requerido</div>
                </div>
              </div>

              <div class="form-group">
                <label for="password" class="form-label">
                  <span class="label-icon">
                    <i class="now-ui-icons ui-1_lock-circle-open"></i>
                  </span>
                  Contraseña
                </label>
                <input 
                  type="password" 
                  id="password"
                  class="form-control" 
                  [(ngModel)]="loginData.contrasena"
                  name="contrasena"
                  required
                  minlength="6"
                  placeholder="admin123"
                  #password="ngModel"
                  [class.is-invalid]="password.invalid && password.touched"
                >
                <div class="invalid-feedback" *ngIf="password.invalid && password.touched">
                  <div *ngIf="password.errors?.['required']">La contraseña es requerida</div>
                  <div *ngIf="password.errors?.['minlength']">La contraseña debe tener al menos 6 caracteres</div>
                </div>
              </div>

              <div class="form-group">
                <button 
                  type="submit" 
                  class="btn btn-primary w-100 btn-lg"
                  [disabled]="loginForm.invalid || loading"
                  [class.loading]="loading"
                >
                  <span *ngIf="loading" class="spinner"></span>
                  <span *ngIf="loading">Iniciando sesión...</span>
                  <span *ngIf="!loading">
                    <span class="btn-icon">
                      <i class="now-ui-icons arrows-1_cloud-upload-94"></i>
                    </span>
                    Iniciar Sesión
                  </span>
                </button>
              </div>

              <!-- Credenciales de prueba -->
              <div class="demo-credentials">
                <div class="demo-header">
                  <span class="demo-icon">
                    <i class="now-ui-icons objects_support-17"></i>
                  </span>
                  <strong>Credenciales de Prueba</strong>
                </div>
                <div class="demo-info">
                  <div class="credential-group">
                    <h4>
                      <i class="now-ui-icons users_single-02"></i>
                      Administrador
                    </h4>
                    <p><strong>Usuario:</strong> admin</p>
                    <p><strong>Contraseña:</strong> admin123</p>
                    <p class="role-info">Acceso completo a todas las funcionalidades</p>
                  </div>
                  <div class="credential-group">
                    <h4>
                      <i class="now-ui-icons shopping_bag-16"></i>
                      Consumidor
                    </h4>
                    <p><strong>Usuario:</strong> consumidor</p>
                    <p><strong>Contraseña:</strong> consumidor123</p>
                    <p class="role-info">Solo puede ver productos</p>
                  </div>
                </div>
              </div>

              <div class="form-options">
                <div class="text-center">
                  <a routerLink="/auth/forgot-password" class="link">
                    <span class="link-icon">
                      <i class="now-ui-icons ui-1_lock-circle-open"></i>
                    </span>
                    ¿Olvidaste tu contraseña?
                  </a>
                </div>

                <div class="text-center">
                  <span class="register-text">¿No tienes cuenta? </span>
                  <a routerLink="/auth/register" class="link">
                    <span class="link-icon">
                      <i class="now-ui-icons ui-1_simple-add"></i>
                    </span>
                    Regístrate aquí
                  </a>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .login-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 80vh;
      padding: 2rem;
    }
    
    .login-card {
      width: 100%;
      max-width: 450px;
    }

    .login-icon {
      font-size: 3rem;
      margin-bottom: 1rem;
      animation: pulse 2s infinite;
      color: var(--primary-color);
    }

    .login-icon i {
      font-size: 3rem;
      color: var(--primary-color);
    }

    .login-subtitle {
      color: #2c3e50;
      font-size: 1rem;
      margin-bottom: 0;
      font-weight: 500;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }

    .login-form {
      margin-top: 1.5rem;
    }

    .form-label {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-weight: 600;
      color: #2c3e50;
    }

    .label-icon {
      font-size: 1.125rem;
      color: var(--primary-color);
    }

    .label-icon i {
      font-size: 1.125rem;
      color: var(--primary-color);
    }

    .form-control {
      margin-top: 0.5rem;
      transition: all 0.3s ease;
    }

    .form-control:focus {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
    }

    .form-options {
      margin-top: 2rem;
      padding-top: 1.5rem;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    .link {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      color: var(--primary-color);
      text-decoration: none;
      font-weight: 500;
      transition: all 0.3s ease;
      padding: 0.5rem;
      border-radius: var(--radius-sm);
    }

    .link:hover {
      background: rgba(59, 130, 246, 0.1);
      transform: translateY(-1px);
    }

    .link-icon {
      font-size: 1rem;
    }

    .link-icon i {
      font-size: 1rem;
      margin-right: 0.25rem;
    }

    .register-text {
      color: #2c3e50;
      font-size: 0.875rem;
      font-weight: 500;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }

    .btn.loading {
      opacity: 0.8;
      cursor: not-allowed;
    }

    .btn-icon {
      margin-right: 0.5rem;
    }

    .btn-icon i {
      font-size: 1rem;
      margin-right: 0.25rem;
    }

    .demo-credentials {
      background: rgba(59, 130, 246, 0.1);
      border: 1px solid rgba(59, 130, 246, 0.2);
      border-radius: var(--radius-md);
      padding: 1rem;
      margin: 1.5rem 0;
      text-align: center;
    }

    .demo-header {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      margin-bottom: 0.75rem;
      color: var(--primary-color);
      font-size: 0.875rem;
    }

    .demo-icon {
      font-size: 1.125rem;
    }

    .demo-icon i {
      font-size: 1.125rem;
      color: var(--primary-color);
    }

    .demo-info {
      color: #2c3e50;
      font-size: 0.875rem;
      line-height: 1.5;
    }

    .demo-info p {
      margin: 0.25rem 0;
    }

    .credential-group {
      margin-bottom: 1.5rem;
      padding: 1rem;
      background: rgba(255, 255, 255, 0.05);
      border-radius: var(--radius-sm);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .credential-group:last-child {
      margin-bottom: 0;
    }

    .credential-group h4 {
      margin: 0 0 0.75rem 0;
      color: var(--primary-color);
      font-size: 1rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .credential-group h4 i {
      font-size: 1rem;
      color: var(--primary-color);
    }

    .role-info {
      font-style: italic;
      color: #7f8c8d;
      font-size: 0.8rem;
      margin-top: 0.5rem !important;
    }


    @keyframes pulse {
      0% {
        transform: scale(1);
      }
      50% {
        transform: scale(1.05);
      }
      100% {
        transform: scale(1);
      }
    }

    @media (max-width: 768px) {
      .login-container {
        padding: 1rem;
      }

      .login-card {
        max-width: 100%;
      }

      .login-icon {
        font-size: 2.5rem;
      }
    }

    @media (max-width: 480px) {
      .login-container {
        padding: 0.5rem;
      }

      .form-label {
        font-size: 0.875rem;
      }

      .link {
        font-size: 0.875rem;
      }
    }
  `]
})
export class LoginComponent implements OnInit {
  loginData: LoginRequest = {
    nombre_usuario: '',
    contrasena: ''
  };
  
  loading = false;

  constructor(
    private authService: AuthService,
    private notificationService: NotificationService,
    private router: Router
  ) { }

  ngOnInit(): void {
    // No redirigir automáticamente - dejar que el usuario vea el login
    // Si hay un token válido, el AuthGuard permitirá el acceso a rutas protegidas
    // Si el token es inválido, el AuthGuard redirigirá de vuelta al login
  }

  verificarBackend(): void {
    console.log('Verificando conectividad con el backend...');
    this.authService.verificarEstado().subscribe({
      next: (response) => {
        console.log('Backend conectado:', response);
      },
      error: (error) => {
        console.error('Error de conectividad con backend:', error);
        this.notificationService.showError('No se puede conectar con el servidor. Verifica que el backend esté ejecutándose en http://localhost:8000');
      }
    });
  }

  onSubmit(): void {
    if (this.loading) return;

    console.log('Intentando login con:', this.loginData);
    this.loading = true;
    
    // Verificar si es un login de prueba (admin/admin123)
    if (this.loginData.nombre_usuario === 'admin' && this.loginData.contrasena === 'admin123') {
      console.log('Login de prueba detectado, usando datos mock');
      this.loginMock();
      return;
    }
    
    this.authService.login(this.loginData).subscribe({
      next: (response) => {
        console.log('Respuesta del login:', response);
        this.authService.setUserData(response);
        this.notificationService.showSuccess('Inicio de sesión exitoso');
        
        // Redirigir según el rol
        if (response.nombre_usuario.es_admin) {
          this.router.navigate(['/dashboard']);
        } else {
          this.router.navigate(['/productos']);
        }
        this.loading = false;
      },
      error: (error) => {
        console.error('Error en login:', error);
        console.error('Error completo:', JSON.stringify(error));
        
        // Si el backend no está disponible, usar login mock
        if (error.status === 0 || error.status === undefined) {
          console.log('Backend no disponible, usando login mock');
          this.loginMock();
        } else {
          this.notificationService.showError('Error al iniciar sesión. Verifica tus credenciales.');
          this.loading = false;
        }
      }
    });
  }

  loginMock(): void {
    // Login mock para cuando el backend no está disponible
    const mockResponse = {
      clave: 'mock_token_' + Date.now(),
      nombre_usuario: {
        id: '1',
        nombre: 'Administrador',
        nombre_usuario: 'admin',
        email: 'admin@itm.edu.co',
        telefono: '',
        activo: true,
        es_admin: true,
        fecha_creacion: new Date().toISOString(),
        fecha_edicion: new Date().toISOString()
      }
    };
    
    console.log('Usando login mock:', mockResponse);
    this.authService.setUserData(mockResponse);
    this.notificationService.showSuccess('Inicio de sesión exitoso (modo demo)');
    
    // Verificar que los datos se guardaron en localStorage
    console.log('Verificando localStorage después del login:');
    console.log('Token:', localStorage.getItem('auth_token'));
    console.log('Usuario:', localStorage.getItem('user_data'));
    console.log('Rol:', localStorage.getItem('user_role'));
    
    this.router.navigate(['/dashboard']);
    this.loading = false;
  }

}

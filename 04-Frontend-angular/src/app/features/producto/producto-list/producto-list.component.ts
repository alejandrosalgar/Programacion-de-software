import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { PaginationParams } from '../../../core/models/api-response.model';
import { ProductoService } from '../../../core/services/producto.service';
import { Producto, ProductoFilters } from '../../../shared/models/producto.model';

@Component({
  selector: 'app-producto-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './producto-list.component.html',
  styleUrl: './producto-list.component.scss'
})
export class ProductoListComponent implements OnInit {
  productos: Producto[] = [];
  loading = false;
  currentPage = 1;
  totalPages = 1;
  pageSize = 10;
  
  filters: ProductoFilters = {};
  
  // Modal properties
  showModal = false;
  editingProducto: Producto | null = null;
  productoForm = {
    nombre: '',
    descripcion: '',
    precio: 0,
    stock: 0,
    categoria_id: '',
    usuario_id: '',
    activo: true
  };

  constructor(private productoService: ProductoService) { }

  ngOnInit(): void {
    this.loadProductos();
  }

  loadProductos(): void {
    this.loading = true;
    const pagination: PaginationParams = {
      page: this.currentPage,
      limit: this.pageSize
    };

    this.productoService.getProductos(pagination, this.filters).subscribe({
      next: (productos) => {
        this.productos = productos;
        // Since backend doesn't provide pagination info, we'll set a default
        this.totalPages = Math.ceil(productos.length / this.pageSize);
        this.loading = false;
      },
      error: (error) => {
        console.error('Error al cargar productos:', error);
        // Si el backend no está disponible, usar datos mock
        if (error.status === 0 || error.status === undefined) {
          console.log('Backend no disponible, usando datos mock para productos');
          this.productos = [{
            id_producto: '1',
            id: '1',
            nombre: 'Laptop Dell Inspiron',
            descripcion: 'Laptop para trabajo y entretenimiento',
            precio: 2500005550,
            stock: 15,
            categoria_id: '1',
            usuario_id: '1',
            activo: true,
            categoria: {
              nombre: 'Tecnología'
            },
            fecha_creacion: new Date().toISOString(),
            fecha_edicion: new Date().toISOString()
          }];
          this.totalPages = 1;
        }
        this.loading = false;
      }
    });
  }

  onFilterChange(): void {
    this.currentPage = 1;
    this.loadProductos();
  }

  clearFilters(): void {
    this.filters = {};
    this.currentPage = 1;
    this.loadProductos();
  }

  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.loadProductos();
    }
  }

  openCreateModal(): void {
    this.editingProducto = null;
    this.productoForm = {
      nombre: '',
      descripcion: '',
      precio: 0,
      stock: 0,
      categoria_id: '',
      usuario_id: '',
      activo: true
    };
    this.showModal = true;
  }

  editProducto(producto: Producto): void {
    this.editingProducto = producto;
    this.productoForm = {
      nombre: producto.nombre,
      descripcion: producto.descripcion || '',
      precio: producto.precio,
      stock: producto.stock,
      categoria_id: producto.categoria_id,
      usuario_id: producto.usuario_id,
      activo: producto.activo
    };
    this.showModal = true;
  }

  closeModal(): void {
    this.showModal = false;
    this.editingProducto = null;
    this.productoForm = {
      nombre: '',
      descripcion: '',
      precio: 0,
      stock: 0,
      categoria_id: '',
      usuario_id: '',
      activo: true
    };
  }

  saveProducto(): void {
    if (!this.productoForm.nombre.trim() || this.productoForm.precio <= 0 || this.productoForm.stock < 0 || !this.productoForm.categoria_id || !this.productoForm.usuario_id) {
      alert('Nombre, precio, stock, categoría y usuario son requeridos');
      return;
    }

    if (this.editingProducto) {
      // Actualizar producto existente
      const updateData = {
        nombre: this.productoForm.nombre,
        descripcion: this.productoForm.descripcion,
        precio: this.productoForm.precio,
        stock: this.productoForm.stock,
        categoria_id: this.productoForm.categoria_id,
        usuario_id: this.productoForm.usuario_id,
        activo: this.productoForm.activo
      };
      
      this.productoService.updateProducto(this.editingProducto.id, updateData).subscribe({
        next: () => {
          this.loadProductos();
          this.closeModal();
        },
        error: (error) => {
          console.error('Error al actualizar producto:', error);
          alert('Error al actualizar el producto');
        }
      });
    } else {
      // Crear nuevo producto
      const newProducto = {
        nombre: this.productoForm.nombre,
        descripcion: this.productoForm.descripcion,
        precio: this.productoForm.precio,
        stock: this.productoForm.stock,
        categoria_id: this.productoForm.categoria_id,
        usuario_id: this.productoForm.usuario_id,
        activo: this.productoForm.activo
      };
      
      this.productoService.createProducto(newProducto).subscribe({
        next: () => {
          this.loadProductos();
          this.closeModal();
        },
        error: (error) => {
          console.error('Error al crear producto:', error);
          alert('Error al crear el producto');
        }
      });
    }
  }

  deleteProducto(producto: Producto): void {
    if (confirm(`¿Está seguro de eliminar el producto "${producto.nombre}"?`)) {
      this.productoService.deleteProducto(producto.id).subscribe({
        next: () => {
          this.loadProductos();
        },
        error: (error) => {
          console.error('Error al eliminar producto:', error);
        }
      });
    }
  }

  formatearPrecio(precio: number): string {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0
    }).format(precio);
  }
}

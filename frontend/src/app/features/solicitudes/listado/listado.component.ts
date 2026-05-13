import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { EstadoSolicitud, Solicitud } from '../../../core/models/solicitud.model';
import { SolicitudService } from '../../../core/services/solicitud.service';
import { AuthService } from '../../../core/services/auth.service';

type FiltroEstado = 'todos' | EstadoSolicitud;

@Component({
  selector: 'app-listado',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './listado.component.html',
  styleUrl: './listado.component.css',
})
export class ListadoComponent implements OnInit {
  solicitudes: Solicitud[] = [];
  filtro: FiltroEstado = 'todos';
  loading = false;
  error: string | null = null;

  modalVisible = false;
  modalAccion: 'aprobado' | 'rechazado' | null = null;
  modalSolicitudId: number | null = null;
  modalComentario = '';
  modalError: string | null = null;

  readonly filtros: FiltroEstado[] = ['todos', 'pendiente', 'aprobado', 'rechazado'];

  constructor(private solicitudService: SolicitudService, public auth: AuthService) {}

  ngOnInit(): void {
    this.cargarSolicitudes();
  }

  cargarSolicitudes(): void {
    this.loading = true;
    this.error = null;
    const estado = this.filtro === 'todos' ? undefined : this.filtro;
    this.solicitudService.getAll(estado).subscribe({
      next: (data) => {
        this.solicitudes = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'No se pudo cargar el listado. Verifique que el servidor esté activo.';
        this.loading = false;
      },
    });
  }

  aplicarFiltro(filtro: FiltroEstado): void {
    this.filtro = filtro;
    this.cargarSolicitudes();
  }

  abrirModal(id: number, accion: 'aprobado' | 'rechazado'): void {
    this.modalSolicitudId = id;
    this.modalAccion = accion;
    this.modalComentario = '';
    this.modalError = null;
    this.modalVisible = true;
  }

  cerrarModal(): void {
    this.modalVisible = false;
    this.modalSolicitudId = null;
    this.modalAccion = null;
  }

  confirmarCambio(): void {
    if (!this.modalSolicitudId || !this.modalAccion) return;
    this.solicitudService
      .cambiarEstado(this.modalSolicitudId, { estado: this.modalAccion, comentario: this.modalComentario })
      .subscribe({
        next: () => {
          this.cerrarModal();
          this.cargarSolicitudes();
        },
        error: (err) => {
          const detail = err?.error?.detail;
          this.modalError = Array.isArray(detail)
            ? detail.map((e: any) => e.msg).join(' | ')
            : (detail ?? 'Error al cambiar el estado.');
        },
      });
  }

  formatMonto(monto: number): string {
    return monto.toLocaleString('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 });
  }

  formatFecha(fecha: string): string {
    return new Date(fecha).toLocaleDateString('es-CO', { year: 'numeric', month: 'short', day: '2-digit' });
  }
}

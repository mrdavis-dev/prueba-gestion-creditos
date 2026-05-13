export type EstadoSolicitud = 'pendiente' | 'aprobado' | 'rechazado';

export interface Solicitud {
  id: number;
  cedula: string;
  monto: number;
  plazo_meses: number;
  estado: EstadoSolicitud;
  comentario: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface SolicitudCreate {
  cedula: string;
  monto: number;
  plazo_meses: number;
}

export interface CambioEstado {
  estado: EstadoSolicitud;
  comentario: string;
}

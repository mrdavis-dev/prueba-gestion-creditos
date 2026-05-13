import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CambioEstado, Solicitud, SolicitudCreate } from '../models/solicitud.model';

@Injectable({ providedIn: 'root' })
export class SolicitudService {
  private readonly baseUrl = 'http://localhost:8000/solicitudes';

  constructor(private http: HttpClient) {}

  getAll(estado?: string): Observable<Solicitud[]> {
    let params = new HttpParams();
    if (estado) params = params.set('estado', estado);
    return this.http.get<Solicitud[]>(this.baseUrl + '/', { params });
  }

  create(data: SolicitudCreate): Observable<Solicitud> {
    return this.http.post<Solicitud>(this.baseUrl + '/', data);
  }

  cambiarEstado(id: number, cambio: CambioEstado): Observable<Solicitud> {
    return this.http.patch<Solicitud>(`${this.baseUrl}/${id}/estado`, cambio);
  }
}

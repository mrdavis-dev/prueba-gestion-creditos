import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { SolicitudService } from '../../../core/services/solicitud.service';

@Component({
  selector: 'app-formulario',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './formulario.component.html',
  styleUrl: './formulario.component.css',
})
export class FormularioComponent {
  form: FormGroup;
  loading = false;
  error: string | null = null;
  success = false;

  constructor(
    private fb: FormBuilder,
    private solicitudService: SolicitudService,
    private router: Router
  ) {
    this.form = this.fb.group({
      cedula: ['', [Validators.required, Validators.minLength(5)]],
      monto: [null, [Validators.required, Validators.min(500), Validators.max(50000)]],
      plazo_meses: [null, [Validators.required, Validators.min(6), Validators.max(60)]],
    });
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    this.loading = true;
    this.error = null;
    this.solicitudService.create(this.form.value).subscribe({
      next: () => {
        this.success = true;
        this.loading = false;
        setTimeout(() => this.router.navigate(['/']), 1500);
      },
      error: (err) => {
        const detail = err?.error?.detail;
        if (Array.isArray(detail)) {
          this.error = detail.map((e: any) => e.msg).join(' | ');
        } else {
          this.error = detail ?? 'Error al crear la solicitud.';
        }
        this.loading = false;
      },
    });
  }

  isInvalid(field: string): boolean {
    const ctrl = this.form.get(field);
    return !!(ctrl && ctrl.invalid && ctrl.touched);
  }
}

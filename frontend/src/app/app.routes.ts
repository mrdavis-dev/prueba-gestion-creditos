import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { LoginComponent } from './features/auth/login/login.component';
import { ListadoComponent } from './features/solicitudes/listado/listado.component';
import { FormularioComponent } from './features/solicitudes/formulario/formulario.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: '', component: ListadoComponent, canActivate: [authGuard] },
  { path: 'nueva', component: FormularioComponent, canActivate: [authGuard] },
  { path: '**', redirectTo: '' },
];

import AgendarView from '@/views/AgendarView.vue';
import CitasView from '@/views/CitasView.vue';
import DerivacionesView from '@/views/DerivacionesView.vue';
import DisponibilidadView from '@/views/DisponibilidadView.vue';
import EstadisticasView from '@/views/EstadisticasView.vue';
import FacturasView from '@/views/FacturasView.vue';
import HistorialClinicoView from '@/views/HistorialClinicoView.vue';
import MedicosView from '@/views/MedicosView.vue';
import PacientesView from '@/views/PacientesView.vue';
import ProveedoresLaboratorioView from '@/views/ProveedoresLaboratrorioView.vue';
import ProveedoresMedicoView from '@/views/ProveedoresMedicoView.vue';
import RolesView from '@/views/RolesView.vue';
import SeguridadAuditoria2View from '@/views/SeguridadAuditoria2View.vue';
import SeguridadAuditoriaView from '@/views/SeguridadAuditoriaView.vue';
import TratamientosView from '@/views/TratamientosView.vue';
import UsuariosView from '@/views/UsuariosView.vue';
//import PruebasView from '@/views/PruebasView.vue';
import LoginView from '@/views/LoginView.vue';
//import View from '@/views/View.vue';
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  { path: '/Pacientes', name: 'Pacientes', component: PacientesView },
  { path: '/Medicos', name: 'Medicos', component: MedicosView },
  { path: '/Agendar', name: 'Agendar', component: AgendarView },
  { path: '/Tratamientos', name: 'Tratamientos', component: TratamientosView },
  { path: '/HistorialClinico', name: 'HistorialClinico', component: HistorialClinicoView },
  { path: '/Derivaciones', name: '', component: DerivacionesView },
  { path: '/Estadisticas', name: '', component: EstadisticasView },
  { path: '/Facturas', name: '', component: FacturasView },
  { path: '/Usuarios', name: '', component: UsuariosView },
  { path: '/Roles', name: '', component: RolesView },
  { path: '/SeguridadAuditoria', name: '', component: SeguridadAuditoriaView },
  { path: '/SeguridadAuditoria2', name: '', component: SeguridadAuditoria2View },
  { path: '/ProveedoresLaboratorio', name: '', component: ProveedoresLaboratorioView },
  { path: '/ProveedoresMedico', name: '', component: ProveedoresMedicoView },
  { path: '/Disponibilidad', name: 'Disponibilidad', component: DisponibilidadView },
  { path: '/Citas', name: 'Citas', component: CitasView },
  //{ path: '/Pruebas', name: 'Pruebas', component: PruebasView },
  { path: '/Login', name: 'Login', component: LoginView },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;

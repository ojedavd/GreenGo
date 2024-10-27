import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class PopupService {

  constructor() { }

  makeCapitalPopup(data: any): string {
    return `` +
      `<div>Puntaje: 100 puntos</div>` +
      `<div>Llevas plantado: ${ data.population } árboles</div>`
  }
}

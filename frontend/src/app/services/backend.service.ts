import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class BackendService {

  constructor(private http: HttpClient) { }
  
  uploadFile(value: any) {
    return this.http.post<any>('http://localhost:5000/upload', value);
  }

  // getGscale(value: string) {
  //   return this.http.get<any>("http://localhost:5000/gscale/"+value);
  // }
}

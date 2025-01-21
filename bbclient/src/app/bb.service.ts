import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs'
import { of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { HttpHeaders } from '@angular/common/http'; 


@Injectable({
  providedIn: 'root'
})
export class BbService {
  private url: String = 'http://localhost:8000/api/';
  
  getBbs(): Observable<Object[]> {
    return this.http.get<Object[]>(`${this.url}bbs/`); 
  }
  
  getBb (pk: Number) : Observable<Object> {
    return this.http.get<Object>(`${this.url}bbs/${pk}`);
  }
  
  handleError () {
    return (error: any) : Observable<Object> => { window.alert(error.message);
      return of({});
    }
  }

  addComment(bb: String, author: String, password: String, content: String): Observable<Object>
  {
    const comment = {'bb': bb, 'author': author, 'content': content};
    const options = {
      headers: new HttpHeaders(
        {
          'Content_Type': 'application/json',
          'Authorization': 'Basic ' + window.btoa(author + ':' + password)
        }
      )
    };
    return this.http.post<Object>(`${this.url}bbs/${bb}/comments/`, comment, options).pipe(catchError(this.handleError()));
  }

  getComments(pk: Number): Observable<Object[]> {
    return this.http.get<Object[]>(`${this.url}bbs/${pk}/comments/`);
  }

  constructor(private http: HttpClient) { }
}

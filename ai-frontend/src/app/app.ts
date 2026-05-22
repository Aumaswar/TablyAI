import { Component, ChangeDetectorRef } from '@angular/core';

import { CommonModule } from '@angular/common';

import { FormsModule } from '@angular/forms';

import {
  HttpClient,
  HttpClientModule,
  HttpHeaders
} from '@angular/common/http';

@Component({

  selector: 'app-root',

  standalone: true,

  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule
  ],

  templateUrl: './app.html',

  styleUrls: ['./app.css']

})

export class AppComponent {

  host = '';

  username = '';

  password = '';

  database = '';

  dbType = 'mysql';

  question = '';

  responseData: any = null;

  schemaData: any = null;

  loading = false;

  token = '';

  appUsername = '';

  appPassword = '';

  metadataTable = '';

  metadataColumn = '';

  metadataDescription = '';

  constructor(

    private http: HttpClient,

    private cdr: ChangeDetectorRef

  ) {}

  login() {

    const body = {

      username: this.appUsername,

      password: this.appPassword

    };

    this.http.post(

      'http://localhost:8000/login',

      body

    ).subscribe({

      next: (response: any) => {

        console.log(response);

        this.token = response.access_token;

        localStorage.setItem(
          'token',
          this.token
        );

        alert('Login successful');

      },

      error: (error) => {

        console.error(error);

        alert('Login failed');

      }

    });

  }

  logout() {

    this.token = '';

    localStorage.removeItem('token');

    alert('Logged out');

  }

  connectDB() {

    const body = {

      db_type: this.dbType,

      host: this.host,

      username: this.username,

      password: this.password,

      database: this.database

    };

    this.http.post(

      'http://localhost:8000/connect-db',

      body

    ).subscribe({

      next: (response: any) => {

        console.log(response);

        alert(response.message);

      },

      error: (error) => {

        console.error(error);

        alert('Connection failed');

      }

    });

  }

  saveMetadata() {

    const token = localStorage.getItem(
      'token'
    );

    const headers = new HttpHeaders({

      Authorization: `Bearer ${token}`

    });

    const body = {

      table_name: this.metadataTable,

      column_name: this.metadataColumn,

      description: this.metadataDescription

    };

    this.http.post(

      'http://localhost:8000/save-metadata',

      body,

      { headers }

    ).subscribe({

      next: (response: any) => {

        console.log(response);

        alert('Metadata saved');

        this.metadataTable = '';

        this.metadataColumn = '';

        this.metadataDescription = '';

      },

      error: (error) => {

  console.log(error);

  if (error.error) {

    alert(
      JSON.stringify(error.error)
    );

  } else {

    alert('Failed to save metadata');

  }

}
    });

  }

  askAI() {

    if (!this.question.trim()) {

      alert('Please enter a question');

      return;

    }

    const token = localStorage.getItem(
      'token'
    );

    const headers = new HttpHeaders({

      Authorization: `Bearer ${token}`

    });

    this.loading = true;

    this.responseData = null;

    this.http.get(

      `http://localhost:8000/query?question=${encodeURIComponent(this.question)}`,

      { headers }

    ).subscribe({

      next: (response: any) => {

        console.log(response);

        this.responseData = response;

        this.loading = false;

        this.cdr.detectChanges();

      },

      error: (error) => {

        console.error(error);

        this.loading = false;

        alert('Query failed');

      }

    });

  }

  loadSchema() {

    this.http.get(

      'http://localhost:8000/schemas'

    ).subscribe({

      next: (response: any) => {

        console.log(response);

        this.schemaData = response;

        this.cdr.detectChanges();

      },

      error: (error) => {

        console.error(error);

        alert('Failed to load schema');

      }

    });

  }

  objectKeys(obj: any): string[] {

    return Object.keys(obj);

  }

} 